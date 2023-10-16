from flask import Blueprint, session, render_template, request, redirect
import random
from functions.functions import dataBase
DB = dataBase('users.db')
# emailer = sender(emailPass)


auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login")
def _login_():
    if session['user'] != None :
        return render_template('home.html',result = session['user'])
    else :
        return render_template('sign-in.html', state = "")

@auth_bp.route("/signup")
def _signup_():
    if session['user'] != None :
        return render_template('home.html',result = session['user'])
    else :
        return render_template('sign-up.html', state = "")




@auth_bp.route("/loginRequist",methods = ['GET','POST']) #******************************login***************************
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # serch for email in students and teachers table
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
            return(redirect('/profile'))
        return render_template('sign-in.html', state = 'The password is not correct')
    return render_template('sign-in.html', state = "")

        


    
    
@auth_bp.route("/signupRequist",methods = ['GET','POST']) #******************************signup***************************
def signup():
    if request.method == 'POST'  :
        name = request.form['username']
        password = request.form['password']
        email = request.form['email']
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

        # nameExist = DB.search('students',name,by='username')
        # if not nameExist :
        #     nameExist = DB.search('teachers',name,by='username')

        if emailExist :
            return render_template('sign-up.html', state = "The email is exist please sign in if you have an account")
        # elif nameExist :
        #     return render_template('sign-up.html', state = "The name is exist please sign in if you have an account")
        
        emailValide = emailer.valide_email(email)
        if not emailValide :
            return render_template('sign-up.html', state = "Please Enter Valid Email")
        
        #Every thing is good ... create account
        code = random.randint(100000, 999999)
        message_ = {'To':email , 'title':'send config', 'message':'here is your code : '+str(code), 'attachment':None}
        emailer.send(message_)
        DB.__signup__(type_,name, email, password,code)
        return render_template('sign-in.html', state = "")
        
        
        
    if session['user']!=None :
        if session['user'][6] == 'students':
            return render_template('profile.html',state = "", result = session['user'])
        elif session['user'][6] =='teachers':
            return render_template('teacher.html',state = "", result = session['user'])
    else :
        return render_template('sign-up.html', state = "")
    