from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


password = "MySecretPassword123"

hashed = hash_password(password)

print("Hash:", hashed)
print("Valid:", verify_password(password, hashed))
print("Invalid:", verify_password("wrong-password", hashed))

token = create_access_token("test-user-123")

print("Token:", token)
print("Decoded:", decode_access_token(token))