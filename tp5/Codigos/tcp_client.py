#!/usr/bin/env python3
# tcp_client.py

"""
TCP Client Application.

This script connects to a TCP server, sends a predefined number of packets,
awaits acknowledgments (ACKs) for each packet, and calculates Round-Trip Time (RTT)
metrics (latency, jitter). It supports optional payload encryption using Fernet.

Purpose:
- Demonstrate TCP communication (connection-oriented, reliable).
- Measure network performance metrics like latency and jitter over TCP.
- Implement and test symmetric payload encryption.
- Log communication events for analysis.
"""

import socket
import time
import statistics
import config_client as config  # Using 'config' alias for brevity
from cryptography.fernet import Fernet, InvalidToken
from typing import List, Tuple, Optional, Union

# --- Encryption Configuration ---
# ENCRYPT: Set to True to enable payload encryption, False to disable.
# This allows testing the impact of encryption on performance and verifying
# payload confidentiality in tools like Wireshark.
ENCRYPT: bool = False # Default to False; can be set to True for encryption testing.
cipher_suite: Optional[Fernet] = None

if ENCRYPT:
    if not config.ENCRYPTION_KEY or config.ENCRYPTION_KEY == b'YOUR_GENERATED_FERNET_KEY_HERE=': # Generic placeholder check
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
    Logs a message to the specified file in CSV format.

    Purpose:
    To create a structured record of communication events (sent packets, received ACKs)
    with precise timestamps, allowing for later analysis of the communication flow
    and performance.

    Args:
        filename: The name of the log file.
        direction: "SENT" or "ACK_RECEIVED".
        timestamp: The time of the event (from time.time()).
        message_id: The unique identifier of the message or ACK.
        data_str: The payload content (for SENT) or empty (for ACK_RECEIVED).
        latency_str: The calculated latency (for ACK_RECEIVED) or empty.
    """
    try:
        with open(filename, 'a') as f:
            f.write(f"{timestamp:.6f},{direction},{message_id},{data_str},{latency_str}\n")
    except IOError as e:
        print(f"Error writing to log file {filename}: {e}")

def calculate_metrics(latencies: List[float]) -> Union[Tuple[float, float, float, float], Tuple[None, None, None, None]]:
    """
    Calculates average, max, min latency, and average jitter from a list of latencies.

    Purpose:
    To quantify network performance based on the RTTs observed.
    - Latency (RTT): Time taken for a packet to go to the server and an ACK to return.
    - Jitter: Variation in packet delay, important for real-time applications.

    Args:
        latencies: A list of latency values (in seconds).

    Returns:
        A tuple containing (avg_latency, max_latency, min_latency, avg_jitter) in seconds.
        Returns (None, None, None, None) if latencies list is too short for calculations.
    """
    if not latencies:
        return None, None, None, None

    avg_latency: float = statistics.mean(latencies)
    max_latency: float = max(latencies)
    min_latency: float = min(latencies)

    if len(latencies) < 2: # Jitter calculation requires at least two latency values
        avg_jitter = 0.0
    else:
        jitters: List[float] = [abs(latencies[i] - latencies[i-1]) for i in range(1, len(latencies))]
        avg_jitter = statistics.mean(jitters) if jitters else 0.0

    return avg_latency, max_latency, min_latency, avg_jitter

def main() -> None:
    """
    Main function to run the TCP client.
    Establishes connection, sends packets, receives ACKs, logs, and calculates metrics.
    """
    print("Starting TCP client...")
    # AF_INET: Address family IPv4
    # SOCK_STREAM: Socket type for TCP (connection-oriented, reliable stream)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_address = (config.HOST, config.TCP_PORT)
        print(f"Attempting to connect to server at {server_address}...")
        client_socket.connect(server_address)
        print(f"TCP client connected to {server_address}")
        print(f"Encryption active: {ENCRYPT}")

        # Initialize/clear log file at the start of a session
        try:
            with open(config.LOG_FILE_TCP_CLIENT, 'w') as f:
                f.write("Timestamp,Direction,MessageID,Data,Latency(s)\n")
        except IOError as e:
            print(f"Error initializing log file {config.LOG_FILE_TCP_CLIENT}: {e}")
            # Decide if to exit or continue without logging
            # For this example, we'll print an error and continue,
            # but logging functionality will be compromised.

        latencies: List[float] = []

        print(f"\n--- Sending {config.NUM_PACKETS_METRICS} TCP packets for metrics ---")
        for i in range(config.NUM_PACKETS_METRICS):
            message_id: str = f"{config.GROUP_NAME}-{i+1}"
            payload_content: str = f"This is the payload of TCP packet {i+1}"
            # Message format: "ID:Payload" for easier parsing by the server
            message_to_send: str = f"{message_id}:{payload_content}"

            send_data_bytes: bytes = message_to_send.encode('utf-8')
            if ENCRYPT and cipher_suite:
                send_data_bytes = cipher_suite.encrypt(send_data_bytes)

            send_timestamp: float = time.time()
            # sendall() is used for TCP to ensure the entire message is sent,
            # as send() might only send a part of it.
            client_socket.sendall(send_data_bytes)
            log_message(config.LOG_FILE_TCP_CLIENT, "SENT", send_timestamp, message_id, payload_content)
            # print(f"Sent (ID: {message_id}): '{payload_content}'") # Optional: for verbose console output

            # Wait for ACK from server
            # BUFFER_SIZE determines the maximum data received in one call.
            # For ACKs, this is usually small.
            ack_received_data: bytes = client_socket.recv(config.BUFFER_SIZE)
            ack_receive_timestamp: float = time.time()

            ack_message: str
            if ENCRYPT and cipher_suite:
                try:
                    ack_message = cipher_suite.decrypt(ack_received_data).decode('utf-8')
                except InvalidToken:
                    print(f"Error: Failed to decrypt ACK for {message_id}. Token invalid (key mismatch or corrupted data).")
                    ack_message = f"ERROR_DECRYPT_ACK: {ack_received_data[:50]}..." # Log partial raw data
                except Exception as e:
                    print(f"Error decrypting ACK for {message_id}: {e}")
                    ack_message = f"ERROR_DECRYPT_ACK: {ack_received_data[:50]}..."
            else:
                ack_message = ack_received_data.decode('utf-8')

            latency: float = ack_receive_timestamp - send_timestamp
            latencies.append(latency)

            log_message(config.LOG_FILE_TCP_CLIENT, "ACK_RECEIVED", ack_receive_timestamp, ack_message, "", f"{latency:.6f}")
            # print(f"Received ACK: '{ack_message}', Latency: {latency:.4f}s") # Optional

            if (i + 1) % 10 == 0: # Print progress every 10 packets
                print(f"Packets sent and ACKs received: {i+1}/{config.NUM_PACKETS_METRICS}")

            # SEND_INTERVAL_SECONDS controls the frequency of sending packets.
            # This helps to avoid overwhelming the network or server and provides
            # a more controlled environment for measuring metrics.
            time.sleep(config.SEND_INTERVAL_SECONDS)

        # Calculate and display metrics
        metrics = calculate_metrics(latencies)
        if metrics[0] is not None:
            avg_lat, max_lat, min_lat, avg_jit = metrics
            print("\n--- TCP Connection Metrics (RTT) ---")
            print(f"Average Latency: {avg_lat * 1000:.2f} ms")
            print(f"Maximum Latency: {max_lat * 1000:.2f} ms")
            print(f"Minimum Latency: {min_lat * 1000:.2f} ms")
            print(f"Average Jitter:  {avg_jit * 1000:.2f} ms")

            # Log metrics to file
            log_message(config.LOG_FILE_TCP_CLIENT, "\n--- TCP Metrics ---", time.time(), "", "")
            log_message(config.LOG_FILE_TCP_CLIENT, f"Avg Latency: {avg_lat * 1000:.2f} ms", time.time(), "", "")
            # ... (log other metrics similarly or use a dedicated metrics log format)
            # For simplicity, we'll just print to console and a brief summary in log
            with open(config.LOG_FILE_TCP_CLIENT, 'a') as f:
                f.write(f"\n--- TCP Metrics ---\n")
                f.write(f"Avg Latency: {avg_lat*1000:.2f} ms\n")
                f.write(f"Max Latency: {max_lat*1000:.2f} ms\n")
                f.write(f"Min Latency: {min_lat*1000:.2f} ms\n")
                f.write(f"Avg Jitter:  {avg_jit*1000:.2f} ms\n")
        else:
            print("Not enough data to calculate metrics.")

        # Optional: Send a finalization message to the server.
        # This could signal the server that the client is done sending metrics packets.
        # Currently, this part is commented out; server relies on client closing connection
        # or a predefined number of packets if server tracks it.
        # end_message = f"{config.GROUP_NAME}-END_OF_METRICS:FIN"
        # end_data = end_message.encode('utf-8')
        # if ENCRYPT and cipher_suite:
        #     end_data = cipher_suite.encrypt(end_data)
        # client_socket.sendall(end_data)
        # log_message(config.LOG_FILE_TCP_CLIENT, "SENT", time.time(), f"{config.GROUP_NAME}-END_OF_METRICS", "FIN")

    except socket.error as e:
        print(f"Socket error: {e}")
    except ConnectionRefusedError:
        print(f"Error: Connection refused. Server at {config.HOST}:{config.TCP_PORT} might not be running or is unreachable.")
    except Exception as e:
        print(f"An unexpected error occurred in the client: {e}")
    finally:
        # It's crucial to close the socket to release system resources.
        print("Closing TCP client socket.")
        client_socket.close()
        print("TCP client finished.")

if __name__ == "__main__":
    main()
