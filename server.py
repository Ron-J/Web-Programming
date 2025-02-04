from serverMySqlInterface import *
from flask import Flask, request, render_template 
 
app = Flask(__name__)   
 
#Home Page
@app.route('/', methods=["GET", "POST"])
def home():
   return render_template("home.html")
#Search Page
@app.route('/search', methods =["GET", "POST"])
def search():
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
   app.run()