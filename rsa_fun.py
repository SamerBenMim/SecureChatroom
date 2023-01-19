import rsa

import cons

def getKeys(sender,receiver):
    MyKey = loadMyPrivateKey(sender)
    RKey = loadKeyReceiver(receiver)
    return MyKey , RKey

def generateKeys(login):
    (publicKey, privateKey) = rsa.newkeys(1024)
    print(publicKey)
    with open('RSA/public_keys/'+login+'.key', 'wb') as p:
        p.write(publicKey.save_pkcs1('PEM'))
    with open(cons.PRV_KEYS+login+'.key', 'wb') as p:
        p.write(privateKey.save_pkcs1('PEM'))

def loadKeyReceiver(login): # receiver's login
    with open('RSA/public_keys/'+login+'.key', 'rb') as p:
        publicKey = rsa.PublicKey.load_pkcs1(p.read())
    return publicKey

def loadMyPrivateKey(login): # sender's login
    with open(cons.PRV_KEYS+login+'.key', 'rb') as p:
        privateKey = rsa.PrivateKey.load_pkcs1(p.read())
    return privateKey

def encrypt(message, key):
    return rsa.encrypt(message.encode("UTF-8"), key)

def decrypt(ciphertext, key):
    try:
        return rsa.decrypt(ciphertext, key).decode("UTF-8")
    except:
        return False

