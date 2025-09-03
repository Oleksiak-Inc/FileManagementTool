import bcrypt, base64

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    hashed_b64 = base64.b64encode(hashed).decode('utf-8')
    return hashed_b64

def authenticate(password: str, stored_hash_b64: str) -> bool:
    """Check password against Base64-encoded stored hash"""
    stored_hash = base64.b64decode(stored_hash_b64.encode("utf-8"))
    return bcrypt.checkpw(password.encode("utf-8"), stored_hash)

if __name__ == "__main__":
    # Example usage
    stored = hash_password("ABC")
    print("Stored hash (Base64):", stored)

    if authenticate("ABC", stored):
        print("auth")
    else:
        print("notauth")