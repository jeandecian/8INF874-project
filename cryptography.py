from Crypto.Cipher import AES, ARC4, Blowfish, ChaCha20, DES, DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from codecarbon import track_emissions
from twofish import Twofish
import os
import xtea

host = ("macbook_air_m2", "raspberry_pi_3B", "raspberry_pi_4")[0]

output_dir = f"./reports/{host}/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

algorithm = ("3DES", "AES", "Blowfish", "ChaCha20", "DES", "RC4", "Twofish", "XTEA")[2]
KEY_SIZE = {
    "3DES": [128, 192],
    "AES": (128, 192, 256),
    "Blowfish": [32],
    "ChaCha20": [256],
    "DES": [64],
    "RC4": [40],
    "Twofish": (128, 192, 256),
    "XTEA": [128],
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

            if algorithm == "3DES":
                padded_data = pad(file_data, DES3.block_size)
                iv = get_random_bytes(DES3.block_size)
                cipher = DES3.new(key, DES3.MODE_CBC, iv)
                ciphertext = iv + cipher.encrypt(padded_data)

            elif algorithm == "AES":
                padded_data = pad(file_data, AES.block_size)
                iv = get_random_bytes(AES.block_size)
                cipher = AES.new(key, AES.MODE_CBC, iv)
                ciphertext = iv + cipher.encrypt(padded_data)

            elif algorithm == "Blowfish":
                padded_data = pad(file_data, Blowfish.block_size)
                iv = get_random_bytes(Blowfish.block_size)
                cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
                ciphertext = iv + cipher.encrypt(padded_data)

            elif algorithm == "ChaCha20":
                cipher = ChaCha20.new(key=key)
                ciphertext = cipher.nonce + cipher.encrypt(file_data)

            elif algorithm == "DES":
                padded_data = pad(file_data, DES.block_size)
                iv = get_random_bytes(DES.block_size)
                cipher = DES.new(key, DES.MODE_CBC, iv)
                ciphertext = iv + cipher.encrypt(padded_data)

            elif algorithm == "RC4":
                cipher = ARC4.new(key)
                ciphertext = cipher.encrypt(file_data)

            elif algorithm == "Twofish":
                tf = Twofish(key)
                padded_data = pad(file_data, 16)
                iv = get_random_bytes(16)
                ciphertext = iv
                for i in range(0, len(padded_data), 16):
                    block = padded_data[i : i + 16]
                    ciphertext += tf.encrypt(block)

            elif algorithm == "XTEA":
                cipher = xtea.new(key, mode=xtea.MODE_OFB)
                ciphertext = cipher.encrypt(pad(file_data, 8))

            else:
                raise ValueError(f"Unsupported algorithm: {algorithm}")

            with open(FILES_DIR + file_path + ".enc", "wb") as enc_file:
                enc_file.write(ciphertext)

        @track_emissions(output_dir=output_dir, output_file=output_file)
        def decrypt_file(file_path, key, algorithm="AES"):
            with open(FILES_DIR + file_path, "rb") as enc_file:
                ciphertext = enc_file.read()

            if algorithm == "3DES":
                iv = ciphertext[: DES3.block_size]
                actual_ciphertext = ciphertext[DES3.block_size :]
                cipher = DES3.new(key, DES3.MODE_CBC, iv)
                padded_plaintext = cipher.decrypt(actual_ciphertext)
                plaintext = unpad(padded_plaintext, DES3.block_size)

            elif algorithm == "AES":
                iv = ciphertext[: AES.block_size]
                actual_ciphertext = ciphertext[AES.block_size :]
                cipher = AES.new(key, AES.MODE_CBC, iv)
                padded_plaintext = cipher.decrypt(actual_ciphertext)
                plaintext = unpad(padded_plaintext, AES.block_size)

            elif algorithm == "Blowfish":
                iv = ciphertext[: Blowfish.block_size]
                actual_ciphertext = ciphertext[Blowfish.block_size :]
                cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
                padded_plaintext = cipher.decrypt(actual_ciphertext)
                plaintext = unpad(padded_plaintext, Blowfish.block_size)

            elif algorithm == "ChaCha20":
                nonce = ciphertext[:8]
                actual_ciphertext = ciphertext[8:]
                cipher = ChaCha20.new(key=key, nonce=nonce)
                plaintext = cipher.decrypt(actual_ciphertext)

            elif algorithm == "DES":
                iv = ciphertext[: DES.block_size]
                actual_ciphertext = ciphertext[DES.block_size :]
                cipher = DES.new(key, DES.MODE_CBC, iv)
                padded_plaintext = cipher.decrypt(actual_ciphertext)
                plaintext = unpad(padded_plaintext, DES.block_size)

            elif algorithm == "RC4":
                cipher = ARC4.new(key)
                plaintext = cipher.decrypt(ciphertext)

            elif algorithm == "Twofish":
                iv = ciphertext[:16]
                actual_ciphertext = ciphertext[16:]
                tf = Twofish(key)
                decrypted_data = b""
                for i in range(0, len(actual_ciphertext), 16):
                    block = actual_ciphertext[i : i + 16]
                    decrypted_data += tf.decrypt(block)
                plaintext = unpad(decrypted_data, 16)

            elif algorithm == "XTEA":
                cipher = xtea.new(key, mode=xtea.MODE_OFB)
                plaintext = unpad(cipher.decrypt(ciphertext), 8)

            else:
                raise ValueError(f"Unsupported algorithm: {algorithm}")

            with open(FILES_DIR + file_path[:-4], "wb") as dec_file:
                dec_file.write(plaintext)

        key = get_random_bytes(key_size // 8)

        encrypt_file(file_size, key, algorithm=algorithm)
        print(f"File '{file_size}' has been encrypted with {algorithm}-{key_size}.")

        decrypt_file(file_size + ".enc", key, algorithm=algorithm)
        print(f"File '{file_size}.enc' has been decrypted with {algorithm}-{key_size}.")

        # Codecarbon tracks Apple Silicon Chip energy consumption using powermetrics
        if os.path.exists(output_dir + "powermetrics_log.txt"):
            log_file_name = (
                output_dir
                + f"powermetrics_log_{host}_{algorithm}_{key_size}_{file_size}.txt"
            )
            os.rename(output_dir + "powermetrics_log.txt", log_file_name)
