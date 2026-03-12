from hashlib import sha256
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

p = 10332921861938291919377635159012636040519117927041835671194203494937679183911345052843111512544303969800681115505917911462916407940308340306260755239268943
# Publiczny klucz Alicji z komunikacji
A = 8370337962458643162004582468469045984889816058567658904788530882468973454873284491037710219222503893094363658486261941098330951794393018216763327572120119
B = 9755909033513767641159594933585734179714892615169429957597029280980531443144704341694474385957669949989090202320232433789032328934018623049865998847328154

# Zaszyfrowana flaga z komunikacji
ciphertext = "PLCPttoNuN/dZyOWEQVpcu+ZPeKldvA+DqpBQgen9/loHpLKAzUQwL1NqD7TWO0ceGiOXVMk5z5KF1PGhdPUFg=="

g = 11

# Odzyskanie b % p
b_mod_p = g ^ B

# Shared secret zgodnie z kodem programu
shared_secret = str(A ^ b_mod_p)

# AES key
key = sha256(shared_secret.encode()).digest()

# Base64 decode
raw = b64decode(ciphertext)
iv = raw[:16]
ct = raw[16:]

cipher = AES.new(key, AES.MODE_CBC, iv)

plaintext = unpad(cipher.decrypt(ct), AES.block_size)

print("FLAG:", plaintext.decode())