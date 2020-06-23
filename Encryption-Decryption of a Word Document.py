# Here we can encrypt a, for example, Word document using two different methods and decrypt it.

# Open my selected file: "First News File: The Australian Case":
file = open('R#_data.docx','rb')
content = file.read()
content

# Create new file to write original data into it:
file_out = open('New_R#_data.docx','wb')
doc = file_out.write(content)

# source: https://python-docx.readthedocs.io/en/latest/user/documents.html
# source: https://automatetheboringstuff.com/chapter13/



############################
### PART 1 - DATA DIGEST ###
############################

# Method 1: Using SHA 256 to Hash the file:
from Crypto.Hash import SHA256
hash_M1 = SHA256.new(data=content)
print(hash_M1.digest())
# b'\xf6\xddpY\xae\xb4R\xe6Hl\xc0W]Y]V?@y\x1fBL\xf3GS\xb6\xbc\x0e\xacax2'
print(hash_M1.hexdigest())
# f6dd7059aeb452e6486cc0575d595d563f40791f424cf34753b6bc0eac617832

# source: https://pycryptodome.readthedocs.io/en/latest/src/hash/sha256.html
# source: https://nitratine.net/blog/post/how-to-hash-files-in-python/

# Method 2: Using BLAKE2S to Hash the file:
from Crypto.Hash import BLAKE2s
hash_M2 = BLAKE2s.new(digest_bits=256)
hash_M2.update(content)
print(hash_M2.digest())
# b'\xa6\xd4\xd9c\x80mP\xd1\x88\xbd[\xbcm\xebYr{\xb9\x1fU\x0b\xdf\x9bc\xaf\x05\x80\xef8\x92\xa1\x81'
print(hash_M2.hexdigest())
# a6d4d963806d50d188bd5bbc6deb59727bb91f550bdf9b63af0580ef3892a181

# source: https://pycryptodome.readthedocs.io/en/latest/src/hash/blake2s.html
# source: https://nitratine.net/blog/post/how-to-hash-files-in-python/


################################
### PART 2 - DATA ENCRYPTION ###
################################

# Method 1: Encrypting using AES (CBC):
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

output_file = 'R#_AES.bin' # Output file
data = content # data doc
key = b'!SQS5342_LBO@S_B' # The key you generated

# Create cipher object and encrypt the data
cipher = AES.new(key, AES.MODE_CBC) # Create a AES cipher object with the key using the mode CBC
ciphered_data = cipher.encrypt(pad(data, AES.block_size)) # Pad the input data and then encrypt

file_out = open(output_file, "wb") # Open file to write bytes
file_out.write(cipher.iv) # Write the iv to the output file (will be required for decryption)
file_out.write(ciphered_data) # Write the varying length cipher text to the file (this is the encrypted data)
file_out.close()

# source: https://pycryptodome.readthedocs.io/en/latest/src/cipher/classic.html
# source: https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html
# source: https://nitratine.net/blog/post/python-encryption-and-decryption-with-pycryptodome/


# Method 2: Encrypting using CAST Mode:
from Crypto.Cipher import CAST
output_file = 'R#_CAST.bin'
data = content
key = b'!SQS5342_LBO@S_B'
cipher = CAST.new(key, CAST.MODE_OPENPGP)
plaintext = content
msg = cipher.encrypt(plaintext)

file_out = open(output_file, "wb") # Open file to write bytes
#file_out.write(cipher.iv) # Write the iv to the output file (will be required for decryption)
file_out.write(ciphered_data) # Write the varying length cipher text to the file (this is the encrypted data)
file_out.close()

# source: https://pycryptodome.readthedocs.io/en/latest/src/cipher/cast.html



################################
### PART 3 - DATA DECRYPTION ###
################################

# Method 1: Decrypting Using AES (CBC):
from Crypto.Util.Padding import unpad

input_file = 'R#_AES.bin' # Input file
key = b'!SQS5342_LBO@S_B' # The key used for encryption (do not store/read this from the file)

# Read the data from the file
file_in = open(input_file, 'rb') # Open the file to read bytes
iv = file_in.read(16) # Read the iv out - this is 16 bytes long
ciphered_data = file_in.read() # Read the rest of the data
file_in.close()

cipher = AES.new(key, AES.MODE_CBC, iv=iv)  # Setup cipher
original_data = unpad(cipher.decrypt(ciphered_data), AES.block_size) # Decrypt and then up-pad the result
file_out = open('R#_AES_decrypted.docx','wb')
doc1 = file_out.write(original_data)


assert content == original_data


# source: # https://nitratine.net/blog/post/python-encryption-and-decryption-with-pycryptodome/


# Method 2: Decrypting using CAST Mode:
input_file = 'R#_CAST.bin'
key = b'!SQS5342_LBO@S_B'
eiv = msg[:CAST.block_size+2]
ciphertext = msg[CAST.block_size+2:]
cipher = CAST.new(key, CAST.MODE_OPENPGP, eiv)
cast_D = cipher.decrypt(ciphertext)
file_out2 = open('R#_CAST_decrypted.docx','wb')
doc2 = file_out2.write(cast_D)

# source: https://pycryptodome.readthedocs.io/en/latest/src/cipher/cast.html



###########################################
### PART 4: Data Integrity Verification ###
###########################################


# Method 1: Using SHA 256 to Hash the Decrypted file:
from Crypto.Hash import SHA256
hash_D1 = SHA256.new(data=original_data) # from decryption
print(hash_D1.digest())
# Original file:
# b'\xf6\xddpY\xae\xb4R\xe6Hl\xc0W]Y]V?@y\x1fBL\xf3GS\xb6\xbc\x0e\xacax2'
# Decrypted file:
# b'\xf6\xddpY\xae\xb4R\xe6Hl\xc0W]Y]V?@y\x1fBL\xf3GS\xb6\xbc\x0e\xacax2'
print(hash_D1.hexdigest())
# Original file:
# f6dd7059aeb452e6486cc0575d595d563f40791f424cf34753b6bc0eac617832
# Decrypted file:
# f6dd7059aeb452e6486cc0575d595d563f40791f424cf34753b6bc0eac617832

# source: https://pycryptodome.readthedocs.io/en/latest/src/hash/hash.html


# Method 2: Using BLAKE2S to Hash the Decrypted file:
from Crypto.Hash import BLAKE2s
hash_D2 = BLAKE2s.new(digest_bits=256)
hash_D2.update(original_data)
print(hash_D2.digest())
# Original file:
# b'\xa6\xd4\xd9c\x80mP\xd1\x88\xbd[\xbcm\xebYr{\xb9\x1fU\x0b\xdf\x9bc\xaf\x05\x80\xef8\x92\xa1\x81'
# Decrypted file:
# b'\xa6\xd4\xd9c\x80mP\xd1\x88\xbd[\xbcm\xebYr{\xb9\x1fU\x0b\xdf\x9bc\xaf\x05\x80\xef8\x92\xa1\x81'
print(hash_D2.hexdigest())
# Original file:
# a6d4d963806d50d188bd5bbc6deb59727bb91f550bdf9b63af0580ef3892a181
# Decrypted:
# a6d4d963806d50d188bd5bbc6deb59727bb91f550bdf9b63af0580ef3892a181




