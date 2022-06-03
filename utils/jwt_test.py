from datetime import datetime, timedelta

from jose import jwt
from dotenv import dotenv_values


def encode():
    env = dotenv_values("../.env")
    key = env['QDC_2D_ACCESS_TOKEN_SECRET']
    expire = datetime.utcnow() + timedelta(hours=15000)
    encoded = jwt.encode({'user_id': 231092888, 'task_id': 1642612066994, "exp": expire}, key)
    print(encoded)

def decode():
    env = dotenv_values("../.env")
    key = env['QDC_2D_ACCESS_TOKEN_SECRET']

    payload = jwt.decode('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyMzEwOTI4ODgsInRhc2tfaWQiOjE2NDI2MTIwNjY5OTQsImV4cCI6MTcwODIzMzQwNn0.b47wnRc9q9rhzQ6nUZuGKKKwqTnZb4HWqs2AOYg1gSM', key)
    [user_id, task_id, exp] = [*payload.values()]
    print(payload)


if __name__ == '__main__':
    #encode()
    decode()
