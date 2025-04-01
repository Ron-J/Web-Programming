from flask_mail import Mail, Message
from flask import Flask, request, render_template, redirect, url_for, session, flash
import secrets
import os
from serverMySqlInterface import *

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# --- Email Configuration (ADD YOUR DETAILS HERE) ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'mail to be used by server@gmail.com'  # Use your actual Gmail address
app.config['MAIL_PASSWORD'] = 'mail to be used by server>Manage Account>Security>App Password'     # Use your generated App Password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

# --- reCAPTCHA Configuration (ADD YOUR KEYS) ---
app.config['RECAPTCHA_SITE_KEY'] = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'  # << FROM Google reCAPTCHA
app.config['RECAPTCHA_SECRET_KEY'] = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'  # << FROM Google reCAPTCHA

# Temporary token storage (use database in production)
password_reset_tokens = {}

# User database (replace with DB in production)
users = {
    'abc': {'password': 'student', 'email': 'abc.@gmail.com'},
    'abc': {'password': 'student', 'email': 'abc@gmail.com'},
}

# --- Routes ---
@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        captcha_response = request.form.get('g-recaptcha-response')
        
        # Verify CAPTCHA first
        if not verify_recaptcha(captcha_response):
            return render_template(
                "login.html",
                error="CAPTCHA verification failed",
                captcha_error="Please complete the CAPTCHA",
                site_key=app.config['RECAPTCHA_SITE_KEY']
            )
        
        if username in users and users[username]['password'] == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template(
                "login.html",
                error="Invalid credentials",
                site_key=app.config['RECAPTCHA_SITE_KEY']  # Preserve CAPTCHA
            )
    
    return render_template("login.html", site_key=app.config['RECAPTCHA_SITE_KEY'])

@app.route('/forgot-password', methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        user = next((u for u in users if users[u]['email'] == email), None)
        
        if user:
            token = secrets.token_urlsafe(32)
            password_reset_tokens[token] = user
            
            # Send email (REPLACE WITH YOUR EMAIL IN THE 'sender' FIELD)
            msg = Message(
                'Password Reset Request',
                sender='mail to be used by server- same as before@gmail.com',  # << MUST MATCH MAIL_USERNAME
                recipients=[email]
            )
            msg.body = f"""To reset your password, visit:
{url_for('reset_password', token=token, _external=True)}

If you didn't request this, ignore this email.
"""
            mail.send(msg)
            
            flash('Password reset link sent to your email', 'info')
        else:
            flash('Email not found', 'error')
    
    return render_template("forgot_password.html")

@app.route('/reset-password/<token>', methods=["GET", "POST"])
def reset_password(token):
    if token not in password_reset_tokens:
        flash('Invalid/expired token', 'error')
        return redirect(url_for('login'))
    
    if request.method == "POST":
        new_password = request.form.get("password")
        user = password_reset_tokens[token]
        users[user]['password'] = new_password  # In prod: hash password
        del password_reset_tokens[token]
        flash('Password updated successfully', 'success')
        return redirect(url_for('login'))
    
    return render_template("reset_password.html", token=token)

# --- Helper Functions: Prototype only ---
def verify_recaptcha(response):
    if not response:
        return False
    return True 
# Logout route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

#Home Page
@app.route('/home', methods=["GET", "POST"])
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template("home.html", username=session.get('username'))

#Search Page
@app.route('/search', methods =["GET", "POST"])
def search():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    centers= []
    if request.method == "POST":
        x=int(request.form.get("searchby"))
        print(x+1)
        if(x==1 or x==2):
            centers=readdata(x, "")
            print(centers)
        elif(x==3):
            centers=readdata(x,request.form.get("centerName"))
        elif(x==4):
            centers=readdata(x,request.form.get("location"))
    return render_template("search.html", centers=centers)

#Review Page
@app.route('/review', methods=["GET", "POST"])
def review():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == "POST":
        name=request.form.get("name")
        typep=int(request.form.get("TypeP"))
        typec=int(request.form.get("TypeC"))
        time=int(request.form.get("time"))
        sideeffects=int(request.form.get("sideeffects"))
        location=request.form.get("location")
        inputdata(name, typep, typec, time, sideeffects, location)
        return render_template("thankyou.html")
    return render_template("review.html")

if __name__=='__main__':
    app.run(debug=True)
