import mysql.connector as mycon
con=mycon.connect(host='localhost',user='root',passwd='tiger', database="db")
cur=con.cursor()
cur2=con.cursor()

#Accepting data from users

def inputdata(name, typep, typec, time, sideeffects, location):
    cur2.execute("SELECT max(SNO) FROM Hospital")
    p=cur2.fetchall()
    sno=p[0][0]
    sev=typep*typec    
    updscore=sev-(int(time)+int(sideeffects))/sev
    try:
        cur.execute("Select Rating,Reviews from Hospital where name='{}'".format(name))
        a=cur.fetchall()
        n=(a[0][0]*a[0][1]+updscore)/(a[0][1]+1)
        cur.execute("Update Hospital set Rating={}, Reviews={} where name='{}'".format(n,a[0][1]+1,name))
    except:
        cur.execute("Insert into Hospital values({},'{}',{},'{}',{})".format(sno+1,name,int(updscore),location,1))
    con.commit()
        

def readdata(x, name): 
        #1.Show All 2. Highest Rated 3. Search Hospital 4. Search with Location
        cur1=con.cursor(dictionary=True)
        if x==1:
            cur1.execute("select * from Hospital")
            return cur1.fetchall()
        elif x==2:
            cur4=con.cursor()
            cur4.execute("SELECT max(Rating) from hospital")
            p=cur4.fetchall()
            max=p[0][0]
            cur1.execute("Select * from hospital where rating={}".format(max))
            return cur1.fetchall()
        elif x==3:
            try:
               cur1.execute("SELECT * from hospital where name='{}'".format(name)) 
               return cur1.fetchall()  
            except:
              return []
        elif x==4:
            try:
               cur1.execute("SELECT * from hospital where location='{}'".format(name))
               return cur1.fetchall()
            except:
              return []
        return []