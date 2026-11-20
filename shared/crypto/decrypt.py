from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def Decrypt(encrypted_package: bytes, private_pem: bytes, as_text: bool = False) -> bytes | str:
    """
    Giải mã gói tin do Encrypt() tạo ra, bằng Private Key của người nhận.

    Tham số:
        encrypted_package: gói bytes nhận được.
        private_pem: Private Key dạng PEM.
        as_text: True -> trả về str (chat), False -> trả về bytes (file).

    Lỗi:
        ValueError / InvalidTag nếu sai khóa hoặc dữ liệu bị sửa đổi.
    """
    private_key = serialization.load_pem_private_key(private_pem, password=None)

    # 1. Tách các phần của gói tin
    key_len = int.from_bytes(encrypted_package[:2], byteorder="big")
    encrypted_aes_key = encrypted_package[2 : 2 + key_len]
    nonce = encrypted_package[2 + key_len : 2 + key_len + 12]
    ciphertext = encrypted_package[2 + key_len + 12 :]

    # 2. RSA giải mã lấy khóa AES
    aes_key = private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    # 3. AES-GCM giải mã nội dung
    decrypted = AESGCM(aes_key).decrypt(nonce, ciphertext, None)
    return decrypted.decode("utf-8") if as_text else decrypted