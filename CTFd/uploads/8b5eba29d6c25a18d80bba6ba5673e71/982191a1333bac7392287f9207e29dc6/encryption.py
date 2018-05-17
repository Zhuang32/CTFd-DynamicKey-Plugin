from gmpy2 import is_prime
from os import urandom

def bytes_to_num(b):
	return int(b.encode('hex'), 16)
	
def num_to_bytes(n):
	b = hex(n)[2:-1]
	b = '0' + b if len(b)%2 == 1 else b
	return b.decode('hex')
	
def get_a_prime(l):
	random_seed = urandom(l)
	num = bytes_to_num(random_seed)
	while True:
		if is_prime(num):
			break
		num+=1
	return num

def encrypt(flag):
	p1 = get_a_prime(128)
        p2 = get_a_prime(128)
        n = p1*p2
        e = 0x1001
        p = bytes_to_num(flag)
	p = pow(p, e, n)
	return num_to_bytes(p).encode('hex')
        