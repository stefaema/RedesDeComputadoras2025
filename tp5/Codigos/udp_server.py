#!/usr/bin/env python3
# udp_server.py

"""
UDP Server Application.

This script listens for incoming UDP datagrams, processes them, sends
acknowledgments (ACKs) back to the client's address, and logs these events.
It supports optional payload decryption if the client sends encrypted data.
The server is designed to terminate after receiving a specific end-of-metrics
signal from the client.

Purpose:
- Demonstrate UDP server operations (bind, recvfrom, sendto).
- Act as a counterpart to udp_client.py for testing UDP communication.
- Implement and test symmetric payload decryption for UDP.
- Log received datagrams for analysis.
- Handle a client-initiated termination signal.
"""

import socket
import time
import config_server as config # Using 'config' alias for brevity
from cryptography.fernet import Fernet, InvalidToken
from typing import Optional, Tuple

# --- Encryption Configuration ---
ENCRYPT: bool = True # Default to True for UDP, consistent with udp_client.py
cipher_suite: Optional[Fernet] = None

if ENCRYPT:
    if not config.ENCRYPTION_KEY or config.ENCRYPTION_KEY == b'YOUR_GENERATED_FERNET_KEY_HERE=':
        print("Error: Encryption key not configured in config_server.py. Please generate and set it.")
        exit(1)
    try:
        cipher_suite = Fernet(config.ENCRYPTION_KEY)
    except ValueError as e:
        print(f"Error initializing Fernet cipher suite: {e}. Ensure the key is valid.")
        exit(1)
# --- End Encryption Configuration ---

def log_message(filename: str, direction: str, timestamp: float,
                message_id: str, data_str: str, client_addr_str: str = "") -> None:
    """
    Logs a message to the specified file in CSV format.

    Purpose:
    To create a structured record of received datagrams, including the client's address,
    with precise timestamps for analysis.

    Args:
        filename: The name of the log file.
        direction: "RECEIVED" (or "ACK_SENT_FROM_SERVER" if needed).
        timestamp: The time of the event (from time.time()).
        message_id: The unique identifier of the received message.
        data_str: The payload content of the received message.
        client_addr_str: The string representation of the client's address (IP, port).
    """
    try:
        with open(filename, 'a') as f:
            f.write(f"{timestamp:.6f},{direction},{message_id},{data_str},{client_addr_str}\n")
    except IOError as e:
        print(f"Error writing to log file {filename}: {e}")

def main() -> None:
    """
    Main function to run the UDP server.
    Binds to an address, receives datagrams, sends ACKs, logs events,
    and waits for a client signal to terminate.
    """
    # AF_INET: Address family IPv4
    # SOCK_DGRAM: Socket type for UDP (connectionless, datagram-based)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # SO_REUSEADDR helps in quickly restarting the server if needed.
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_address: Tuple[str, int] = (config.HOST, config.UDP_PORT)
        server_socket.bind(server_address)
        print(f"UDP server listening on {server_address}")
        print(f"Encryption active: {ENCRYPT}")
    except OSError as e:
        # OSError can occur if the address is already in use and SO_REUSEADDR doesn't solve it,
        # or if there are permission issues to bind to the port.
        print(f"Error binding UDP server to {server_address}: {e}")
        return # Exit if binding fails

    try:
        with open(config.LOG_FILE_UDP_SERVER, 'w') as f:
            f.write("Timestamp,Direction,MessageID,Data,ClientAddr\n")
    except IOError as e:
        print(f"Error initializing log file {config.LOG_FILE_UDP_SERVER}: {e}")

    packets_received_count: int = 0
    # client_finished_metrics controls the main server loop.
    # The server will continue to process packets until the client signals it's done.
    client_finished_metrics: bool = False

    try:
        while not client_finished_metrics:
            print("\nWaiting to receive UDP message...")
            try:
                # recvfrom() is a blocking call: it waits for a UDP datagram.
                # It returns the data and the address (ip, port) of the client that sent it.
                # BUFFER_SIZE is the maximum data to receive.
                # Optional: server_socket.settimeout(60.0) # e.g., 60 seconds
                # If a timeout is set, the server could shut down if no client activity is seen.
                data_received, client_address = server_socket.recvfrom(config.BUFFER_SIZE)
            except socket.timeout:
                # This block would execute if server_socket.settimeout() was used and expired.
                print("UDP Server: Timeout waiting for packets. Shutting down.")
                break # Exit the loop if server times out.
            except socket.error as e_recv:
                print(f"Socket error during recvfrom: {e_recv}. Continuing...")
                continue # Skip this iteration and try to receive again.

            receive_timestamp: float = time.time()
            message_content: str
            payload: str

            if ENCRYPT and cipher_suite:
                try:
                    message_content = cipher_suite.decrypt(data_received).decode('utf-8')
                except InvalidToken:
                    print(f"Error: Failed to decrypt UDP message from {client_address}. Token invalid. Data: {data_received[:50]}...")
                    message_content = f"ERROR_DECRYPT_UDP: {data_received[:50]}..."
                    payload = "DECRYPTION_ERROR"
                except Exception as e:
                    print(f"Error decrypting UDP message from {client_address}: {e}. Data: {data_received[:50]}...")
                    message_content = f"ERROR_DECRYPT_UDP: {data_received[:50]}..."
                    payload = "DECRYPTION_ERROR"
            else:
                message_content = data_received.decode('utf-8')

            parts = message_content.split(':', 1)
            message_id_full: str = parts[0]
            if "ERROR_DECRYPT_UDP" not in message_id_full:
                payload = parts[1] if len(parts) > 1 else "N/A_PAYLOAD"

            print(f"Received from {client_address} (ID: {message_id_full}): '{payload}'")
            log_message(config.LOG_FILE_UDP_SERVER, "RECEIVED", receive_timestamp,
                        message_id_full, payload, str(client_address))
            packets_received_count += 1

            # Check for the special end-of-metrics signal from the client.
            if "END_OF_METRICS_UDP" in message_id_full:
                print(f"End-of-metrics signal received from {client_address}. UDP server will terminate after this.")
                client_finished_metrics = True
                # No ACK is sent for this control message to keep client logic simple.
            else:
                # For regular data packets, send an ACK back to the client.
                # The client_address obtained from recvfrom() is used to send the ACK.
                ack_message_str: str = f"ACK_UDP_FOR_{message_id_full}"
                ack_data_bytes: bytes = ack_message_str.encode('utf-8')

                if ENCRYPT and cipher_suite: # Encrypt ACKs if communication is encrypted
                    ack_data_bytes = cipher_suite.encrypt(ack_data_bytes)

                server_socket.sendto(ack_data_bytes, client_address)
                # print(f"ACK sent to {client_address} for {message_id_full}") # Optional: verbose ACK sending log

    except KeyboardInterrupt:
        print("\nUDP Server is shutting down due to KeyboardInterrupt (Ctrl+C).")
    except Exception as e:
        print(f"An unexpected error occurred in the UDP server: {e}")
    finally:
        # It's crucial to close the socket to release system resources.
        print(f"Total UDP packets processed by server: {packets_received_count}")
        print("Closing UDP server socket.")
        server_socket.close()
        print("UDP server shut down.")

if __name__ == "__main__":
    main()
