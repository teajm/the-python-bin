import secrets
import string

from datetime import datetime

def generatePassword(length):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    pwd = ''
    for i in range(length):
        pwd += ''.join(secrets.choice(alphabet))
    return pwd

def generateDate():
    now = datetime.now()
    return now.strftime("%m/%d/%Y")
    
def main():
    pwdLength = 16
    date = generateDate()
    password = generatePassword(pwdLength)
    print(password)
    password = date + " " + password
    
    with open('passwords.txt', 'a') as f:
        f.writelines(password)
        f.write('\n')
        
if __name__ == '__main__':
    main()