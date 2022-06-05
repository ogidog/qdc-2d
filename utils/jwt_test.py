from datetime import datetime, timedelta

from jose import jwt
from dotenv import dotenv_values

# 'user_id': 231092888, 'task_id': 1642612066994
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyMzEwOTI4ODgsInRhc2tfaWQiOjE2NDI2MTIwNjY5OTQsImV4cCI6MTcwODQwNzY1Mn0.wxBo1k-U5M_zI7Ij-VLjg3d4z2DvrtLsHYYwpD2lnyw

# 'user_id': 231092888, 'task_id': 1642612066995
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyMzEwOTI4ODgsInRhc2tfaWQiOjE2NDI2MTIwNjY5OTUsImV4cCI6MTcwODQwNzU5Nn0.H6TmS4zTF30QXAVZz5S_DmtqAg1FHtnAA_qTILYaeG4

def encode():
    env = dotenv_values("../.env")
    key = env['QDC_2D_ACCESS_TOKEN_SECRET']
    expire = datetime.utcnow() + timedelta(hours=15000)
    encoded = jwt.encode({'user_id': 231092888, 'task_id': 1642612066994, "exp": expire}, key)
    print(encoded)

def decode():
    env = dotenv_values("../.env")
    key = env['QDC_2D_ACCESS_TOKEN_SECRET']

    payload = jwt.decode('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyMzEwOTI4ODgsInRhc2tfaWQiOjE2NDI2MTIwNjY5OTQsImV4cCI6MTcwODQwNzY1Mn0.wxBo1k-U5M_zI7Ij-VLjg3d4z2DvrtLsHYYwpD2lnyw', key)
    [user_id, task_id, exp] = [*payload.values()]
    print(payload)


if __name__ == '__main__':
    #encode()
    decode()
