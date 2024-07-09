import os

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.py'):
            with open(os.path.join(root, file), 'rb') as f:
                content = f.read()
                if b'\x00' in content:
                    print(f"Null byte found in {os.path.join(root, file)}")