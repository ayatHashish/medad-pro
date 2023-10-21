



class Log:
    def __init__(self,folderName):
        self.folder = folderName
        self.visit = 'visit.log'
        self.signup = 'signup.log'
        self.login = 'login.log'
        self.taskAdded = 'taskAdded.log'
        self.studentAccept = 'studentAccept.log'

        self.home = './'
        #self.home = '/home/maged_khaled/workSpace/medadA/website/'

        
    def addVisitLog(self):
        with open(f'{self.home}{self.folder}{self.visit}','r') as file:
            count = file.read()
        count = int(count) + 1
        with open(f'{self.home}{self.folder}{self.visit}','w') as file:
            file.write(str(count))

    def addSignUpLog(self,email,time):
        with open(f'{self.home}{self.folder}{self.signup}','a') as file:
            file.write(f'New user use email: {email} made account at {time}\n')
        

    def addLoginLog(self,email,time):
        with open(f'{self.home}{self.folder}{self.login}','a') as file:
            file.write(f'The user with email: {email} logged at {time}\n')
        

    def addTaskLog(self,email,taskName,time):
        with open(f'{self.home}{self.folder}{self.taskAdded}','a') as file:
            file.write(f'The student with email: {email} added task with name {taskName} at {time}\n')
        
    def addAcceptTeacherLog(self,email,taskName,time):
        with open(f'{self.home}{self.folder}{self.teacherAccept}','a') as file:
            file.write(f'The teacher with email: {email} accepted task with id {taskName} at {time}\n')
        

    def addAcceptStudentLog(self,teacherName,studentName,time,state):
        with open(f'{self.home}{self.folder}{self.studentAccept}','a') as file:
            if state:
                file.write(f'The student {studentName} accepted teacher {teacherName} at {time}\n')
            else:
                file.write(f'The student {studentName} rejected teacher {teacherName} at {time}\n')

        

    def addFinishLog(self):
        pass
