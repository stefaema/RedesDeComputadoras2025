#!/usr/bin/env python3
# udp_client.py

"""
UDP Client Application.

This script sends a predefined number of datagrams to a UDP server,
awaits acknowledgments (ACKs) for each datagram (with a timeout), and
calculates Round-Trip Time (RTT) metrics (latency, jitter) based on received ACKs.
It also estimates packet loss. Supports optional payload encryption using Fernet.

Purpose:
- Demonstrate UDP communication (connectionless, unreliable).
- Measure network performance metrics over UDP, accounting for potential packet loss.
- Implement and test symmetric payload encryption for UDP.
- Log communication events, including timeouts for ACKs.
- Send a control message to the server to signal completion.
"""

import socket
import time
import statistics
import config_client as config # Using 'config' alias for brevity
from cryptography.fernet import Fernet, InvalidToken
from typing import List, Tuple, Optional, Union

# --- Encryption Configuration ---
ENCRYPT: bool = True # Default to True for UDP to emphasize security for potentially broadcast/less controlled medium
cipher_suite: Optional[Fernet] = None

if ENCRYPT:
    if not config.ENCRYPTION_KEY or config.ENCRYPTION_KEY == b'YOUR_GENERATED_FERNET_KEY_HERE=':
        print("Error: Encryption key not configured in config_client.py. Please generate and set it.")
        exit(1)
    try:
        cipher_suite = Fernet(config.ENCRYPTION_KEY)
    except ValueError as e:
        print(f"Error initializing Fernet cipher suite: {e}. Ensure the key is valid.")
        exit(1)
# --- End Encryption Configuration ---

def log_message(filename: str, direction: str, timestamp: float,
                message_id: str, data_str: str, latency_str: str = "") -> None:
    """
    Logs a message to the specified file in CSV format. (Identical to TCP client's)
    """
    try:
        with open(filename, 'a') as f:
            f.write(f"{timestamp:.6f},{direction},{message_id},{data_str},{latency_str}\n")
    except IOError as e:
        print(f"Error writing to log file {filename}: {e}")

def calculate_metrics(latencies: List[float]) -> Union[Tuple[float, float, float, float], Tuple[None, None, None, None]]:
    """
    Calculates average, max, min latency, and average jitter. (Identical to TCP client's)
    """
    if not latencies:
        return None, None, None, None
    avg_latency: float = statistics.mean(latencies)
    max_latency: float = max(latencies)
    min_latency: float = min(latencies)
    if len(latencies) < 2:
        avg_jitter = 0.0
    else:
        jitters: List[float] = [abs(latencies[i] - latencies[i-1]) for i in range(1, len(latencies))]
        avg_jitter = statistics.mean(jitters) if jitters else 0.0
    return avg_latency, max_latency, min_latency, avg_jitter

def main() -> None:
    """
    Main function to run the UDP client.
    Sends datagrams, waits for ACKs (with timeout), logs, calculates metrics,
    and signals server completion.
    """
    print("Starting UDP client...")
    # AF_INET: Address family IPv4
    # SOCK_DGRAM: Socket type for UDP (connectionless, datagram-based)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address: Tuple[str, int] = (config.HOST, config.UDP_PORT)
    print(f"UDP client will send to {server_address}")
    print(f"Encryption active: {ENCRYPT}")

    # Set a timeout for socket operations (specifically recvfrom).
    # If an ACK is not received within this time, a socket.timeout exception occurs.
    # Timeout is set to twice the send interval to give ample time for ACK.
    client_socket.settimeout(config.SEND_INTERVAL_SECONDS * 2)

    try:
        with open(config.LOG_FILE_UDP_CLIENT, 'w') as f:
            f.write("Timestamp,Direction,MessageID,Data,Latency(s)\n")
    except IOError as e:
        print(f"Error initializing log file {config.LOG_FILE_UDP_CLIENT}: {e}")

    latencies: List[float] = []
    packets_sent_successfully: int = 0 # Counts packets where sendto() didn't raise an immediate error.
    acks_received: int = 0

    print(f"\n--- Sending {config.NUM_PACKETS_METRICS} UDP packets for metrics ---")
    for i in range(config.NUM_PACKETS_METRICS):
        message_id: str = f"{config.GROUP_NAME}-{i+1}"
        payload_content: str = f"This is the payload of UDP packet {i+1}"
        message_to_send: str = f"{message_id}:{payload_content}"

        send_data_bytes: bytes = message_to_send.encode('utf-8')
        if ENCRYPT and cipher_suite:
            send_data_bytes = cipher_suite.encrypt(send_data_bytes)

        send_timestamp: float = time.time()
        try:
            # sendto() is used for UDP as it's connectionless; address is specified each time.
            client_socket.sendto(send_data_bytes, server_address)
            packets_sent_successfully +=1
            log_message(config.LOG_FILE_UDP_CLIENT, "SENT", send_timestamp, message_id, payload_content)

            # Wait for ACK from server
            # recvfrom() also returns the address of the sender, though we expect it from server_address.
            ack_received_data, _ = client_socket.recvfrom(config.BUFFER_SIZE)
            ack_receive_timestamp: float = time.time()
            acks_received += 1

            ack_message: str
            if ENCRYPT and cipher_suite:
                try:
                    ack_message = cipher_suite.decrypt(ack_received_data).decode('utf-8')
                except InvalidToken:
                    print(f"Error: Failed to decrypt ACK for UDP {message_id}. Token invalid.")
                    ack_message = f"ERROR_DECRYPT_ACK_UDP: {ack_received_data[:50]}..."
                except Exception as e:
                    print(f"Error decrypting ACK for UDP {message_id}: {e}")
                    ack_message = f"ERROR_DECRYPT_ACK_UDP: {ack_received_data[:50]}..."
            else:
                ack_message = ack_received_data.decode('utf-8')

            latency: float = ack_receive_timestamp - send_timestamp
            latencies.append(latency)
            log_message(config.LOG_FILE_UDP_CLIENT, "ACK_RECEIVED", ack_receive_timestamp, ack_message, "", f"{latency:.6f}")

        except socket.timeout:
            # This occurs if recvfrom() exceeds the timeout set earlier.
            print(f"Timeout waiting for ACK for UDP packet {message_id}")
            log_message(config.LOG_FILE_UDP_CLIENT, "ACK_TIMEOUT", time.time(), message_id, "TIMEOUT_NO_ACK")
        except socket.error as e:
            # This could be an error during sendto or recvfrom (other than timeout).
            print(f"Socket error during send/recv for packet {message_id}: {e}")
            log_message(config.LOG_FILE_UDP_CLIENT, "SOCKET_ERROR", time.time(), message_id, str(e))
        except Exception as e:
            print(f"An unexpected error occurred for packet {message_id}: {e}")
            log_message(config.LOG_FILE_UDP_CLIENT, "UNEXPECTED_ERROR", time.time(), message_id, str(e))

        if (i + 1) % 10 == 0: # Print progress
            print(f"UDP Packets: {i+1}/{config.NUM_PACKETS_METRICS} attempts. Successfully sent: {packets_sent_successfully}, ACKs received: {acks_received}.")

        # SEND_INTERVAL_SECONDS controls send frequency.
        time.sleep(config.SEND_INTERVAL_SECONDS)

    # --- Summary and Metrics ---
    print(f"\n--- UDP Send Summary ---")
    print(f"Total UDP packets attempted to send: {config.NUM_PACKETS_METRICS}")
    print(f"Total UDP packets successfully sent (sendto did not fail): {packets_sent_successfully}")
    print(f"Total UDP ACKs received: {acks_received}")

    packet_loss_percentage: float = 0.0
    if packets_sent_successfully > 0:
        # Packet loss is estimated as (packets sent - ACKs received) / packets sent.
        # This assumes each sent packet should have received an ACK.
        packet_loss_percentage = ((packets_sent_successfully - acks_received) / packets_sent_successfully) * 100
    print(f"Estimated packet loss (based on ACKs): {packet_loss_percentage:.2f}%")

    metrics = calculate_metrics(latencies)
    if metrics[0] is not None:
        avg_lat, max_lat, min_lat, avg_jit = metrics
        print("\n--- UDP Connection Metrics (RTT of ACKs) ---")
        print(f"Based on {len(latencies)} ACKs received from {packets_sent_successfully} packets successfully sent:")
        print(f"Average Latency: {avg_lat * 1000:.2f} ms")
        print(f"Maximum Latency: {max_lat * 1000:.2f} ms")
        print(f"Minimum Latency: {min_lat * 1000:.2f} ms")
        print(f"Average Jitter:  {avg_jit * 1000:.2f} ms")

        with open(config.LOG_FILE_UDP_CLIENT, 'a') as f:
            f.write(f"\n--- UDP Metrics ---\n")
            f.write(f"Attempted sends: {config.NUM_PACKETS_METRICS}\n")
            f.write(f"Packets sent (sendto successful): {packets_sent_successfully}\n")
            f.write(f"ACKs received: {acks_received}\n")
            f.write(f"Estimated loss: {packet_loss_percentage:.2f}%\n")
            f.write(f"Avg Latency (based on ACKs): {avg_lat*1000:.2f} ms\n")
            f.write(f"Max Latency: {max_lat*1000:.2f} ms\n")
            f.write(f"Min Latency: {min_lat*1000:.2f} ms\n")
            f.write(f"Avg Jitter:  {avg_jit*1000:.2f} ms\n")
    else:
        print("No ACKs received, cannot calculate latency metrics for UDP.")
        with open(config.LOG_FILE_UDP_CLIENT, 'a') as f:
             f.write(f"\n--- UDP Metrics ---\nNo ACKs received.\n")

    # --- Send End-of-Metrics Signal to Server ---
    # This is a control message to inform the server that the client has finished
    # its metrics-gathering phase and the server can potentially terminate or reset.
    print("\nSending end-of-metrics signal to UDP server...")
    end_message_id: str = f"{config.GROUP_NAME}-END_OF_METRICS_UDP"
    end_payload: str = "Client metrics phase finished"
    end_message_to_send: str = f"{end_message_id}:{end_payload}"

    end_send_data_bytes: bytes = end_message_to_send.encode('utf-8')
    if ENCRYPT and cipher_suite:
        end_send_data_bytes = cipher_suite.encrypt(end_send_data_bytes)

    try:
        # Send the signal multiple times because UDP is unreliable.
        # This increases the probability of the server receiving it.
        # No ACK is expected for this control message to keep it simple.
        for _ in range(3): # Send 3 times
            client_socket.sendto(end_send_data_bytes, server_address)
            time.sleep(0.1) # Small delay between retransmissions
        log_message(config.LOG_FILE_UDP_CLIENT, "SENT_CONTROL_MSG", time.time(), end_message_id, end_payload)
        print("End-of-metrics signal sent to server.")
    except socket.error as e:
        print(f"Error sending end-of-metrics signal for UDP: {e}")
        log_message(config.LOG_FILE_UDP_CLIENT, "ERROR_CONTROL_MSG", time.time(), end_message_id, str(e))
    # --- End of Signal Sending ---

    # It's crucial to close the socket to release system resources.
    print("Closing UDP client socket.")
    client_socket.close()
    print("UDP client finished.")

if __name__ == "__main__":
    main()
