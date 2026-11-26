from __future__ import annotations

import os

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def Encrypt(data: str | bytes, public_pem: bytes) -> bytes:
    """
    Mã hóa dữ liệu (chuỗi chat hoặc bytes của file) bằng Public Key của người nhận.

    Cơ chế lai (hybrid): RSA-OAEP mã hóa khóa AES-256 ngẫu nhiên,
    AES-GCM mã hóa nội dung (nhanh, không giới hạn kích thước, chống sửa đổi).

    Cấu trúc gói trả về:
        [2 byte độ dài khóa RSA][khóa AES đã mã hóa RSA][12 byte nonce][ciphertext AES-GCM]
    """
    raw_data = data.encode("utf-8") if isinstance(data, str) else data
    public_key = serialization.load_pem_public_key(public_pem)

    # 1. Khóa AES ngẫu nhiên + nonce
    aes_key = AESGCM.generate_key(bit_length=256)
    nonce = os.urandom(12)

    # 2. Mã hóa nội dung bằng AES-GCM
    ciphertext = AESGCM(aes_key).encrypt(nonce, raw_data, None)

    # 3. Mã hóa khóa AES bằng RSA-OAEP
    encrypted_aes_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    # 4. Đóng gói
    key_len = len(encrypted_aes_key).to_bytes(2, byteorder="big")
    return key_len + encrypted_aes_key + nonce + ciphertext