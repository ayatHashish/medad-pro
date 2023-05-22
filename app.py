from flask import Flask,request,redirect,render_template,session,url_for
from functions.functions import DB
from functions.mail_sender import sender
import sys
import os
import random

path = os.path.dirname(__file__)

app_root = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)



print(app_root)


@app.route("/_home_")
def _home_():
    return render_template('home.html')
                           
@app.route("/_services_")
def _services_():
    return render_template('services.html')
                           
@app.route("/_profile_")
def _profile_():
    return render_template('profile.html')
                           
@app.route("/_teacher_")
def _teacher_():
    return render_template('teacher.html')
                           
@app.route("/_contactus_")
def _contactus_():
    return render_template('contact-us.html')
                           
@app.route("/_login_")
def _login_():
    return render_template('sign-in.html', result = None)
                           
@app.route("/_signup_")
def _signup_():
    return render_template('sign-up.html',result = None)







@app.route("/",methods = ['GET','POST'])
def main():
        
    
    return redirect(url_for("home"))



 

@app.route("/home",methods = ['GET','POST'])
def home():
    #if request.method == 'POST':
    if 'username' in session :
        
        user = session['user']
    else :
        user = None
        
    return render_template("home.html", result = user)




@app.route("/logout",methods = ['GET','POST'])
def logout():
    session.pop('username',None)
    session.pop('user',None)
    return redirect("/home")
    
@app.route("/login",methods = ['GET','POST'])
def login():
    if request.method == 'POST':
 
        email = request.form['email']
        password = request.form['password']
        
        user = My_DB.search(email)
        if not user :
            return render_template('sign-in.html', result = 'email not correct')
        
        user = My_DB.__login__(user,password)
        if user :
            
            session['username'] = user[1]
            session['user'] = user
            return redirect(url_for("home"))
        
        return render_template('sign-in.html', result = 'password not correct')
    
    return redirect("/_login_")


    
    
@app.route("/signup",methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        
        emailExist = My_DB.search(email,by='email')
        nameExist = My_DB.search(name,by='username')
        if emailExist :
            return render_template('sign-up.html', result = "email exist")
        elif nameExist :
            return render_template('sign-up.html', result = "name exist")
        
        emailValide = emailer.valide_email(email)
        if not emailValide :
            return render_template('sign-up.html', result = "email invalide")
        
        
        print(emailValide)
        My_DB.__signup__(name, email, password)
        

        code = random.randint(100000, 999999)
        
        
        
        message_ = {'To':email , 'title':'send config', 'message':'here is your code : '+str(code)}
        
        emailer.send(message_)

        return redirect(url_for("login"))
        
        
        
    return redirect("/_signup_")




@app.route("/contactus", methods= ['GET','POST'])
def contactus():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        title = request.form['title']
        subject = request.form['subject']
        
        user = My_DB.search(email)
        if not user :
            print(1)
            return render_template('contact-us.html', result = 'email not correct')
        
        user = My_DB.__login__(user,password)
        if user :
            print(2)
            TMessage = "Hi Admin" + "\n\n" + subject +"\n\n\n" + "here is my email and phone number \n" + phone +"\n" + email
            message_ = {'To':emailer.Admin, 'title':title, 'message':TMessage }
            emailer.send(message_)
            return redirect(url_for("home"))
        print(3)
        return render_template('contact-us.html', result = 'password not correct')
        

    return redirect("/_contactus_")

@app.route("/student",methods = ['GET','POST'])

def student():
        
    return 'student'
    




if __name__ == '__main__':
    emailPass = input('Enter password for Medad email ')
    My_DB = DB('users.db')
    emailer = sender(emailPass)
    app.secret_key = 'Medad_WS@MishkaKids-2023_'
    port = sys.argv[1]
    app.run(host='localhost', port = port, debug=True)
    
    