# Import necessary modules from cryptography library
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.serialization import (Encoding,PrivateFormat,NoEncryption)

# Import custom module "cons"
import cons

# Define the function to generate a certificate request
def gen_cert_req(login,firstname):
    # Generate a private key using RSA encryption
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    # Create a certificate signing request builder
    builder = x509.CertificateSigningRequestBuilder()
    # Set the subject name of the certificate signing request
    builder = builder.subject_name(
        x509.Name([
            x509.NameAttribute(NameOID.SURNAME, u'LOGIN:'+login),
            x509.NameAttribute(NameOID.GIVEN_NAME,u''+firstname)
        ])
    )
    # Add a basic constraints extension to the certificate signing request
    builder = builder.add_extension(
        x509.BasicConstraints(ca=False,path_length=None),critical=True,
    )
    # Sign the certificate signing request using SHA256 hashing algorithm
    request = builder.sign(
        private_key, hashes.SHA256(), default_backend()
    )
    # Write the certificate signing request to a file in PEM format
    with open(cons.dest_req+'/'+login+'_req.csr','wb') as f:
        f.write(request.public_bytes(Encoding.PEM))
    # Write the private key to a file in PEM format
    with open(cons.dest_key_cert+'/'+login+'.key','wb') as f:
        f.write(private_key.private_bytes(Encoding.PEM,PrivateFormat.TraditionalOpenSSL,NoEncryption()))
