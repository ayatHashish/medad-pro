import hashlib
import sqlite3
import os 
import shutil

class dataBase:
    def __init__(self,name):
        self.name = "./database/"+name
        with sqlite3.connect(self.name) as conn:
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cur.fetchall()
            
            if ('students',) not in tables :
                conn.execute('''CREATE TABLE students
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, username TEXT, password TEXT, phone TEXT, validation TEXT, Type_ TEXT DEFAULT students)''')
            if ('teachers',) not in tables :
                conn.execute('''CREATE TABLE lessons
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, studentID INTEGER, teacherID INTEGER, lessonLOC TEXT, state TEXT, date TEXT, URL TEXT coursType TEXT)''')
                
            if ('lessons',) not in tables :
                conn.execute('''CREATE TABLE teachers
                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                email TEXT, 
                username TEXT, 
                password TEXT, 
                phone TEXT, 
                validation TEXT, 
                Type_ TEXT DEFAULT 'teachers', 
                coursType TEXT)''')

           
                
   
        
    def search(self,table, tofind, by = "email"):
        with sqlite3.connect(self.name) as conn:
            print(table)
            query = "SELECT * FROM "+table+" WHERE "+by+" = ?"
            result = conn.execute(query, (tofind,)).fetchone()
        return result #user tuple or none
        
        

    
    
            
    def __signup__(self,table,username,email,password,code):
        with sqlite3.connect(self.name) as conn:
            
            cursor = conn.cursor()
            hpw = hashlib.sha256(password.encode()).hexdigest()
            #hpw = password
            
            data = {'email': email, 'username':username, 'password': hpw, 'phone': None, 'validation': code}
            columns = ', '.join(data.keys())
            placeholders = ':' + ', :'.join(data.keys())
            
            
            insert_query = "INSERT INTO "+table+" ("+columns+") VALUES ("+placeholders+")"
            cursor.execute(insert_query, data) 
            conn.commit()
            
            
            
            
            user = self.search(table, email)
            print('>>',user)
            print(data)
            
            os.makedirs('static/Users_Data'+'/'+table+'/'+str(user[0])+'/Pictures')
            os.makedirs('static/Users_Data'+'/'+table+'/'+str(user[0])+'/Lectures')
            shutil.copyfile('static/images/avatar.png','static/Users_Data'+'/'+table+'/'+str(user[0])+'/Pictures/Personal_Pic.png')

            
            
            

    

        
    def __login__(self,table,user,password):
    
        password = hashlib.sha256(password.encode()).hexdigest()
        # if bcrypt_sha256.verify(password, user[3]):
        #     return user
        if password == user[3]:
            return user
        return None
    
    def __edit__(self,table,user,new_data):
        with sqlite3.connect(self.name) as conn:
            cursor = conn.cursor()
            print(user)
            print(new_data)
            if user[6] == 'students' :
                update_query = f'''
                    UPDATE {table}
                    SET email = ?,
                        username = ?,
                        phone= ?,
                        validation= ?
                    WHERE email= ?
                '''
                email = new_data['email']
                name = new_data['name']
                phone = new_data['phone']
                code = new_data['code'] 
                
                cursor.execute(update_query, (email, name, phone, code, user[1]))
                conn.commit()
            
                
            elif user[6] == 'teachers' :
                update_query = f'''
                    UPDATE {table}
                    SET email = ?,
                        username = ?,
                        phone= ?,
                        validation=?,
                        coursType=?
                    WHERE email= ?
                '''
                email = new_data['email']
                name = new_data['name']
                phone = new_data['phone']
                code = new_data['code']
                courseType = new_data['courseType']


                
                cursor.execute(update_query, (email, name, phone,code,courseType , user[1]))
                conn.commit()
            
    def addLesson(self,data):
        print(data)
        with sqlite3.connect(self.name) as conn:
            
            cursor = conn.cursor()
            
            
            columns = ', '.join(data.keys())
            placeholders = ':' + ', :'.join(data.keys())
            
            
            insert_query = "INSERT INTO lessons ("+columns+") VALUES ("+placeholders+")"
            print(insert_query)
            cursor.execute(insert_query, data) 
            conn.commit()


    import sqlite3

    def get_all_table_data(self, table_name):
        # Step 1: Connect to the SQLite database
        with sqlite3.connect(self.name) as conn:

            # Step 2: Create a cursor object to execute SQL queries
            cursor = conn.cursor()

            # Step 3: Execute a SELECT query to fetch all data from the table
            cursor.execute(f"SELECT * FROM {table_name}")

            # Step 4: Retrieve the data using the cursor
            all_data = cursor.fetchall()

            # Step 5: Close the cursor and the database connection
            cursor.close()


            return all_data



        

