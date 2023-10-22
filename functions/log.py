



class Log:
    def __init__(self,folderName):
        self.folder = folderName
        self.visit = 'visit.log'
        self.signup = 'signup.log'
        self.login = 'login.log'
        self.taskAdded = 'taskAdded.log'
        self.studentAccept = 'studentAccept.log'
        self.teacherAccept = 'teacherAccept.log'
        self.finishLesson = 'finishLesson.log'

        self.home = './'

        
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
        

    def addAcceptStudentLog(self,teacherName,studentName,lessonName,time,state):
        with open(f'{self.home}{self.folder}{self.studentAccept}','a') as file:
            if state:
                file.write(f'The student {studentName} accepted teacher {teacherName} for lesson {lessonName} at {time}\n')
            else:
                file.write(f'The student {studentName} rejected teacher {teacherName} for lesson {lessonName} at {time}\n')

        

    def addFinishLog(self):
        pass



    




    def getAll(self):
        data = {}
        data['visitCount'] = getData(f'{self.home}{self.folder}{self.visit}')[0]
        data['loginNotification'] = getData(f'{self.home}{self.folder}{self.login}')
        data['signUpNotification'] = getData(f'{self.home}{self.folder}{self.signup}')
        data['lessonUploadNotification'] = getData(f'{self.home}{self.folder}{self.taskAdded}')
        data['studentAccepted'] = getData(f'{self.home}{self.folder}{self.studentAccept}')
        data['lessonAccepted'] = getData(f'{self.home}{self.folder}{self.teacherAccept}')
        data['finishLesson'] = getData(f'{self.home}{self.folder}{self.finishLesson}')

        return data







def getData(file):
    with open(file,'r') as file:
        data = file.readlines()
    return data








