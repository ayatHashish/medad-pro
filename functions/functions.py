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
        
        


class DB:
    def __init__(self,name):
        self.name = name
        with sqlite3.connect(self.name) as conn:
            try:
                conn.execute('''CREATE TABLE accounts
                            (email TEXT, username TEXT, password TEXT)''')
            except:
                __ = None
        
        
    def search(self, tofind, by = "email"):
        with sqlite3.connect(self.name) as conn:
            query = "SELECT * FROM accounts WHERE " + by + " = ?"
            result = conn.execute(query, (tofind,)).fetchone()
        return result #user tuple or none
        
        

    
    
            
    def __signup__(self,username,email,password):
        with sqlite3.connect(self.name) as conn:
            
          
            hpw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            data = {'email': email, 'username':username, 'password': hpw}
            conn.execute("INSERT INTO accounts VALUES ( :email, :username, :password)", data)
            conn.commit()
            

    

        
    def __login__(self,user,password):
    
        password = password.encode('utf-8')
        if bcrypt.checkpw(password, user[2]):
            return user
        
        return None
            
            

