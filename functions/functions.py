import hashlib
import sqlite3
import os 
import shutil

#course state : 
# 0 >> not accepted by any teacher 
# 1 >> accepted by one or more teacher 
# 2 >> student choose one teacher
# 3 >> admin accepted the course 
class dataBase:
    def __init__(self,name):
        self.home = './'
        self.home = '/home/maged_khaled/workSpace/medadA/website/'
        self.name = f"{self.home}database/{name}"
        # with sqlite3.connect(self.name) as conn:
        #     cur = conn.cursor()
        #     cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        #     tables = cur.fetchall()
            
        #     if ('students',) not in tables :
        #         conn.execute('''CREATE TABLE students
        #                     (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, username TEXT, password TEXT, phone TEXT, validation TEXT, Type_ TEXT DEFAULT students)''')
        #     if ('lessons',) not in tables :
        #         conn.execute('''CREATE TABLE lessons
        #                     (id INTEGER PRIMARY KEY AUTOINCREMENT, studentID INTEGER, teacherID INTEGER, lessonLOC TEXT, state TEXT, date TEXT, URL TEXT, coursType TEXT, roomName TEXT)''')
                
        #     if ('teachers',) not in tables :
        #         conn.execute('''CREATE TABLE teachers
        #         (id INTEGER PRIMARY KEY AUTOINCREMENT, 
        #         email TEXT, 
        #         username TEXT, 
        #         password TEXT, 
        #         phone TEXT, 
        #         validation TEXT, 
        #         Type_ TEXT DEFAULT 'teachers', 
        #         coursType TEXT)''')

        
    def search(self,table, tofind, by = "email"):
        with sqlite3.connect(self.name) as conn:
            query = "SELECT * FROM "+table+" WHERE "+by+" = ?"
            result = conn.execute(query, (tofind,)).fetchone()
        return result #user tuple or none
        
        

    def teacherLessons(self,toFind):
        with sqlite3.connect(self.name) as conn:
            query = f"SELECT c.studentID,c.teacherID,c.lessonID,l.lessonLOC,l.state,l.date,roomName\
                    FROM 'st-tch-ls' AS c, lessons AS l \
                    WHERE l.id = c.lessonID AND c.teacherID = ?"
            result = conn.execute(query, (toFind,)).fetchall()
        lessonData = []
        for lesson in result:
            lessonData.append({'studentID':lesson[0],'teacherID':lesson[1],'lessonID':lesson[2],
                    'lessonLOC':lesson[3],'state':lesson[4],
                    'date':lesson[5],'roomName':lesson[6]})
        
        return lessonData #user tuple or none
    
    def teacherNotLessons(self,toFind):
        with sqlite3.connect(self.name) as conn:
            query = f"SELECT * FROM lessons \
                        WHERE id not in (SELECT c.lessonID\
                        FROM 'st-tch-ls' AS c, lessons AS l\
                        WHERE l.id = c.lessonID AND c.teacherID = ?)\
                        AND state < 2"
            
            result = conn.execute(query, (toFind,)).fetchall()
        lessonData = []

        for lesson in result:
            lessonData.append({'studentID':lesson[1],'lessonID':lesson[0],
                    'lessonLOC':lesson[3],'state':lesson[4],
                    'date':lesson[5],'roomName':lesson[7]})
        
        return lessonData #user tuple or none
            
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
           
            
            os.makedirs(f'{self.home}static/Users_Data/{table}/{str(user[0])}/Pictures')
            os.makedirs(f'{self.home}static/Users_Data/{table}/{str(user[0])}/Lectures')
            shutil.copyfile(f'{self.home}static/images/avatar.png',f'{self.home}static/Users_Data/{table}/{str(user[0])}/Pictures/Personal_Pic.png')

            
            
            

    

        
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
            
    def addLesson(self,table,data):
        with sqlite3.connect(self.name) as conn:
            
            cursor = conn.cursor()
            
            
            columns = ', '.join(data.keys())
            placeholders = ':' + ', :'.join(data.keys())
            
            
            insert_query = f"INSERT INTO '{table}' ({columns}) VALUES ({placeholders})"
            cursor.execute(insert_query, data) 
            conn.commit()


    def get_all_table_data(self, table_name, condition =''):
        with sqlite3.connect(self.name) as conn:
            cursor = conn.cursor()
            if condition == '':
                cursor.execute(f"SELECT * FROM {table_name}")
            else:
                cursor.execute(f"SELECT * FROM {table_name} where {condition[0]} = '{condition[1]}'")
            all_data = cursor.fetchall()
            cursor.close()
        return all_data


    def editLesson(self, new_data):
        with sqlite3.connect(self.name) as conn:
            
            cursor = conn.cursor()
            
            update_query = f'''
                UPDATE lessons
                SET teacherID = ?,
                    state = ?,
                    roomName = ?
                WHERE id = ?
            '''
            
            cursor.execute(update_query, (new_data['teacherID'], new_data['state'],new_data['roomName'], new_data['lessonID']))
            conn.commit()


    def getStudentLessons(self,studentID):
        with sqlite3.connect(self.name) as conn:
        
            query = f"SELECT c.lessonID,c.teacherID,l.lessonLOC,t.email,l.date,l.state, l.roomName \
            FROM lessons AS l, 'st-tch-ls' AS c, teachers AS t\
            WHERE c.lessonID = l.id AND c.studentID = ? AND c.teacherID = t.id;"
            lessonsAccepted = conn.execute(query, (studentID,)).fetchall()

            query = f"SELECT * FROM lessons WHERE id not in (\
                SELECT lessonID FROM 'st-tch-ls' WHERE studentID = ?);"
            lessonsNotAccepted = conn.execute(query, (studentID,)).fetchall()

        lessonsAcceptedData = []
        lessonsNotAcceptedData = []

        for lesson in lessonsAccepted:
            lessonsAcceptedData.append({'teacherID':lesson[1],'lessonID':lesson[0],
                    'lessonLOC':lesson[2],'teacherEmail':lesson[3],'state':lesson[5],
                    'date':lesson[4],'roomName':lesson[6]})
            
        for lesson in lessonsNotAccepted:
            lessonsNotAcceptedData.append({'teacherID':lesson[2],'lessonID':lesson[0],
                    'lessonLOC':lesson[3],'teacherEmail':None,'state':lesson[4],
                    'date':lesson[5],'roomName':lesson[7]})
        
        return lessonsAcceptedData,lessonsNotAcceptedData #user tuple or none


        

