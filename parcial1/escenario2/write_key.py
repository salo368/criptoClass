import os

from Crypto.Random import get_random_bytes

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Create the full path for the file
file_path = os.path.join(script_dir, "key")

# 32 bytes key
key = get_random_bytes(32)

with open(file_path, "wb") as f:
    f.write(key)
    