from Crypto.Cipher import AES, DES
from Crypto.Random import get_random_bytes
from codecarbon import track_emissions
import os


def pad(data, block_size):
    padding_len = block_size - len(data) % block_size
    return data + bytes([padding_len] * padding_len)


def unpad(data):
    padding_len = data[-1]
    return data[:-padding_len]


host = ("macbook_air_m2", "raspberry_pi_3B", "raspberry_pi_4")[0]

output_dir = f"./reports/{host}/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

algorithm = ("AES", "DES")[0]
KEY_SIZE = {
    "AES": (128, 192, 256),
    "DES": [64],
}.get(algorithm)
FILE_SIZE = (
    "1MB",
    "10MB",
    "25MB",
    "50MB",
    "75MB",
    "100MB",
    "250MB",
    "500MB",
    "750MB",
    "1GB",
    "2GB",
    "5GB",
)

FILES_DIR = "files/"

for key_size in KEY_SIZE:
    for file_size in FILE_SIZE:
        output_file = f"emissions_{host}_{algorithm}_{key_size}_{file_size}.csv"

        @track_emissions(output_dir=output_dir, output_file=output_file)
        def encrypt_file(file_path, key, algorithm="AES"):
            with open(FILES_DIR + file_path, "rb") as file:
                file_data = file.read()

            if algorithm == "AES":
                padded_data = pad(file_data, AES.block_size)
                iv = get_random_bytes(AES.block_size)
                cipher = AES.new(key, AES.MODE_CBC, iv)
                ciphertext = iv + cipher.encrypt(padded_data)

            elif algorithm == "DES":
                padded_data = pad(file_data, DES.block_size)
                iv = get_random_bytes(DES.block_size)
                cipher = DES.new(key, DES.MODE_CBC, iv)
                ciphertext = iv + cipher.encrypt(padded_data)

            else:
                raise ValueError(f"Unsupported algorithm: {algorithm}")

            with open(FILES_DIR + file_path + ".enc", "wb") as enc_file:
                enc_file.write(ciphertext)

        @track_emissions(output_dir=output_dir, output_file=output_file)
        def decrypt_file(file_path, key, algorithm="AES"):
            with open(FILES_DIR + file_path, "rb") as enc_file:
                ciphertext = enc_file.read()

            if algorithm == "AES":
                iv = ciphertext[: AES.block_size]
                actual_ciphertext = ciphertext[AES.block_size :]
                cipher = AES.new(key, AES.MODE_CBC, iv)
                padded_plaintext = cipher.decrypt(actual_ciphertext)
                plaintext = unpad(padded_plaintext)

            elif algorithm == "DES":
                iv = ciphertext[: DES.block_size]
                actual_ciphertext = ciphertext[DES.block_size :]
                cipher = DES.new(key, DES.MODE_CBC, iv)
                padded_plaintext = cipher.decrypt(actual_ciphertext)
                plaintext = unpad(padded_plaintext)

            else:
                raise ValueError(f"Unsupported algorithm: {algorithm}")

            with open(FILES_DIR + file_path[:-4], "wb") as dec_file:
                dec_file.write(plaintext)

        if algorithm == "AES":
            aes_key = get_random_bytes(key_size // 8)
            enc_key = aes_key
            dec_key = aes_key
        elif algorithm == "DES":
            des_key = get_random_bytes(key_size // 8)
            enc_key = des_key
            dec_key = des_key

        encrypt_file(file_size, enc_key, algorithm=algorithm)
        print(f"File '{file_size}' has been encrypted with {algorithm}-{key_size}.")

        decrypt_file(file_size + ".enc", dec_key, algorithm=algorithm)
        print(f"File '{file_size}.enc' has been decrypted with {algorithm}-{key_size}.")

        # Codecarbon tracks Apple Silicon Chip energy consumption using powermetrics
        if os.path.exists(output_dir + "powermetrics_log.txt"):
            log_file_name = (
                output_dir
                + f"powermetrics_log_{host}_{algorithm}_{key_size}_{file_size}.txt"
            )
            os.rename(output_dir + "powermetrics_log.txt", log_file_name)
