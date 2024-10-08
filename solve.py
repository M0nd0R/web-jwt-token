from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Generate a 2048-bit private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Save the private key to a file
with open("private_key.pem", "wb") as private_file:
    private_file.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
    )

# Generate the public key from the private key
public_key = private_key.public_key()

# Save the public key to a file
with open("public_key.pem", "wb") as public_file:
    public_file.write(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )

print("RSA key pair generated and saved to 'private_key.pem' and 'public_key.pem'")







"""without public key just gave them public key"""