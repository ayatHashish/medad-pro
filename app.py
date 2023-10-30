from flask import Flask,request,redirect,render_template,session,url_for,jsonify
from functions.database import DataBase
from functions.mail_sender import sender
from functions.log import Log
import sys
import random
from datetime import datetime
from functions.api import Video
from werkzeug.utils import secure_filename


#*****************set server*****************
homeDir = './'
#homeDir = '/home/maged_khaled/workSpace/medadA/website/'
app = Flask(__name__)

# GOOGLE_CLIENT_ID = "361389956894-fikf8t93743htich35qalbib61kotq1q.apps.googleusercontent.com"
# GOOGLE_CLIENT_SECRET = "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"
# GOOGLE_REDIRECT_URI = "http://www.medadd.eu.com/logwithgoogleserver"
# GOOGLE_AUTHORIZATION_URI = "https://accounts.google.com/o/oauth2/auth"
# GOOGLE_TOKEN_URI = "https://oauth2.googleapis.com/token"
# GOOGLE_USER_INFO_URI = 'https://www.googleapis.com/oauth2/v3/userinfo'

@app.before_request 
def setDefaultValue():
    if 'user' not in session:
        session['user'] = None
    if not '.' in request.base_url:
        LOG.addVisitLog()


#*****************redirect url*****************
@app.route("/",methods = ['GET','POST'])
def main():
    print(session['user'])
    
    return render_template('home.html',result = session['user'])

@app.route("/home",methods = ['GET','POST'])
def home():
    return render_template("home.html", result = session['user'])

@app.route("/service")
def _services_():
    return render_template('services.html',result = session['user'])

@app.route("/teacher")
def _teacher_():
    return render_template('home.html',result = session['user'])

@app.route("/contactus")
def _contactus_():       
    return render_template('contact-us.html',result = session['user'])

@app.route("/profile")
def _profile_(state = ["","",""]):
    if (session['user'] != None) :
        if session['user'][6] == 'students':
            acceptedLessons,notAcceptedLessons,readyLessons,finishedLessons = DB.getStudentLessons(session['user'][0])

            acceptedLessons = sorted(acceptedLessons, key=lambda d: d['lessonID'], reverse=True)
            notAcceptedLessons = sorted(notAcceptedLessons, key=lambda d: d['lessonID'], reverse=True)
            readyLessons = sorted(readyLessons, key=lambda d: d['lessonID'], reverse=True)
            finishedLessons = sorted(finishedLessons, key=lambda d: d['lessonID'], reverse=True)
            
            return render_template('profile.html',state = state, result = session['user'], myAcceptedLessons = acceptedLessons, myNotAcceptedLessons = notAcceptedLessons, myReadyLessons = readyLessons, myFinishedLessons = finishedLessons)
        
        elif session['user'][6] =='teachers':
            myLessons = DB.teacherLessons(session['user'][0])
            courses = DB.teacherNotLessons(session['user'][0])
            


            coursesData = {}
            for course in courses :
                courseName = course['lessonLOC'].split('/')[-1]
                coursesData[courseName]=(course['lessonID'],course['lessonLOC'])

            myLessonData = {}
            for course in myLessons :
                courseName = course['lessonLOC'].split('/')[-1]
                myLessonData[courseName]=(course['lessonID'],course['lessonLOC'])
            

            return render_template('teacher.html',state = state, result = session['user'], courses=coursesData, myLessons = myLessonData)
    else :
        return render_template('sign-in.html',state = "")


@app.route("/login")
def _login_():
    if session['user'] != None :
        return render_template('home.html',result = session['user'])
    else :
        return render_template('sign-in.html', state = "")

@app.route("/signup")
def _signup_():
    if session['user'] != None :
        return render_template('home.html',result = session['user'])
    else :
        return render_template('sign-up.html', state = "")






#**************************************Functions**************************************

@app.route("/logout",methods = ['GET','POST']) #******************************logout***************************
def logout():
    session['user'] = None
    return render_template('home.html',result = None)


@app.route("/loginRequist",methods = ['GET','POST']) #******************************login***************************
def login():
    if request.method == 'POST':
        email = request.form['email']
        email = email.lower()
        password = request.form['password']
        # search for email in students and teachers table
        type_ = 'students'
        user = DB.search(type_,email)
        if not user :
            type_ = 'teachers'
            user = DB.search(type_,email) 
        if not user :
            return render_template('sign-in.html', state = 'This email is not exist')
        
        #make a login 
        user = DB.__login__(type_,user,password)
        if user :
            session['user'] = user
            LOG.addLoginLog(user[1],datetime.now())
            return(redirect('/profile'))
        return render_template('sign-in.html', state = 'The password is not correct')
    return render_template('sign-in.html', state = "")

        


    
    
@app.route("/signupRequist",methods = ['GET','POST']) #******************************signup***************************
def signup():
    if request.method == 'POST'  :
        name = request.form['username']
        password = request.form['password']
        email = request.form['email']
        email = email.lower()
        type_ = request.form['type']
        # check availability of the input data
        if 'agreeTS' not in request.form :
            return render_template('sign-up.html', state = "Please read and agree on Terms of Service and Privacy Policy")
        if name == None:
            return render_template('sign-up.html', state = "Please enter valide name")
        if email == None:
            return render_template('sign-up.html', state = "Please enter valide email")
        if password == None:
            return render_template('sign-up.html', state = "Please enter valide password")
        
        emailExist = DB.search('students',email,by='email')
        if not emailExist :
            emailExist = DB.search('teachers',email,by='email')

        if emailExist :
            return render_template('sign-up.html', state = "The email is exist please sign in if you have an account")
        
        emailValide = emailer.valide_email(email)
        if not emailValide :
            return render_template('sign-up.html', state = "Please Enter Valid Email")
        
        #Every thing is good ... create account
        code = random.randint(100000, 999999)
        message_ = {'To':email , 'title':'send config', 'message':'here is your code : '+str(code), 'attachment':None}
        #emailer.send(message_)
        DB.__signup__(type_,name, email, password,code)
        LOG.addSignUpLog(email,datetime.now())
        return render_template('sign-in.html', state = "")
        
        
        
    if session['user']!=None :
        return(redirect('/profile'))
    else :
        return render_template('sign-up.html', state = "")
    




@app.route("/contactusRequist", methods= ['GET','POST'])
def contactus():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        title = request.form['title']
        subject = request.form['subject']
        type_ = 'students'
        userData = session['user']

        # check availability of data
        if email == '':
            return render_template('contact-us.html', state = 'Please enter your email',result=userData)
        if password == '':
            return render_template('contact-us.html', state = 'Please enter your password',result=userData)
        if phone == '':
            return render_template('contact-us.html', state = 'Please enter your phone',result=userData)
        if title == '':
            return render_template('contact-us.html', state = 'Please enter a title for your message',result=userData)
        if subject == '':
            return render_template('contact-us.html', state = 'Please enter the details of yout message',result=userData)
        
        type_ = 'students'
        user = DB.search(type_,email)
        if not user :
            type_ = 'teachers'
            user = DB.search(type_,email)
            
        if not user :
            return render_template('contact-us.html', state = 'Email is not correct',result=userData)

        #try to login
        user = DB.__login__(type_,user,password)
        if user :
            TMessage = "Hi Admin" + "\n\n" + subject +"\n\n\n" + "here is my email and phone number \n" + phone +"\n" + email
            message_ = {'To':emailer.Admin, 'title':title, 'message':TMessage, 'attachment':None }
            emailer.send(message_)
            return render_template('contact-us.html', state = 'Your Message sent successfully to Admin',result=userData)

        return render_template('contact-us.html', state = 'password is not correct',result=userData)
        

    return redirect("/contactus")

@app.route("/update_profile",methods = ['GET','POST'])
def Update_Profile():
    if request.method == 'POST':
        emailChangeFlag = False
        code = session['user'][5]
        email = request.form['email']
        email = email.lower()
        name = request.form['first_name']+' '+request.form['last_name']
        phone = request.form['whatsapp']
        image = request.files['image']
        image.filename = secure_filename(image.filename)
    
        type_ = session['user'][6]
        if session['user'][6] == 'teachers':
            courseType = request.form['course']
            if courseType == '':
                courseType = session['user'][7]
        # check availability of data
        if email == '':
            email = session['user'][1]
        if name == ' ':
            name = session['user'][2]
        if phone == '':
            phone = session['user'][4]
        
        if not (image.filename == ''):
            path = f'{homeDir}static/Users_Data/{type_}/{str(session["user"][0])}/Pictures/Personal_Pic.png'
            image.save(path)

        # email changing 
        if session['user'][1] != email:
            if (emailer.valide_email(email)):
                code = random.randint(100000, 999999)
                
                message_ = {'To':email , 'title':'send config', 'message':'here is your code : '+str(code), 'attachment':None}
                emailer.send(message_)
                
                emailChangeFlag = True
            else :
                if session['user'][6] == 'students':
                    return render_template('profile.html',state = ["The email is invalide","",""], result = session['user'])
                elif session['user'][6] =='teachers':
                    return render_template('teacher.html',state = ["The email is invalide","",""], result = session['user'])
        
        # save new data in database
        if session['user'][6]=='students':
            new_data = {'email':email,'name':name,'phone':phone,'code':code}
        elif session['user'][6]=='teachers':
            new_data = {'email':email,'name':name,'phone':phone,'code':code, 'courseType':courseType}
        DB.__edit__(type_,session['user'], new_data)
        
        
        
        
        user = DB.search(type_,email)
        session['username'] = user[2]
        session['user'] = user
        
        # make suitable output
        if emailChangeFlag :
            _profile_(state = ["Your profile updated successfully and we send validation code to your email","",""])
        else:
            _profile_(state = ["Your profile updated successfully","",""])

    return redirect(f'/profile')
    





    
@app.route("/Upload_PDF",methods = ['GET','POST'])
def Upload_PDF():
    if request.method == 'POST':
        
        acceptedLessons,notAcceptedLessons,readyLessons,finishedLessons = DB.getStudentLessons(session['user'][0])
        acceptedLessons = sorted(acceptedLessons, key=lambda d: d['lessonID'], reverse=True)
        notAcceptedLessons = sorted(notAcceptedLessons, key=lambda d: d['lessonID'], reverse=True)
        readyLessons = sorted(readyLessons, key=lambda d: d['lessonID'], reverse=True)
        finishedLessons = sorted(finishedLessons, key=lambda d: d['lessonID'], reverse=True)


        type_ = session['user'][6]
        uploaded_file = request.files['file']
        uploaded_file.filename=secure_filename(uploaded_file.filename)

        path = f'{homeDir}static/Users_Data/{type_}/{str(session["user"][0])}/Lectures/{uploaded_file.filename}'
        isExist = DB.search('lessons',path,by='lessonLOC')
        print('isExist: ',isExist)
        if not isExist:

            uploaded_file.save(path)
            text = f" here is a request from {session['user'][2]} \n\n here is the student's contact information \n\n {session['user'][1]} \n {session['user'][4]}"                 
            message_ = {'To':emailer.Admin , 'title':'request lesson', 'message':text, 'attachment':path}
            emailer.send(message_)
            DB.addLesson('lessons',{'lessonLOC':path,'studentID':session['user'][0],'teacherID':None,'date':request.form['date'],'state':'0'})
            LOG.addTaskLog(session['user'][1],uploaded_file.filename,datetime.now())
            

            
            
        

            state = ["","Your file uploaded and sent to Admin",""]
            return render_template('profile.html',state = state, result = session['user'], myAcceptedLessons = acceptedLessons, myNotAcceptedLessons = notAcceptedLessons, myReadyLessons = readyLessons, myFinishedLessons = finishedLessons)

        else:
            state = ["","You have a file with the same Name, please change the file name ",""]
            return render_template('profile.html',state = state, result = session['user'], myAcceptedLessons = acceptedLessons, myNotAcceptedLessons = notAcceptedLessons, myReadyLessons = readyLessons, myFinishedLessons = finishedLessons)


    
    return redirect("/profile")



@app.route("/admin")
def admin():
    if session['user']:
        if session['user'][1] == emailer.Admin or True: 
            notification = {**DB.getAllCount(),**LOG.getAll()}
            

            return render_template("admin.html",notification = notification, user=session['user'])
    return redirect('/home')


# *******************signIN using google*******************
# @app.route('/auth/google')
# def google_auth():
#     params = {
#         'client_id': GOOGLE_CLIENT_ID,
#         'redirect_uri': GOOGLE_REDIRECT_URI,
#         'response_type': 'code',
#         'scope': 'email profile',
#     }
#     auth_url = f"{GOOGLE_AUTHORIZATION_URI}?{'&'.join(f'{k}={v}' for k, v in params.items())}"
#     return redirect(auth_url)

# @app.route('/logwithgoogleserver')
# def google_callback():
#     code = request.args.get('code')
#     data = {
#         'code': code,
#         'client_id': GOOGLE_CLIENT_ID,
#         'client_secret': GOOGLE_CLIENT_SECRET,
#         'redirect_uri': GOOGLE_REDIRECT_URI,
#         'grant_type': 'authorization_code',
#     }
#     response = requests.post(GOOGLE_TOKEN_URI, data=data)
#     access_token = response.json().get('access_token')

#     # Use the access_token to fetch user information
#     user_info_response = requests.get(f"{GOOGLE_USER_INFO_URI}?access_token={access_token}")
#     user_info = user_info_response.json()


#     # Here, you can store user_info['email'] or other relevant information in your database
#     # and then proceed to authenticate the user in your system.

#     # signUpUsingGoogle(user_info)
#     return render_template('logWithGoogle.html',userInfo = user_info)

# @app.route('/logwithgoogleserverCofirming')
# def signUpUsingGoogle(data):
#     name = data['name']
#     # password = request.form['password']
#     email = data['email']
#     type_ = request.form['type']
#     # check availability of the input data
#     if 'agreeTS' not in request.form :
#         return render_template('sign-up.html', state = "Please read and agree on Terms of Service and Privacy Policy")
#     if name == None:
#         return render_template('sign-up.html', state = "Please enter valide name")
#     if email == None:
#         return render_template('sign-up.html', state = "Please enter valide email")
#     if password == None:
#         return render_template('sign-up.html', state = "Please enter valide password")
    
#     emailExist = DB.search('students',email,by='email')
#     if not emailExist :
#         emailExist = DB.search('teachers',email,by='email')

#     # nameExist = DB.search('students',name,by='username')
#     # if not nameExist :
#     #     nameExist = DB.search('teachers',name,by='username')

#     if emailExist :
#         return render_template('sign-up.html', state = "The email is exist please sign in if you have an account")
#     # elif nameExist :
#     #     return render_template('sign-up.html', state = "The name is exist please sign in if you have an account")
    
#     emailValide = emailer.valide_email(email)
#     if not emailValide :
#         return render_template('sign-up.html', state = "Please Enter Valide Email")
    
#     #Every thing is good ... create account
#     code = random.randint(100000, 999999)
#     message_ = {'To':email , 'title':'send config', 'message':'here is your code : '+str(code), 'attachment':None}
#     emailer.send(message_)
#     DB.__signup__(type_,name, email, password,code)
#     return render_template('sign-in.html', state = "")


@app.route('/lessonAccepted',methods=['POST'])
def lessonAccepted():
    if request.method == 'POST':
        data = request.get_json()
        my_variable = data.get('variable')
        studentID = DB.search('lessons',int(my_variable),by='id')
        DB.addLesson('st-tch-ls',{'studentID':studentID[1],'teacherID':session['user'][0],'lessonID':int(my_variable)})
        DB.editLesson({'state':1,'lessonID':int(my_variable)})
        
        response_data = {'message': f'Received variable: {my_variable}'}
        LOG.addAcceptTeacherLog(session['user'][1],my_variable,datetime.now())
        return jsonify(response_data), 200
    return jsonify({'error': str('10')}), 500
    

@app.route('/live', methods=['POST','GET'])
def live():
    if request.method == 'POST':
        lessonID = request.form['selectLesson']
        roomName = DB.getRoomName(lessonID)
        data = DB.getLessonData(lessonID)
        state = False
        if session['user'][6] == 'students':
            state = True

        LOG.addLiveLog(data['teacherName'],data['studentName'],data['lessonName'],datetime.now(),state)

        return render_template('index.html',roomName = roomName, result = session['user'])
    return redirect('/profile')

@app.route('/student_finish_course', methods=['POST','GET'])
def student_finish_course():
    if request.method == 'POST':
        lessonID = request.form['selectLesson']
        data = DB.getLessonData(lessonID)
        DB.studentLessonFinished(lessonID)
        LOG.addFinishLog(data['teacherName'],data['studentName'],data['lessonName'],datetime.now(),False)

    return redirect('/profile')


@app.route('/getLessonData/<int:id>', methods=['GET'])
def get_data(id):
    my_variable = DB.getLesson(id)
    data = my_variable
    return jsonify(data)

@app.route('/finish_lesson', methods = ['GET','POST'])
def finishLesson():
    if request.method == 'POST':
        lessonID = request.form['selectLesson']
        data = DB.getLessonData(lessonID)
        DB.lessonFinished(lessonID)
        LOG.addFinishLog(data['teacherName'],data['studentName'],data['lessonName'],datetime.now(),True)
    return redirect('/profile')


@app.route('/lesson_accept_student', methods = ['POST'])
def lesson_accept_student():
    if request.method == 'POST':

        data = request.get_json()
        print('accepted lesson:    ',data)
        lessonID = data.get('variable')['lessonID']
        teacherID = data.get('variable')['teacherID']
        lessonAccepted = data.get('variable')['state']
        print(data)
        teacher = DB.search('teachers',int(teacherID),by='id')
        lesson = DB.search('lessons',int(lessonID),by='id')

        teacherName = teacher[2]
        lessonName = lesson[3].split('/')[-1]
        studentName = session['user'][2]
        
        if lessonAccepted:                
            roomName = f"Meeting Between {teacherName} and {studentName} for {lessonName}"
            DB.acceptLesson({'lessonID':lessonID,'teacherID':teacherID,'studentID':session['user'][0],'roomName':roomName})
            LOG.addAcceptStudentLog(teacherName,studentName,lessonName,datetime.now(),True)

        else:
            DB.rejectLesson({'lessonID':lessonID,'teacherID':teacherID,'studentID':session['user'][0]})
            LOG.addAcceptStudentLog(teacherName,studentName,lessonName,datetime.now(),False)



        

        response_data = {'message': f'Received variable: {lessonID}'}
        return jsonify(response_data), 200
    return jsonify({'error': str('10')}), 500

@app.route('/clear_logs',methods=['GET','POST'])
def clear_logs():
    if request.method == 'POST':
        LOG.clearAll()
    return redirect('/home')





if __name__ == '__main__':
    logFolder = 'logs/'
    LOG = Log(logFolder)
    emailPass = sys.argv[2]
    DB = DataBase('users.db')
    emailer = sender(emailPass)
    video = Video()
    app.secret_key = 'Medad_WS@MishkaKids-2023_'
    port = sys.argv[1]
    app.run(host='localhost', port = port, debug=True)
    
    
