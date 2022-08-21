import jwt
def create_token(data: dict):
    encode_data = jwt.encode(payload=data, key="165248521", algorithm="HS256")
    return encode_data

def decode_token(token: str):
    try:
        decode_data = jwt.decode(jwt=token, key="165248521", algorithms="HS256")
        return decode_data
    except Exception as e:
        return None