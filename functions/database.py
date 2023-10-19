import hashlib
import sqlite3
import os 
import shutil

#course state : 
# 0 >> not accepted by any teacher 
# 1 >> accepted by one or more teacher 
# 2 >> student choose one teacher
# 3 >> admin accepted the course 
class DataBase:
    def __init__(self,name):
        self.home = './'
        self.home = '/home/maged_khaled/workSpace/medadA/website/'
        self.name = f"{self.home}database/{name}"
        
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
                SET state = ?
                WHERE id = ?
            '''
            
            cursor.execute(update_query, (new_data['state'],new_data['lessonID']))
            conn.commit()


    def getStudentLessons(self,studentID):
        with sqlite3.connect(self.name) as conn:
            
            query = f"SELECT id,lessonLOC,date FROM lessons \
                        WHERE state = 0 AND studentID = ?;"
            lessonsNotAccepted = conn.execute(query, (studentID,)).fetchall()


            query = f"SELECT lessons.id,lessons.lessonLOC,teachers.username,lessons.date,teachers.id \
                    FROM lessons,teachers,'st-tch-ls'\
                    WHERE lessons.id = 'st-tch-ls'.lessonID AND \
                    teachers.id = 'st-tch-ls'.teacherID AND\
                    lessons.state = 1 AND lessons.studentID = ?;"
            lessonsAccepted = conn.execute(query, (studentID,)).fetchall()

            

            query = f"SELECT lessons.id,lessons.lessonLOC,teachers.username,lessons.date,lessons.roomName \
                    FROM lessons,teachers,'st-tch-ls'\
                    WHERE lessons.id = 'st-tch-ls'.lessonID AND \
                    teachers.id = 'st-tch-ls'.teacherID AND\
                    lessons.state = 2 AND lessons.studentID = ?;"
            readyLessons = conn.execute(query, (studentID,)).fetchall()

        lessonsAcceptedData = []
        lessonsNotAcceptedData = []
        readyLessonsData = []


        for lesson in lessonsNotAccepted:
            lessonName = lesson[1].split('/')[-1]
            lessonsNotAcceptedData.append({'lessonID':lesson[0],'lessonName':lessonName,'lessonLOC':lesson[1],'date':lesson[2]})
        
        for lesson in lessonsAccepted:
            lessonName = lesson[1].split('/')[-1]
            lessonsAcceptedData.append({'lessonID':lesson[0],'lessonName':lessonName,'lessonLOC':lesson[1],
                                        'teacherName':lesson[2],'date':lesson[3],'teacherID':lesson[4]})

        for lesson in readyLessons:
            lessonName = lesson[1].split('/')[-1]
            readyLessonsData.append({'lessonID':lesson[0],'lessonName':lessonName,'lessonLOC':lesson[1],
                                        'teacherName':lesson[2],'date':lesson[3],'roomName':lesson[4]})
            
        return lessonsAcceptedData,lessonsNotAcceptedData,readyLessonsData #user tuple or none


    def acceptLesson(self,data):
        with sqlite3.connect(self.name) as conn:
            query = f"DELETE FROM 'st-tch-ls'\
                        WHERE lessonID = ? AND teacherID != ? AND studentID = ?;"
            conn.execute(query, (data['lessonID'],data['teacherID'],data['studentID'],)).fetchall()


            query = f"UPDATE lessons SET state = 2, teacherID = ?, roomName = ? \
                    WHERE id = ?"
            conn.execute(query, (data['teacherID'],data['roomName'],data['lessonID'],)).fetchall()



    def rejectLesson(self,data):
        with sqlite3.connect(self.name) as conn:
            query = f"DELETE FROM 'st-tch-ls' \
                    WHERE lessonID = ? AND teacherID = ? AND studentID = ?;"
            conn.execute(query, (data['lessonID'],data['teacherID'],data['studentID'],)).fetchall()


            query = f"UPDATE lessons SET state = 0 \
                    WHERE state = 1 AND id NOT IN (SELECT lessonID from 'st-tch-ls')"
            conn.execute(query, ()).fetchall()


    def getRoomName(self,id):
        with sqlite3.connect(self.name) as conn:

            query = f"SELECT roomName FROM lessons \
                    where id = ?;"
            roomName = conn.execute(query, (id,)).fetchone()
        return roomName[0]



    def getLesson(self,id):
        with sqlite3.connect(self.name) as conn:

            query = f"SELECT l.lessonLOC, l.state,\
                l.date, l.roomName, s.email, s.username\
            from lessons as l, students as s \
            WHERE l.id = ? AND l.studentID = s.id;"

            data = conn.execute(query, (id,)).fetchone()

            lessonName = data[0].split('/')[-1]

            data = {'lessonName':lessonName,'lessonLoc':data[0],'state':data[1],
                    'date':data[2],'roomName':data[3],
                    'email':data[4],'username':data[5]}
        print('data: ',data)
        return data

        
