import random, hashlib
def otp_gen():
    otp = f"{random.randint(100000, 999999)}"
    hashed = hashlib.sha256(otp.encode()).hexdigest()
    print(hashed)
    return hashed
