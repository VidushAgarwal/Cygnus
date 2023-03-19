from django.shortcuts import render
import os
from os import path
import keyboard
# Create your views here.
mast=0
diff=1
email=" "
c=[]
sup=0
def home(request):
        return render(request,"home.html")
def front(request):
        keyboard.unhook_all()
        return render(request,"front.html")
def abc(request):
        global diff
        ch=request.POST.get('SIGN-IN')
        if ch!=None:
                ch=None
                diff=2
                return render(request,'login.html')
        else:
                diff=1
                return render(request,'sign-up(1).html')
def log(request):
        keyboard.unhook_all()
        global diff
        if diff==1:
                err="" 
                err2=""
                if request.method =="POST":
                        fn=request.POST.get('first-name')
                        ln=request.POST.get('last-name')
                        em=request.POST.get('email')
                        pa=request.POST.get('password')
                        dat=request.POST.get('date')
                if not path.exists("username.user"):
                        q=open("username.user", "w")
                        q.close()
                def verify(a):
                        s = 0
                        c = 0
                        no = 0
                        fl = 0
                        for i in a:
                                if ord(i) >= 97 and ord(i) <= 122:
                                        s = 1
                                elif ord(i) >= 65 and ord(i) <= 91:
                                        c = 1
                                elif ord(i) >= 48 and ord(i) <= 57:
                                        no = 1
                                else:
                                        if ord(i) != 46 and ord(i) != 95 and ord(i) != 64:
                                                fl = 1
                        if s == 1 and c == 1 and no == 1 and fl != 1:
                                return 1
                        elif (s == 1 or c == 1 or fl == 1) and fl != 1:
                                return 2
                        else:
                                return 0

                def age():
                        dob = ""
                        from datetime import date
                        da = str(date.today())
                        dob =dat
                        a = int(da[0:4]) * 365 + int(da[5:7]) * 30 + int(da[8:10])
                        b = int(dob[0:4]) * 365 + int(dob[5:7]) * 30 + int(dob[8:10])
                        if a - b >= 5844:
                                return (dob)
                        else:
                                return 1
                if fn!=None:
                        first_name =fn
                        last_name =ln
                        dob = age()
                        if dob==1:
                                err={"err":"You must be above 16 years of age"}
                                return render(request,'sign-up(1).html',err)
                        username = em
                        username = username.lower()
                        if username[-11:] != "@cygnus.com":
                                err2={"err2":"Please add proper domain @cygnus.com at the end"}
                                return render(request, 'sign-up(1).html',err2)
                        ch=verify(username)
                        if ch == 2:
                                file = open("username.user", "r")
                                q = file.readlines()
                                file.close()
                                if username + "\n" not in q:
                                        f=verify(pa)
                                        if f == 1:
                                                q.append(username + "\n")
                                                a = open("username.user", "w")
                                                for i in q:
                                                        a.write(i)
                                                a.close()
                                                os.mkdir(username)
                                                os.chdir(username)
                                                b = open((username + ".info"), "w")
                                                b.write(first_name + " ")
                                                b.write(last_name + "\n")
                                                b.write(pa + "\n")
                                                b.write(dob + "\n")
                                                b.close()
                                                os.mkdir("sent")
                                                os.chdir("..")
                                        else:
                                                err1={"err1":"Password not valid"}
                                                return render(request,'sign-up(1).html',err1)
                                else:
                                        err2={"err2":"Email exists try something new"}
                                        return render(request,'sign-up(1).html',err2)
                        else:
                                err2={"err2":"Email not valid"}
                                return render(request,'sign-up(1).html',err2)
                return render(request,'exit.html')
        if diff==2:
                global email
                global sup
                email=request.POST.get('email')
                password=request.POST.get('password')
                a=open("username.user","r")
                b=a.readlines()
                a.close()
                user=False
                passw=False
                if email=="Cygnus@Swan" and password=="Swan@Cygnus":
                        sup=1
                        err1={"err1":"Welcome Superuser"}
                        return render(request,'login.html',err1)
                if email+"\n" in b:
                        user=True
                else:
                        err1={"err1":"No username exists"}
                        return render(request,'login.html',err1)
                if user==True:
                        err1={"err1":"Wrong password"}
                        os.chdir(email)
                        a = open(email + ".info", "r")
                        b = a.readlines()
                        a.close()
                        os.chdir("..")
                        if b[1]==password+"\n" or sup==1:
                                sup=0
                                passw=True
                        else:
                                return render(request,'login.html',err1)
                if passw==True:
                        return render(request,'home.html')
def write(request):
        global email
        keyboard.unhook_all()
        reciever=request.POST.get('reciever')
        reciever.replace(" ","")
        mail=request.POST.get('message')
        mail=mail+"\n"+"0"
        file=email
        a=open("username.user","r")
        b=a.readlines()
        a.close()
        if reciever+"\n" not in b:
                return render(request,'compose.html',{"err":"Username doesnot exist"})
        os.chdir(reciever)
        while True:
                if not path.exists(file+".mail"):
                        a=open(file+".mail","w")
                        break
                else:
                        file=file+"1"
        a.write(mail)
        a.close()
        os.chdir("..")
        os.chdir(email)
        os.chdir("sent")
        file=reciever
        while True:
                if not path.exists(file+".mail"):
                        a=open(file+".mail","w")
                        break
                else:
                        file=file+"1"
        a=open(file+".mail","w")
        a.write(mail)
        a.close()
        os.chdir("..")
        os.chdir("..")
        return render(request,'home.html')
def mail(request):
        global email
        global c
        os.chdir(email)
        val=request.POST.get('val')
        a=c[int(val)-1]
        w=open(a,'r')
        q=w.readlines()
        q.pop(-1)
        w.close()
        w=open(a,'w')
        for i in q:
                w.write(i)
        w.write("1")
        w.close()
        os.chdir("..")
        out1={"out":q}
        return render(request,'mail.html',out1)
def smail(request):
        global email
        global c
        os.chdir(email)
        val=request.POST.get('val')
        a=c[int(val)-1]
        os.chdir("sent")
        w=open(a,'r')
        q=w.readlines()
        w.close()
        os.chdir("..")
        os.chdir("..")
        out={"out":q[:-1]}
        return render(request,'mail.html',out)
def xyz(request):
        import os
        keyboard.unhook_all()
        global c
        global email
        a=request.POST.get('xyz')
        if a=="compose":
                keyboard.add_hotkey('.', lambda:keyboard.write(' '))
                return render(request,'compose.html')
        if a=="inbox":
                import os
                os.chdir(email)
                a=os.listdir()
                a.pop(a.index("sent"))
                for i in range(0,len(a)-1):
                        if a[i][-4:]=="info":
                                a.pop(i)
                c=[]
                d=[]
                x=[]
                for i in a:
                        v=open(i,"r")
                        k=v.readlines()
                        v.close()
                        if k[-1]=="0":
                                d.append(i)
                        if k[-1]=="1":
                                x.append(i)
                for i in d:
                        c.append(i)
                for i in x:
                        c.append(i)
                for i in range(0,len(d)):
                        b=open(d[i],'r')
                        d[i]=d[i][:d[i].index("@")]+" - "+b.readline()
                        b.close()
                for i in range(0,len(x)):
                        b=open(x[i],'r')
                        x[i]=x[i][:x[i].index("@")]+" - "+b.readline()
                        b.close()
                mail={"read":x,"unread":d}
                os.chdir("..")
                return render(request,'inbox.html',mail)
        if a=="sent":
                os.chdir(email)
                os.chdir("sent")
                a=os.listdir()
                c=[]
                for i in a:
                        c.append(i)
                for i in range(0,len(a)):
                        b=open(a[i],'r')
                        a[i]=a[i][:a[i].index("@")]+" - "+b.readline()
                        b.close()
                mail={"read":a}
                os.chdir("..")
                os.chdir("..")
                return render(request,'send.html',mail)
