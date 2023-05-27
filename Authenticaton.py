import streamlit_authenticator as stauth
import pickle 
from pathlib import Path

names=["niranjan","priyanka"]
usernames=["rahi","nira"]
passwords=["rahinira","rahinira"]

#hashmodule
hash_passwords=stauth.Hasher(passwords).generate()
'''file_path=Path(__file__).parent/"hashed_pw.pk1"
with file_path.open("wb") as file:
    pickle.dump(hash_passwords,file)'''

print(hash_passwords)
