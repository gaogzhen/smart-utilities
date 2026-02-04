import hashlib
import random
from typing import Tuple
import base64


class RSAKeyPair:
    def __init__(self, key_size: int = 2048):
        """
        RSA密钥对生成类
        key_size: 密钥长度，推荐2048位以上
        """
        self.key_size = key_size
        self.public_key, self.private_key = self._generate_keypair()

    def _generate_keypair(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """
        生成RSA公私钥对
        返回: (公钥(n, e), 私钥(n, d))
        """

        # 生成两个大素数
        def is_prime(n, k=5):
            """Miller-Rabin素性测试"""
            if n < 2:
                return False
            for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
                if n % p == 0:
                    return n == p

            # 分解 n-1 = 2^s * d
            s = 0
            d = n - 1
            while d % 2 == 0:
                s += 1
                d //= 2

            # 进行k次测试
            for _ in range(k):
                a = random.randrange(2, n - 1)
                x = pow(a, d, n)
                if x == 1 or x == n - 1:
                    continue
                for _ in range(s - 1):
                    x = pow(x, 2, n)
                    if x == n - 1:
                        break
                else:
                    return False
            return True

        def generate_prime(bits):
            """生成指定位数的大素数"""
            while True:
                p = random.getrandbits(bits)
                # 确保是奇数且足够大
                p |= (1 << bits - 1) | 1
                if is_prime(p):
                    return p

        # 生成两个大素数
        p = generate_prime(self.key_size // 2)
        q = generate_prime(self.key_size // 2)

        # 确保p和q不相等
        while p == q:
            q = generate_prime(self.key_size // 2)

        # 计算n和φ(n)
        n = p * q
        phi = (p - 1) * (q - 1)

        # 选择公钥指数e，通常为65537
        e = 65537
        while phi % e == 0:
            e += 2

        # 计算私钥指数d (d = e^-1 mod φ(n))
        def extended_gcd(a, b):
            """扩展欧几里得算法求逆元"""
            if b == 0:
                return (1, 0, a)
            x1, y1, gcd = extended_gcd(b, a % b)
            x = y1
            y = x1 - (a // b) * y1
            return (x, y, gcd)

        d, _, gcd = extended_gcd(e, phi)
        d = d % phi
        if d < 0:
            d += phi

        # 返回公私钥对
        public_key = (n, e)
        private_key = (n, d)

        return public_key, private_key

    def get_public_key_hex(self) -> str:
        """获取十六进制格式的公钥"""
        n, e = self.public_key
        return f"n={hex(n)[2:]}, e={hex(e)[2:]}"

    def get_private_key_hex(self) -> str:
        """获取十六进制格式的私钥"""
        n, d = self.private_key
        return f"n={hex(n)[2:]}, d={hex(d)[2:]}"


class RSASignature:
    def __init__(self, key_pair: RSAKeyPair):
        self.key_pair = key_pair

    def sign(self, message: bytes) -> bytes:
        """
        使用私钥对消息进行签名
        """
        n, d = self.key_pair.private_key

        # 对消息进行哈希
        hash_value = hashlib.sha256(message).digest()

        # 将哈希值转换为整数
        m = int.from_bytes(hash_value, 'big')

        # 确保m < n
        m = m % n

        # 使用私钥签名: s = m^d mod n
        signature = pow(m, d, n)

        # 将签名转换为字节
        signature_bytes = signature.to_bytes((signature.bit_length() + 7) // 8, 'big')

        return signature_bytes

    def verify(self, message: bytes, signature: bytes) -> bool:
        """
        使用公钥验证签名
        """
        n, e = self.key_pair.public_key

        # 将签名转换为整数
        s = int.from_bytes(signature, 'big')

        # 使用公钥验证: m' = s^e mod n
        m_prime = pow(s, e, n)

        # 对原始消息进行哈希
        hash_value = hashlib.sha256(message).digest()
        m_original = int.from_bytes(hash_value, 'big') % n

        # 比较结果
        return m_prime == m_original


class ProofOfWork:
    @staticmethod
    def find_nonce(nickname: str, difficulty: int = 4) -> Tuple[int, str]:
        """
        工作量证明：找到符合条件的nonce
        difficulty: 哈希值前导0的数量
        """
        target_prefix = '0' * difficulty
        nonce = 0

        while True:
            # 构造消息: 昵称 + nonce
            message = f"{nickname}{nonce}"
            message_bytes = message.encode('utf-8')

            # 计算哈希值
            hash_result = hashlib.sha256(message_bytes).hexdigest()

            # 检查是否满足条件
            if hash_result.startswith(target_prefix):
                return nonce, hash_result

            nonce += 1

    @staticmethod
    def verify_pow(nickname: str, nonce: int, difficulty: int = 4) -> bool:
        """验证工作量证明"""
        target_prefix = '0' * difficulty
        message = f"{nickname}{nonce}"
        hash_result = hashlib.sha256(message.encode('utf-8')).hexdigest()
        return hash_result.startswith(target_prefix)


def main():
    # 1. 生成RSA公私钥对
    print("=" * 60)
    print("步骤1: 生成RSA公私钥对")
    print("=" * 60)
    key_pair = RSAKeyPair(key_size=1024)  # 实际使用建议2048位以上

    print(f"公钥(n, e):")
    print(f"  n: {key_pair.public_key[0]}")
    print(f"  e: {key_pair.public_key[1]}")
    print()
    print(f"私钥(n, d):")
    print(f"  n: {key_pair.private_key[0]}")
    print(f"  d: {key_pair.private_key[1]}")
    print()

    # 2. 工作量证明
    print("=" * 60)
    print("步骤2: 进行工作量证明(POW)")
    print("=" * 60)
    nickname = "CryptoMaster"
    difficulty = 4  # 要求哈希值以4个0开头

    print(f"昵称: {nickname}")
    print(f"难度: 哈希值以{difficulty}个0开头")
    print("正在寻找nonce...")

    nonce, hash_result = ProofOfWork.find_nonce(nickname, difficulty)

    print(f"找到符合条件的nonce: {nonce}")
    print(f"完整消息: {nickname}{nonce}")
    print(f"SHA-256哈希值: {hash_result}")
    print()

    # 3. 使用私钥签名
    print("=" * 60)
    print("步骤3: 使用私钥对消息进行签名")
    print("=" * 60)

    rsa_signature = RSASignature(key_pair)
    message = f"{nickname}{nonce}"
    message_bytes = message.encode('utf-8')

    signature = rsa_signature.sign(message_bytes)
    print(f"原始消息: {message}")
    print(f"签名(十六进制): {signature.hex()}")
    print(f"签名(Base64): {base64.b64encode(signature).decode()}")
    print()

    # 4. 使用公钥验证签名
    print("=" * 60)
    print("步骤4: 使用公钥验证签名")
    print("=" * 60)

    is_valid = rsa_signature.verify(message_bytes, signature)
    print(f"签名验证结果: {'✓ 验证成功' if is_valid else '✗ 验证失败'}")
    print()

    # 5. 验证篡改后的消息
    print("=" * 60)
    print("步骤5: 验证篡改后的消息")
    print("=" * 60)

    tampered_message = f"{nickname}{nonce + 1}"  # 篡改nonce
    tampered_bytes = tampered_message.encode('utf-8')

    is_valid_tampered = rsa_signature.verify(tampered_bytes, signature)
    print(f"篡改后消息: {tampered_message}")
    print(f"使用原始签名验证: {'✓ 验证成功' if is_valid_tampered else '✗ 验证失败（预期结果）'}")
    print()

    # 6. 验证POW
    print("=" * 60)
    print("步骤6: 验证工作量证明")
    print("=" * 60)

    pow_valid = ProofOfWork.verify_pow(nickname, nonce, difficulty)
    print(f"POW验证结果: {'✓ 验证成功' if pow_valid else '✗ 验证失败'}")


if __name__ == "__main__":
    main()