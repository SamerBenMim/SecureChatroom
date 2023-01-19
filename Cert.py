import cryptography
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes,serialization
import datetime
import uuid
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.x509 import NameOID

import cons


def gen_ca_cert_key():
    # Generate a new RSA private key
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    # Create a new certificate builder
    builder = x509.CertificateBuilder()

    # Set the certificate's subject
    builder = builder.subject_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u"myCA"),
    ]))

    # Set the certificate's issuer
    builder = builder.issuer_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u"myCA"),
    ]))

    # Set the certificate's public key
    builder = builder.public_key(private_key.public_key())

    # Set the certificate's serial number
    builder = builder.serial_number(x509.random_serial_number())

    # Set the certificate's validity period
    builder = builder.not_valid_before(datetime.datetime.today() - datetime.timedelta(days=1))
    builder = builder.not_valid_after(datetime.datetime.today() + datetime.timedelta(days=7))

    # Add the "CA" basic constraint
    builder = builder.add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)

    # Sign the certificate using the private key
    certificate = builder.sign(private_key, hashes.SHA256(), default_backend())

    # Write the certificate to disk
    with open(cons.dest_ca+"ca.crt", "wb") as f:
        f.write(certificate.public_bytes(serialization.Encoding.PEM))

    # Write the private key to disk
    with open(cons.dest_ca+"ca.key", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

def load_ca_cert_key():
    ca = x509.load_pem_x509_certificate(
        open(cons.dest_ca + 'ca.crt', 'rb').read(), default_backend())
    ca_key = serialization.load_pem_private_key(
        open(cons.dest_ca + 'ca.key', 'rb').read(), password=None, backend=default_backend())
    return ca , ca_key

def create_cert(path,login):
    # get the request
    csr = x509.load_pem_x509_csr(open(cons.dest_req+'/'+login+'_req.csr','rb').read(),default_backend())
    # get the CA certificate and key
    ca , ca_key = load_ca_cert_key()

    builder = x509.CertificateBuilder()
    builder = builder.subject_name(csr.subject)
    builder = builder.issuer_name(ca.subject)
    builder = builder.not_valid_before(datetime.datetime.today() - datetime.timedelta(days=1))
    builder = builder.not_valid_after(datetime.datetime.today() + datetime.timedelta(days=7))
    builder = builder.public_key(csr.public_key())
    builder = builder.serial_number(int(uuid.uuid4()))
    for ext in csr.extensions:
        builder = builder.add_extension(ext.value,ext.critical)

    certificateC = builder.sign(
        ca_key,
        hashes.SHA256(),
        default_backend()
    )

    with open(cons.dest_client_cert+'/'+login+'.crt','wb') as f:
        f.write(certificateC.public_bytes(serialization.Encoding.PEM))

def verif_cert(login):
    # get the CA certificate and key
    ca, ca_key = load_ca_cert_key()

    msg = ""
    # Load the certificate from a file
    with open(cons.dest_client_cert +'/'+login+'.crt', 'rb') as f:
        cert = x509.load_pem_x509_certificate(f.read(), default_backend())


    # Verify the certificate
    try:
        ca_key.public_key().verify(
            cert.signature,
            cert.tbs_certificate_bytes,
            padding.PKCS1v15(),
            cert.signature_hash_algorithm
        )
        msg = "The certificate is authentic"

    except cryptography.exceptions.InvalidSignature:
        msg = "The certificate is not authentic : attempted hack "
    return msg

