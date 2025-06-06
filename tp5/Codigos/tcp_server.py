#!/usr/bin/env python3
# tcp_server.py

"""
TCP Server Application.

This script listens for incoming TCP connections, receives packets from a client,
sends acknowledgments (ACKs) back for each packet, and logs these events.
It supports optional payload decryption using Fernet if the client sends
encrypted data.

Purpose:
- Demonstrate TCP server operations (bind, listen, accept, recv, send).
- Act as a counterpart to tcp_client.py for testing TCP communication.
- Implement and test symmetric payload decryption.
- Log received packets for analysis.
"""

import socket
import time
import config_server as config # Using 'config' alias for brevity
from cryptography.fernet import Fernet, InvalidToken
from typing import Optional

# --- Encryption Configuration ---
# ENCRYPT: Set to True to enable payload decryption, False to disable.
# This must match the client's ENCRYPT setting if encrypted communication is desired.
ENCRYPT: bool = False # Default to False; can be set to True for encryption testing.
cipher_suite: Optional[Fernet] = None

if ENCRYPT:
    if not config.ENCRYPTION_KEY or config.ENCRYPTION_KEY == b'YOUR_GENERATED_FERNET_KEY_HERE=': # Generic placeholder check
        print("Error: Encryption key not configured in config_server.py. Please generate and set it.")
        exit(1)
    try:
        cipher_suite = Fernet(config.ENCRYPTION_KEY)
    except ValueError as e:
        print(f"Error initializing Fernet cipher suite: {e}. Ensure the key is valid.")
        exit(1)
# --- End Encryption Configuration ---

def log_message(filename: str, direction: str, timestamp: float,
                message_id: str, data_str: str) -> None:
    """
    Logs a message to the specified file in CSV format.

    Purpose:
    To create a structured record of received packets with precise timestamps,
    allowing for later analysis of the communication flow from the server's perspective.

    Args:
        filename: The name of the log file.
        direction: "RECEIVED" (could be extended for "ACK_SENT" if needed).
        timestamp: The time of the event (from time.time()).
        message_id: The unique identifier of the received message.
        data_str: The payload content of the received message.
    """
    try:
        with open(filename, 'a') as f:
            f.write(f"{timestamp:.6f},{direction},{message_id},{data_str}\n")
    except IOError as e:
        print(f"Error writing to log file {filename}: {e}")

def main() -> None:
    """
    Main function to run the TCP server.
    Binds to an address, listens for connections, processes incoming data,
    sends ACKs, and logs events.
    """
    # AF_INET: Address family IPv4
    # SOCK_STREAM: Socket type for TCP (connection-oriented, reliable stream)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # SO_REUSEADDR allows the server to restart and bind to the same address
    # if it was recently closed, preventing "Address already in use" errors.
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    conn: Optional[socket.socket] = None # To ensure conn is defined for finally block

    try:
        server_address = (config.HOST, config.TCP_PORT)
        server_socket.bind(server_address)
        # Listen for incoming connections, with a backlog queue of 1.
        # Backlog specifies the number of unaccepted connections that the
        # system will allow before refusing new connections.
        server_socket.listen(1)
        print(f"TCP server listening on {server_address}")
        print(f"Encryption active: {ENCRYPT}")

        # Initialize/clear log file at the start of a session
        try:
            with open(config.LOG_FILE_TCP_SERVER, 'w') as f:
                f.write("Timestamp,Direction,MessageID,Data\n")
        except IOError as e:
            print(f"Error initializing log file {config.LOG_FILE_TCP_SERVER}: {e}")
            # Server might choose to exit or continue without logging.

        print("Waiting for a client connection...")
        # accept() is a blocking call: it waits until a client connects.
        # It returns a new socket object (conn) for this specific connection
        # and the client's address (addr).
        conn, addr = server_socket.accept()
        print(f"Connection established from {addr}")

        packets_received_count: int = 0
        # The server typically runs indefinitely, handling client requests.
        # This loop breaks if the client disconnects or an error occurs.
        while True:
            # recv() is a blocking call: it waits for data from the client.
            # BUFFER_SIZE is the maximum amount of data to receive at once.
            data_received: bytes = conn.recv(config.BUFFER_SIZE)
            if not data_received:
                # An empty data_received means the client has closed the connection.
                print("Client disconnected.")
                break

            receive_timestamp: float = time.time()
            message_content: str
            payload: str

            if ENCRYPT and cipher_suite:
                try:
                    message_content = cipher_suite.decrypt(data_received).decode('utf-8')
                except InvalidToken:
                    print(f"Error: Failed to decrypt message. Token invalid (key mismatch or corrupted data). Data: {data_received[:50]}...")
                    message_content = f"ERROR_DECRYPT: {data_received[:50]}..."
                    payload = "DECRYPTION_ERROR" # Placeholder for payload
                except Exception as e:
                    print(f"Error decrypting message: {e}. Data: {data_received[:50]}...")
                    message_content = f"ERROR_DECRYPT: {data_received[:50]}..."
                    payload = "DECRYPTION_ERROR"
            else:
                message_content = data_received.decode('utf-8')

            # Assuming message format "GROUP_NAME-ID:Payload"
            # Split only on the first occurrence of ':' to correctly handle payloads containing colons.
            parts = message_content.split(':', 1)
            message_id_full: str = parts[0]
            if "ERROR_DECRYPT" not in message_id_full: # Avoid trying to parse if decryption failed
                 payload = parts[1] if len(parts) > 1 else "N/A_PAYLOAD"
            # else payload is already set to "DECRYPTION_ERROR" or similar

            print(f"Received (ID: {message_id_full}): '{payload}' from {addr}")
            log_message(config.LOG_FILE_TCP_SERVER, "RECEIVED", receive_timestamp, message_id_full, payload)
            packets_received_count += 1

            # Send ACK back to the client.
            # The ACK confirms receipt of the specific message_id.
            ack_message_str: str = f"ACK_FOR_{message_id_full}"
            ack_data_bytes: bytes = ack_message_str.encode('utf-8')

            if ENCRYPT and cipher_suite: # Encrypt ACKs if communication is encrypted
                ack_data_bytes = cipher_suite.encrypt(ack_data_bytes)

            conn.sendall(ack_data_bytes)
            # Server-side ACK sending is not typically logged in detail here,
            # as the client logs ACK reception which includes latency.

            # Server might check for a special "END_OF_METRICS" message if client sends one.
            # if "END_OF_METRICS" in message_id_full:
            #     print("End of metrics signal received. Server might reset for next client or terminate.")
            #     # For this example, the server continues until client disconnects.

    except socket.error as e:
        print(f"Socket error on server: {e}")
    except ConnectionResetError:
        # This common error occurs if the client closes the connection abruptly.
        print("Connection reset by client.")
    except KeyboardInterrupt:
        print("\nTCP Server is shutting down due to KeyboardInterrupt (Ctrl+C).")
    except Exception as e:
        print(f"An unexpected error occurred in the server: {e}")
    finally:
        # It's crucial to close sockets to release system resources.
        if conn:
            print("Closing client connection socket.")
            conn.close()
        print("Closing main server socket.")
        server_socket.close()
        print(f"Total packets processed by server in this session: {packets_received_count}")
        print("TCP server shut down.")

if __name__ == "__main__":
    main()