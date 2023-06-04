from flask import Flask,request,redirect,render_template,session,url_for
from functions.functions import DB
from functions.mail_sender import sender
import sys
import os
import random
#from PIL import Image

path = os.path.dirname(__file__)

app_root = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)



print(app_root)


@app.route("/_home_")
def _home_():
    if 'user' in session :
        result = session['user']
    else :
        result = None
    print(result)
    return render_template('home.html',result = result)

@app.route("/_services_")
def _services_():
    #return render_template('services.html')
    if 'user' in session :
        result = session['user']
    else :
        result = None
    print(result)
    return render_template('home.html',result = result)

@app.route("/_profile_")
def _profile_():
    if ('username' in session) :
        print(session['user'])
        return render_template('profile.html',state = ["","",""], result = session['user'])
    else :
        print(None)
        return render_template('sign-in.html',state = "")

@app.route("/_teacher_")
def _teacher_():
    if 'user' in session :
        result = session['user']
    else :
        result = None
#    return render_template('teacher.html')
    print(result)
    return render_template('home.html',result = result)

@app.route("/_contactus_")
def _contactus_():
    if 'user' in session :
        result = session['user']
    else :
        result = None
    print(result)
    return render_template('contact-us.html',result = result)

@app.route("/_login_")
def _login_():
    if 'user' in session :
        return render_template('home.html',result = session['user'])
    else :
        return render_template('sign-in.html', state = "")

@app.route("/_signup_")
def _signup_():

    if 'user' in session :
        return render_template('home.html',result = session['user'])
    else :
        return render_template('sign-up.html', state = "")







@app.route("/",methods = ['GET','POST'])
def main():

    if 'user' in session :
        result = session['user']
    else :
        result = None
    print(result)
    return render_template('home.html',result = result)





@app.route("/home",methods = ['GET','POST'])
def home():
    #if request.method == 'POST':
    if 'username' in session :

        result = session['user']
    else :
        result = None
    print(result)
    return render_template("home.html", result = result)




@app.route("/logout",methods = ['GET','POST'])
def logout():
    if 'user' in session :
        session.pop('username',None)
        session.pop('user',None)

    print(None)
    return render_template('home.html',result = None)



@app.route("/login",methods = ['GET','POST'])
def login():
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        user = My_DB.search(email)
        if not user :

            return render_template('sign-in.html', state = 'This email is not exist')

        user = My_DB.__login__(user,password)
        if user :

            session['username'] = user[2]
            session['user'] = user
            print(user)
            return render_template('profile.html',state = ["","",""], result = session['user'])

        return render_template('sign-in.html', state = 'The password is not correct')
    
    return redirect(url_for("_profile_"))




@app.route("/signup",methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        email = request.form['email']
        print(request.form)
        if 'checkbox' not in request.form :
            return render_template('sign-up.html', state = "Please read and agree on Terms of Service and Privacy Policy")
        if name == None:
            return render_template('sign-up.html', state = "Please enter valide name")
        if email == None:
            return render_template('sign-up.html', state = "Please enter valide email")
        if password == None:
            return render_template('sign-up.html', state = "Please enter valide password")

        emailExist = My_DB.search(email,by='email')
        nameExist = My_DB.search(name,by='username')
        if emailExist :
            return render_template('sign-up.html', state = "The email is exist please sign in if you have an account")
        elif nameExist :
            return render_template('sign-up.html', state = "The name is exist please sign in if you have an account")

        emailValide = emailer.valide_email(email)
        if not emailValide :
            return render_template('sign-up.html', state = "Please Enter Valide Email")


        print(emailValide)



        code = random.randint(100000, 999999)



        message_ = {'To':email , 'title':'send config', 'message':'here is your code : '+str(code), 'attachment':None}
        print(code)
        emailer.send(message_)
        print('donee')
        My_DB.__signup__(name, email, password,code)
        return render_template('sign-in.html', state = "")



    return render_template('sign-up.html', state = "")




@app.route("/contactus", methods= ['GET','POST'])
def contactus():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        title = request.form['title']
        subject = request.form['subject']
        if 'user' in session :
            userData = session['user']
        else :
            userData = None

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

        user = My_DB.search(email)
        if not user :
            return render_template('contact-us.html', state = 'Email is not correct',result=userData)


        user = My_DB.__login__(user,password)
        if user :
            TMessage = "Hi Admin" + "\n\n" + subject +"\n\n\n" + "here is my email and phone number \n" + phone +"\n" + email
            message_ = {'To':emailer.Admin, 'title':title, 'message':TMessage, 'attachment':None }
            emailer.send(message_)
            return render_template('contact-us.html', state = 'Your Message sent successfully to Admin',result=userData)

        return render_template('contact-us.html', state = 'password is not correct',result=userData)


    return redirect("/_contactus_")

@app.route("/update_profile",methods = ['GET','POST'])

def Update_Profile():
    if request.method == 'POST':
        st = False
        code = None


        email = request.form['email']
        name = request.form['first_name']+' '+request.form['last_name']
        phone = request.form['whatsapp']
        image = request.files['image']

        if email == '':
            email = session['user'][1]

        if name == ' ':
            name = session['user'][2]

        if phone == '':
            phone = session['user'][4]

        if not (image.filename == ''):
            path = 'static/Users_Data'+'/'+str(session['user'][0])+'/Pictures/'+'Personal_Pic.png'
            image.save(path)

        if session['user'][1] != email:
            if (emailer.valide_email(email)):
                code = random.randint(100000, 999999)

                message_ = {'To':email , 'title':'send config', 'message':'here is your code : '+str(code), 'attachment':None}
                emailer.send(message_)

                st = True
            else :
                return render_template('profile.html',state = ["The email is invalide","",""], result = session['user'])



        new_data = {'email':email,'name':name,'phone':phone,'code':code}
        My_DB.__edit__(session['user'][1], new_data)




        user = My_DB.search(email)
        session['username'] = user[2]
        session['user'] = user

        if st :
            return render_template('profile.html',state = ["Your profile updated successfully and we send validation code to you email","",""], result = session['user'])
        else:
            return render_template('profile.html',state = ["Your profile updated successfully","",""], result = session['user'])

    return redirect(url_for("_profile_"))





@app.route("/Upload_PDF",methods = ['GET','POST'])
def Upload_PDF():
    if request.method == 'POST':
        #try  :
        uploaded_file = request.files['file']
        date = request.form['date']
        print(uploaded_file.filename)
        path = 'static/Users_Data'+'/'+str(session['user'][0])+'/Lectures/'+uploaded_file.filename
        uploaded_file.save(path)
        print("DONE")
        text = f" here is a request from {session['username']} \n\n the student need to start in {date} \n\n here is the student's contact information \n\n {session['user'][1]} \n {session['user'][4]}"
        message_ = {'To':emailer.Admin , 'title':'request lesson', 'message':text, 'attachment':path}
        emailer.send(message_)

        return render_template('profile.html',state = ["","Your file uploaded and sent to Admin",""], result = session['user'])


        #except :
           # print('file not exist')

    return redirect(url_for("_profile_"))


#@app.route("/Upload_Image",methods = ['GET','POST'])
#def Upload_Image():
#    if request.method == 'POST':

#        uploaded_file = request.files['image']
#        path = 'static/Users_Data'+'/'+str(session['user'][0])+'/Pictures/'+'Personal_Pic.png'
#        uploaded_file.save(path)


#        return render_template('profile.html',state = ["Image Uploaded Successfully","",""], result = session['user'])

#    return render_template('profile.html',state = ["","",""], result = session['user'])


if __name__ == '__main__':
    emailPass = input('Enter password for Medad email ')
    My_DB = DB('users.db')
    emailer = sender(emailPass)
    app.secret_key = 'Medad_WS@MishkaKids-2023_'
    port = sys.argv[1]
    app.run(host='localhost', port = port, debug=True)
