from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def Create_Pairs(key_size: int = 2048) -> tuple[bytes, bytes]:
    """
    Tạo cặp khóa RSA định dạng PEM.

    Tham số:
        key_size: độ dài khóa (bit), mặc định 2048.

    Trả về:
        (public_pem, private_pem) dạng bytes.
        - public_pem: dùng để MÃ HÓA, có thể gửi công khai.
        - private_pem: dùng để GIẢI MÃ, phải giữ bí mật.
    """
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return public_pem, private_pem