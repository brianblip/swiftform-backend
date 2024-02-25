import os

# Create a dummy file of size 9MB
with open("dummy_file.txt", "wb") as f:
    f.write(os.urandom(1024 * 1024 * 9))  # 9MB
