import hashlib
import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import time


# 1. 生成RSA公私钥对
def generate_rsa_keypair(key_size=2048):
    """生成RSA公私钥对"""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )

    public_key = private_key.public_key()

    # 序列化为PEM格式
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return {
        'private_key': private_key,
        'public_key': public_key,
        'private_pem': private_pem,
        'public_pem': public_pem
    }


# 2. 模拟挖矿（工作量证明）
def mine_pow(nickname, difficulty=4, max_nonce=10000000):
    """模拟挖矿，找到符合条件的nonce"""
    target = '0' * difficulty

    for nonce in range(max_nonce):
        message = f"{nickname}:{nonce}"
        message_bytes = message.encode('utf-8')
        hash_result = hashlib.sha256(message_bytes).hexdigest()

        if hash_result.startswith(target):
            return {
                'nonce': nonce,
                'hash': hash_result,
                'message': message,
                'message_bytes': message_bytes
            }

    raise Exception(f"未能在 {max_nonce} 次尝试内找到符合条件的nonce")


# 3. 私钥签名
def sign_with_private_key(private_key, message_bytes):
    """使用私钥对消息进行RS256签名"""
    signature = private_key.sign(
        message_bytes,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return base64.b64encode(signature).decode('utf-8')


# 4. 公钥验签
def verify_with_public_key(public_key, message_bytes, signature_b64):
    """使用公钥验证签名"""
    try:
        signature = base64.b64decode(signature_b64)
        public_key.verify(
            signature,
            message_bytes,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False


# 主函数
def main():
    print("RSA非对称加密签名系统")
    print("=" * 40)

    # 1. 生成RSA公私钥对
    print("\n1. 生成RSA公私钥对")
    keypair = generate_rsa_keypair(2048)
    print("✓ 已生成2048位RSA密钥对")
    print(f"公钥长度: {len(keypair['public_pem'])} 字符")
    print(f"私钥长度: {len(keypair['private_pem'])} 字符")

    # 2. 模拟挖矿（工作量证明）
    print("\n2. 模拟挖矿（工作量证明）")
    nickname = "CryptoUser"
    difficulty = 4

    start_time = time.time()
    pow_result = mine_pow(nickname, difficulty)
    mining_time = (time.time() - start_time) * 1000  # 转换为毫秒

    print(f"✓ 挖矿成功! 耗时: {mining_time:.2f}ms")
    print(f"昵称: {nickname}")
    print(f"Nonce: {pow_result['nonce']}")
    print(f"消息: {pow_result['message']}")
    print(f"哈希值: {pow_result['hash']}")

    # 3. 私钥签名
    print("\n3. 私钥签名")
    signature = sign_with_private_key(keypair['private_key'], pow_result['message_bytes'])
    print("✓ 签名完成")
    print(f"签名(Base64): {signature[:50]}...")

    # 4. 公钥验签
    print("\n4. 公钥验签")
    is_signature_valid = verify_with_public_key(
        keypair['public_key'],
        pow_result['message_bytes'],
        signature
    )
    print(f"签名验证: {'成功' if is_signature_valid else '失败'}")

    print("\n" + "=" * 40)
    print("执行完成")
    print("=" * 40)

    print("\n结果摘要:")
    print(f"昵称: {nickname}")
    print(f"Nonce: {pow_result['nonce']}")
    print(f"哈希: {pow_result['hash']}")
    print(f"签名长度: {len(signature)} 字符")
    print(f"签名验证: {'✓ 成功' if is_signature_valid else '✗ 失败'}")


# 执行主函数
if __name__ == "__main__":
    main()