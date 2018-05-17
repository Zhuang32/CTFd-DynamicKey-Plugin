import sys
import os  
from Crypto.Cipher import AES 
from binascii import b2a_hex, a2b_hex  
   
class prpcrypt():  
    def __init__(self, key):  
        self.key = key  
        self.mode = AES.MODE_CBC  
       
    def encrypt(self, text):  
        cryptor = AES.new(self.key, self.mode, self.key[-16:])
        length = 16  
        count = len(text)  
        if(count % length != 0) :  
            add = length - (count % length)  
        else:  
            add = 0  
        text = text + ('\0' * add)  
        self.ciphertext = cryptor.encrypt(text)
        return b2a_hex(self.ciphertext)  

    def decrypt(self, text):  
        cryptor = AES.new(self.key, self.mode, self.key[-16:])
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')

print("Welcome to PKUCTF!")
print('Please input your team token:')
sys.stdout.flush()
token = raw_input()
with open("master_flag.txt", 'r') as f:
    master_flag = f.read()
if master_flag[-1] == '\n':
   master_flag = master_flag[:-1]
try:
    pc = prpcrypt(token[-32:])
    flag = pc.encrypt(master_flag)
except Exception:
    print("Wrong team token!")
    exit(1)
team_name = "team_"+token[:8]
if not os.path.exists("/opt/jail/home/"+team_name):
    with open(team_name+"_flag", 'w') as f:
        f.write(flag)
    os.system("adduser --quiet --disabled-password --gecos 111 "+team_name)
    os.system("jk_jailuser -m -j /opt/jail/ "+team_name)
    os.system("cp "+team_name+"_flag /opt/jail/home/"+team_name+"/flag.txt")
    os.system("chown -R "+team_name+" /opt/jail/home/"+team_name)
    os.system("chmod 700 /opt/jail/home/"+team_name)
    with open("/opt/jail/etc/passwd", 'r') as f:
        old_content = f.readlines()
    replace_index = old_content[-1].rindex('/usr/sbin/jk_lsh')
    old_content[-1] = old_content[-1][:replace_index]+"/bin/bash\n"
    new_content = "".join(old_content)
    with open("/opt/jail/etc/passwd", 'w') as f:
        f.write(new_content)
os.system("su "+team_name+" -c ../../dev/pwn")
