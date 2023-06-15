import bcrypt


def get_hashed_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_bytes_password)


def get_hashed(plain_password):
    hashed_password = get_hashed_password(plain_password)
    return hashed_password