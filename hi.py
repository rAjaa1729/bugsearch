# import hashlib
from flask_bcrypt import Bcrypt  
# passcode="rajaprism"
# hashfun=hashlib.new("SHA256")
# hashfun.update(passcode.encode())
# hashed_password=hashfun.hexdigest()
# print(hashed_password)
# print(hashed_password=="fe5c70b64d3ca209c9b68d9195cbe0caf67403cb3f44b137fee1a5a328ec0655")
import bcrypt
password1="raja"
password2="raja"
hashed_password1 = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())
hashed_password2 = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())

# Verify the password
print(hashed_password1==hashed_password2)
if bcrypt.checkpw(password2.encode('utf-8'), hashed_password1):
    print("Password matches")
else:
    print("Password does not match")

