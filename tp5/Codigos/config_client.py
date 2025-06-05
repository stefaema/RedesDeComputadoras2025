#!/usr/bin/env python3
# config_client.py

"""
Configuration settings for the client applications (TCP and UDP).

This file centralizes all configurable parameters for the client-side
scripts, making it easier to adjust settings without modifying the
main application logic.
"""

# --- Network Configuration ---
# HOST: The IP address of the server the client will connect to.
# For testing on the same machine, 'localhost' or '127.0.0.1' can be used.
# For testing between different machines on the same network, use the
# server's local network IP address (e.g., '192.168.1.100').
HOST: str = '192.168.100.2'  # Example: Server's IP address

TCP_PORT: int = 12345         # Port number for the TCP server.
UDP_PORT: int = 12346         # Port number for the UDP server.
BUFFER_SIZE: int = 1024       # Maximum amount of data to be received in one go (bytes).
                              # Should generally match the server's buffer size.

# --- Application Specific Configuration ---
GROUP_NAME: str = "NoLoSonIEEE" # Identifier for the group, prepended to message IDs.
NUM_PACKETS_METRICS: int = 100  # Number of packets to send for performance metric calculation.
SEND_INTERVAL_SECONDS: float = 1.0 # Approximate interval between sending packets (in seconds).
                                 # This also affects the UDP client's ACK timeout.

# --- Logging Configuration ---
# Log files will store timestamps, direction, message IDs, data, and latencies.
LOG_FILE_TCP_CLIENT: str = "tcp_client_log.txt"
LOG_FILE_UDP_CLIENT: str = "udp_client_log.txt"
# Server log file names (kept here for completeness, but primarily used by server-side config)
# LOG_FILE_TCP_SERVER: str = "tcp_server_log.txt"
# LOG_FILE_UDP_SERVER: str = "udp_server_log.txt"


# --- Encryption Configuration ---
# ENCRYPTION_KEY: The secret key for Fernet symmetric encryption.
# This key MUST be the same for both the client and the server.
# It should be a byte string.
#
# How to generate and use the ENCRYPTION_KEY:
# 1. Run the `code_gene.py` script (e.g., `python code_gene.py`).
# 2. Copy the generated key (it will be a string).
# 3. Paste it here, ensuring it's a byte string (e.g., b'your_key_here==').
#    Example: ENCRYPTION_KEY = b'example_key_generated_by_fernet=='
# 4. Ensure the *exact same byte string* is used in `config_server.py`.
#
# WARNING: This is a sensitsive configuration. Keep this key secret.
ENCRYPTION_KEY: bytes = b'FQRtfOGLCtJeH3E31p6r4T-afiGzaiuRkbC8cVOEAlI=' # Replace with your securely generated key

