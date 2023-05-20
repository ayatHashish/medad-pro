from flask import Flask,request,redirect,render_template,session,url_for
from functions.functions import __signup__ , __login__
import os 

path = os.path.dirname(__file__)

app = Flask(__name__)




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



    

#@app.route("/home2",methods = ['GET','POST'])
#def home2():
   
#    return render_template("_home_.html",result = "maged")


 

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
        #print(request.form)
        email = request.form['email']
        password = request.form['password']
        user = __login__(email,password)
        if user :
            
            session['username'] = user[1]
            session['user'] = user
            return redirect(url_for("home"))

        return render_template('sign-in.html', result = 'email or password not correct')
    
    return redirect("/_login_")


    
    
@app.route("/signup",methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        #print(request.form)
        name = request.form['username']
        password = request.form['password']
        email = request.form['email']
        statue = __signup__(name, email, password)
        if statue :
            #session['username'] = request.form['username']
            #session['user'] = user
            return redirect(url_for("login"))
        
        else :
            
            return render_template('sign-up.html', result = 'email is exist')
        
    return redirect("/_signup_")




@app.route("/contactus", methods= ['GET','POST'])
def contactus():
    if request.method == 'POST':
        print(request.form)
        return redirect("/home")
    return redirect("/_contactus_")

@app.route("/student",methods = ['GET','POST'])

def student():
        
    return 'student'
    




if __name__ == '__main__':
    
    app.secret_key = 'Medad_WS@MishkaKids-2023'
    app.run(host='localhost', port = 8080, debug=True)
    
    