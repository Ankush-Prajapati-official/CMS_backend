from app.utils.password import hash_password, verify_password

hashed = hash_password("Ankush@123")

print("Hashed Password:", hashed)
print(
    "Password Match:",
    verify_password("Ankush@123", hashed)
)