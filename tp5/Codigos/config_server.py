#!/usr/bin/env python3
# config_server.py

"""
Configuration settings for the server applications (TCP and UDP).

This file centralizes all configurable parameters for the server-side
scripts, making it easier to adjust settings without modifying the
main application logic.
"""

# --- Network Configuration ---
# HOST: The IP address the server will bind to.
# '0.0.0.0' makes the server listen on all available network interfaces
# on the machine. This is typical for servers.
# If running on a specific interface, you can specify its IP address.
HOST: str = '0.0.0.0'

TCP_PORT: int = 12345         # Port number for the TCP server to listen on.
UDP_PORT: int = 12346         # Port number for the UDP server to listen on.
BUFFER_SIZE: int = 1024       # Maximum amount of data to be received in one go (bytes).
                              # Should generally match the client's buffer size.

# --- Application Specific Configuration ---
# These are generally mirrored from client config for consistency if needed by server logic,
# or define server-specific behavior.
GROUP_NAME: str = "NoLoSonIEEE" # Identifier for the group, used for message validation/logging.
NUM_PACKETS_METRICS: int = 100  # Expected number of packets for metrics (can be for server-side tracking if needed).
# SEND_INTERVAL_SECONDS is primarily a client-side setting for send rate.

# --- Logging Configuration ---
# Log files will store timestamps, direction, message IDs, and data.
LOG_FILE_TCP_SERVER: str = "tcp_server_log.txt"
LOG_FILE_UDP_SERVER: str = "udp_server_log.txt"
# Client log file names (kept here for completeness, but primarily used by client-side config)
# LOG_FILE_TCP_CLIENT: str = "tcp_client_log.txt"
# LOG_FILE_UDP_CLIENT: str = "udp_client_log.txt"

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
# 4. Ensure the *exact same byte string* is used in `config_client.py`.
#
# WARNING: Keep this key secret. Anyone with this key can decrypt your messages.
ENCRYPTION_KEY: bytes = b'FQRtfOGLCtJeH3E31p6r4T-afiGzaiuRkbC8cVOEAlI=' # Replace with your securely generated key

