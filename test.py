from flask import Flask, request, jsonify, render_template, redirect, url_for
import jwt
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

app = Flask(__name__)

HMAC_SECRET = 'supersecretkey'

RSA_PRIVATE_KEY = '''-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAuAUww9iFrB3Memmp/bPBBwlEn9frAag/43XO+UHyWshzE155
tuEy1gnk3zwwZ2JrMi9vMs4/LoVdC52kQbZOZBGqUxia/TD2Ax89IWTez1CXIbtX
jiHROnYn8uBS1MVqxbAIlA6N+/H7BcRXfNOAhWz6MBGr36LxwTEsiSSS/9cq8f11
EUjrChpAggUP6kFfza4czMpoiSp0yfofT2rJ9GURNLCOOVYYcbHHyMrFfnm4wM9d
WbQQiX7X2QfH9eSuUEwrsbB+/IPcV7TNV84YMR+xgOdUb6PGEgfbCZy3fem/Jbtp
LnaTnv4UrRad2K/H49g1C3vZMhSNz2fn6k05HwIDAQABAoIBABGTzVinsf0Cy6lV
tnsZVHLLm9Z41WXPIGslsaN1fSTWyMcs2wtw714qi8YXBbiaWgrtJP4BXV+gNYcK
g8oTE+HTHiXZz9QnfRhHP5uU+wNqe0Upk+9ro4SmDKLScpcIVG6Vpfwed8l9D7E5
U/IEcd5MzokQ5w3xjo4ZmFtxNulhBq4u5b5gayafgCwDG908r3+GakaxPqcLWapV
hVe6rB5eg6yt+84y9FvzuJ7YNA4tHCXz7R433GWR/7a6rvawHUEtMnSv6koVnbYV
XazttKyWHOxIEipZWAtZ5u262dMMRO5zNKUFnemBYCoaS+ueKndOl6gelPnMPgaa
HaYy2OECgYEA2UU5Sa8Ee4e29P7RKigpYR/omAG2iIBydlkCkQa+lqhCwv4upiF2
0th850ebKNKj85Z3oemBu0GVaNukaPUkc/El72/aUnCnzqjmFVKoFctuKom3Ac1y
aBNDIneCnpPraxeZ4v+lahke0B2w7MmRu9NvIm+lDaj9kvosKU4g4x0CgYEA2NKm
5Fa6egR83Mo5oLbIyvq9GkIupZ/yXMHO1ojLczbC2xY298oPQl8iCsQ4Kb3xz4JY
QssbKWImZU8USydkoGRImhL0zhRziQh8cuVwiReNem+KrncxGxAxFIRJ4WIjTEF9
Kj4Z1aSna1l6teNbTcMogGwlbnGl9FZKdNLJvGsCgYEAwK5rR7U2vHZ3An6Y8FH9
oGyz0VpzjkqbN+loJUVd8C34RwU0SZCT2Bi1bEZMi7+CNpvSLHzw2CgpYHypKYt9
cHUDt3vymfneV5/hrDdJaUqnwIGxEqAoPbQXbZGe/RMhTC/6AR3GjHkKonYyWUvJ
OlEf1eI89ghQGPBUCa2H7OECgYA1pVEDl+3FeMzH+ATwHalqh0U4dP2DnyJhDta1
P91OoVLuz/1Dq6vA2TbcARaARW3J0M8zn3sV7yHe2QUFXzbHdGh+LoiBYJABbKcV
6mzAjqJDk8t1RSpSLtxl3iFFcXmYSW/Fft33fSirJ9VzoVAa2llwBNHyFI5h+OOt
KeYeBwKBgGVPLeLBARBULMIH4F6yzJdRugf3VwFRnKGm5aLmwo3EbfGfRxU4gpeU
OLmtlPwixslAJQAxyltwgoYBeMzi2iw0wGl2SW1xsCdPFnqBuTgybOibVOnlh1BP
vl7EjiJCA3iB2QAxeo7qBO/5QV5tW1b9VC3K5RvuTjFDed9pQHha
-----END RSA PRIVATE KEY-----
'''

RSA_PUBLIC_KEY = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuAUww9iFrB3Memmp/bPB
BwlEn9frAag/43XO+UHyWshzE155tuEy1gnk3zwwZ2JrMi9vMs4/LoVdC52kQbZO
ZBGqUxia/TD2Ax89IWTez1CXIbtXjiHROnYn8uBS1MVqxbAIlA6N+/H7BcRXfNOA
hWz6MBGr36LxwTEsiSSS/9cq8f11EUjrChpAggUP6kFfza4czMpoiSp0yfofT2rJ
9GURNLCOOVYYcbHHyMrFfnm4wM9dWbQQiX7X2QfH9eSuUEwrsbB+/IPcV7TNV84Y
MR+xgOdUb6PGEgfbCZy3fem/JbtpLnaTnv4UrRad2K/H49g1C3vZMhSNz2fn6k05
HwIDAQAB
-----END PUBLIC KEY-----'''

ADMIN_USER = 'admin'
ADMIN_PASS = 'password'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == ADMIN_USER and password == ADMIN_PASS:
            token = generate_jwt(username, role='admin', algorithm='RS256')
            return jsonify({'message': 'Welcome Admin', 'token': token})

        token = generate_jwt(username, role='user', algorithm='HS256')
        return jsonify({'message': 'Login successful', 'token': token})
    
    return render_template('login.html')

@app.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing'}), 403

    try:
        try:
            payload = jwt.decode(token, RSA_PUBLIC_KEY, algorithms=['RS256'])
        except jwt.InvalidSignatureError:
            payload = jwt.decode(token, HMAC_SECRET, algorithms=['HS256'])

        if payload.get('role') == 'admin':
            return jsonify({'message': 'Welcome Admin, you have access to the secret data!'})

        return jsonify({'message': 'Hello User, you do not have access to this data'})
    
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 403
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 403

def generate_jwt(username, role, algorithm):
    payload = {
        'username': username,
        'role': role,
        'exp': datetime.utcnow() + timedelta(minutes=5)
    }
    
    if algorithm == 'HS256':
        token = jwt.encode(payload, HMAC_SECRET, algorithm='HS256')
    elif algorithm == 'RS256':
        private_key = serialization.load_pem_private_key(
            RSA_PRIVATE_KEY.encode(),
            password=None,
            backend=default_backend()
        )
        token = jwt.encode(payload, private_key, algorithm='RS256')

    return token

if __name__ == '__main__':
    app.run(debug=True)
