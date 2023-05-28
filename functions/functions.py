import bcrypt
import sqlite3
import os

class DB:
    def __init__(self,name):
        self.name = "./database/"+name
        with sqlite3.connect(self.name) as conn:
            try:
                conn.execute('''CREATE TABLE accounts
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, username TEXT, password TEXT, phone TEXT)''')
                            
                
                
            except:
                __ = None
        
        
    def search(self, tofind, by = "email"):
        with sqlite3.connect(self.name) as conn:
            query = "SELECT * FROM accounts WHERE " + by + " = ?"
            result = conn.execute(query, (tofind,)).fetchone()
        return result #user tuple or none
        
        

    
    
            
    def __signup__(self,username,email,password):
        with sqlite3.connect(self.name) as conn:
            
            cursor = conn.cursor()
            hpw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            data = {'email': email, 'username':username, 'password': hpw, 'phone': None}
            columns = ', '.join(data.keys())
            placeholders = ':' + ', :'.join(data.keys())
            table_name = 'accounts'
            
            insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(insert_query, data) 
            conn.commit()
            
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            for table in tables:
                print(table[0])
            conn.commit()
            
            user = self.search( 1, by = "id")
            print('>>',user)
            print(data)
            os.makedirs('static/Users_Data'+'/'+str(user[0])+'/Pictures')
            os.makedirs('static/Users_Data'+'/'+str(user[0])+'/Lectures')
            
            
            
    #def _print_():
    #    with sqlite3.connect(self.name) as conn:
    

        
    def __login__(self,user,password):
    
        password = password.encode('utf-8')
        if bcrypt.checkpw(password, user[3]):
            return user
        
        return None
    
    def __edit__(self,user_email,new_data):
        with sqlite3.connect(self.name) as conn:
            cursor = conn.cursor()
            update_query = '''
                UPDATE accounts
                SET email = ?,
                    username = ?,
                    phone= ?
                WHERE email= ?
            '''
            email = new_data['email']
            name = new_data['name']
            phone = new_data['phone']
            
            cursor.execute(update_query, (email, name, phone, user_email))
            conn.commit()
            

