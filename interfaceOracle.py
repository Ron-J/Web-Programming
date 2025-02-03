import cx_Oracle as mycon
con=mycon.connect(host='localhost',user='system',passwd='tiger')
cur=con.cursor()
cur2=con.cursor()

typep={'medicinal':1,'mix':5,'surgery1':4,'surgery2':5,'surgery3':6,'surgery4':7}

typec={'lower':3,'upper':4,'heart':5,'head':5,'brain':7}

#Accepting data from users

def inputdata():
  cur2.execute("SELECT max(SNO) FROM Hospital")
  p=cur2.fetchall()
  try:
    sno=p[0][0]
  except:
    sno=0
    name=input("Enter the name of hospital")
    #calculating the score based on service
    typepi=input("Enter the type of procedure from:"+str(typep))
    while (typepi in typep)==False:
        print("Invalid input")
        typepi=input("Enter the type of procedure")
    typeci=input("Enter the type of condition:"+str(typec))
    while (typeci in typec)==False:
        print("Invalid input")
        typeci=input("Enter the type of condition")
    time=input("Enter the total time taken to start treatment in days")
    sideeffects=input("Enter the total number of times unexpected conditions occured")
    location=input("Enter the location of the center")
    #score out of 100

    sev=typep[typepi]*typec[typeci]    
    updscore=sev-(int(time)+int(sideeffects))/sev
    try:
        cur.execute("Select Rating,Reviews from Hospital where name='{}'".format(name))
        a=cur.fetchall()
        n=(a[0][0]*a[0][1]+updscore)/(a[0][1]+1)
        cur.execute("Update Hospital set Rating={}, Reviews={} where name='{}'".format(n,a[0][1]+1,name))
    except:
        cur.execute("Insert into Hospital values({},'{}',{},{},{})".format(sno+1,name,int(updscore),location,1))
    con.commit()
        

def readdata(x, name): 
        #1.Show All 2. Highest Rated 3. Search Hospital 4. Search with Location
        if x=="1":
            cur1=con.cursor()
            cur1.execute("select * from Hospital")
            h=cur1.fetchall()
            for i in h:
               print(i)
        elif x=="2":
            cur3=con.cursor()
            cur3.execute("SELECT max(Rating) from hospital")
            p=cur3.fetchall()
            max=p[0][0]
            cur3.execute("Select * from hospital where rating={}".format(max))
            c=cur3.fetchall()
            print(c)
        elif x=="3":
            cur3=con.cursor()
            try:
               cur3.execute("SELECT * from hospital where name='{}'".format(name))
               print(cur3.fetchall())
            except:
              print("Not Found")
        elif x=="4":
            cur3=con.cursor()
            try:
               cur3.execute("SELECT * from hospital where location='{}'".format(name))
               print(cur3.fetchall())
            except:
              print("Not Found")