# 模拟验证程序完整性
import hashlib

# 假设这是官方发布的"正确"哈希值
official_hash = "d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2"

# 我们计算本地文件的哈希
def calculate_file_hash(filename):
    with open(filename, 'rb') as f:
        content = f.read()
        return hashlib.sha256(content).hexdigest()

local_hash = calculate_file_hash('test_hash.py')
print(f"本地文件哈希: {local_hash}")
print(f"官方哈希:     {official_hash}")
print(f"是否一致: {'✅ 文件完整无误' if local_hash == official_hash else '❌ 文件可能被篡改！'}")
