from jose import jwt
from dotenv import dotenv_values


def encode():
    env = dotenv_values("../.env")
    key = env['QDC_2D_ACCESS_TOKEN_SECRET']
    encoded = jwt.encode({'user_id': 231092888, 'task_id': 1642612066994}, key)
    print(encoded)

def decode():
    env = dotenv_values("../.env")
    key = env['QDC_2D_ACCESS_TOKEN_SECRET']

    payload = jwt.decode('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyMzEwOTI4ODgsInRhc2tfaWQiOjE2NDI2MTIwNjY5OTR9.RoMHJfXx5DSXAUxyVSgMFCVU-5W1-DwXSNhKC5kDPoM', key)
    print(payload)


if __name__ == '__main__':
    #encode()
    decode()
