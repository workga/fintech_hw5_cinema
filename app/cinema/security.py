import bcrypt

def verify_password(stored: str, entered: str) -> bool:
    stored_b = stored.encode('utf-8')
    entered_b = entered.encode('utf-8')

    hashed_b = bcrypt.hashpw(entered_b, stored_b)

    return hashed_b == stored_b

def hash_password(entered: str) -> str:
    entered_b = entered.encode('utf-8')
    salt_b = bcrypt.gensalt()

    hashed_b = bcrypt.hashpw(entered_b, salt_b)

    return hashed_b.decode('utf-8')