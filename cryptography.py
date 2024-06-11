from Crypto.Cipher import AES, DES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from codecarbon import track_emissions
import os

algorithm = ("AES", "DES", "RSA")[0]
key_size = {
    "AES": (16, 128, 192, 256),
    "DES": (8, 56),
    "RSA": (1024, 2048, 3072, 4096),
}.get(algorithm)[0]
file_to_encrypt = ("1MB", "100MB", "1GB")[2]
host = ("macbook_air_m2", "raspberry_pi_3B", "raspberry_pi_4")[0]

output_dir = f"./reports/{host}/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_file = f"emissions_{host}_{algorithm}_{key_size}_{file_to_encrypt}.csv"


def pad(data, block_size):
    padding_len = block_size - len(data) % block_size
    return data + bytes([padding_len] * padding_len)


def unpad(data):
    padding_len = data[-1]
    return data[:-padding_len]


@track_emissions(output_dir=output_dir, output_file=output_file)
def encrypt_file(file_path, key, algorithm="AES"):
    with open("files/" + file_path, "rb") as file:
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

    elif algorithm == "RSA":
        recipient_key = RSA.import_key(key)
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        ciphertext = cipher_rsa.encrypt(file_data)

    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

    with open("files/" + file_path + ".enc", "wb") as enc_file:
        enc_file.write(ciphertext)


@track_emissions(output_dir=output_dir, output_file=output_file)
def decrypt_file(file_path, key, algorithm="AES"):
    with open("files/" + file_path, "rb") as enc_file:
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

    elif algorithm == "RSA":
        private_key = RSA.import_key(key)
        cipher_rsa = PKCS1_OAEP.new(private_key)
        plaintext = cipher_rsa.decrypt(ciphertext)

    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

    with open("files/" + file_path[:-4], "wb") as dec_file:
        dec_file.write(plaintext)


if algorithm == "AES":
    aes_key = get_random_bytes(key_size)
    enc_key = aes_key
    dec_key = aes_key
elif algorithm == "DES":
    des_key = get_random_bytes(key_size)
    enc_key = des_key
    dec_key = des_key
elif algorithm == "RSA":
    rsa_key = RSA.generate(key_size)
    enc_key = rsa_key.export_key()
    dec_key = rsa_key.publickey().export_key()

encrypt_file(file_to_encrypt, enc_key, algorithm=algorithm)
print(f"File '{file_to_encrypt}' has been encrypted with {algorithm}.")

decrypt_file(file_to_encrypt + ".enc", dec_key, algorithm=algorithm)
print(f"File '{file_to_encrypt}.enc' has been decrypted with {algorithm}.")

# Codecarbon tracks Apple Silicon Chip energy consumption using powermetrics
if os.path.exists(output_dir + "powermetrics_log.txt"):
    log_file_name = (
        output_dir
        + f"powermetrics_log_{host}_{algorithm}_{key_size}_{file_to_encrypt}.txt"
    )
    os.rename(output_dir + "powermetrics_log.txt", log_file_name)
