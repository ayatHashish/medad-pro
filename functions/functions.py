import bcrypt
import sqlite3


class user:
    def __init__(self,name,pw,email):
        self.name = name
        self.pw = pw
        self.encpw = pw.encode('utf-8')
        self.hpw = bcrypt.hashpw(self.encpw, bcrypt.gensalt())
        self.email = email
        
        self.data = {'email': self.email, 'username':self.name, 'password': self.hpw}
        
        
        
        

def __signup__(username,email,password):
    conn = sqlite3.connect('users.db')
    try:
        conn.execute('''CREATE TABLE accounts
                    (email TEXT, username TEXT, password TEXT)''')
    except:
        __ = None
        
    query = "SELECT * FROM accounts WHERE email = ?"
    result = conn.execute(query, (email,)).fetchone()
    if result :
        conn.close()
        return 0
    
    else :
        new_user = user(username,password,email)    
        conn.execute("INSERT INTO accounts VALUES ( :email, :username, :password)", new_user.data)
        conn.commit()
        return 1

        
def __login__(email,password):
    conn = sqlite3.connect('users.db')
    
    #try:
    #    conn.execute('''CREATE TABLE accounts
    #               (username TEXT, email TEXT, password TEXT)''')
    #except:
    #    __ = None
        
    password = password.encode('utf-8')
    
    found_user = conn.execute("SELECT * FROM accounts WHERE email=?", (email,)).fetchone()
    if found_user :
        if bcrypt.checkpw(password, found_user[2]):
            print('Password is correct')
            return found_user
        else:
            print('Username or Password is incorrect')
    else :
        print('Username or Password is incorrect')
        
    return None
        
        
    conn.close()

