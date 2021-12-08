#from tkinter import *
from tkinter.constants import S
from PIL import ImageTk, Image
from tkinter import messagebox,ttk,Tk,Frame,Label,Button,Entry,PhotoImage,END,Toplevel,NW,CENTER
import math
import os
import threading
import time
import subprocess
import serial
from serial import Serial
import struct

#haruse nng kene

ser = serial.Serial('COM9',9600)
data = ser.readline(5)
print(data)


def read_serial():
    global ser
    try:
        ser = serial.Serial('COM7',9600)
        data = ser.readline(5)
        print("USB COM7 Detected")
        print(data)
    except:
        try:
            ser = serial.Serial('COM8',9600)
            data = ser.readline(5)
            print("USB COM8 Detected")
            print(data)
        except:
            try:
                ser = serial.Serial('COM9',9600)
                data = ser.readline(5)
                print("USB COM9 Detected")
                print(data)
            except:
                try:
                    ser = serial.Serial('COM13',9600)
                    data = ser.readline(5)
                    print("USB COM13 Detected")
                    print(data)
                except:
                    print("no USB connected")
read_serial()

windowPage=0
x=0
fulltext=[0 for x in range(88)]  
flag=0
scaleW=1

scaleH=1

scaleH=0.9
count =0
hours=0
days=0
minutes=0
seconds=0
flag_HM=0
suhu=""
tegangan=""
sudut_penyalaan=""
error=""
derror=""
out_fuzzy=""
# float suhu,tegangan,sudut_penyalaan




root=Tk()

SCREENWIDTH_unscaled = int(root.winfo_screenwidth())
SCREENHEIGHT_unscaled = int(root.winfo_screenheight())
SCREENWIDTH = int(root.winfo_screenwidth()*scaleW)
SCREENHEIGHT = int(root.winfo_screenheight()*scaleH)
root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(SCREENWIDTH, SCREENHEIGHT))
root.iconbitmap('logo.ico')
def clear(s):
    result=""
    for i in s:
        if i !='[' and i !=']':
            result=result+i
    return(result)

# root.resizable(True,True)
class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        self.flag=0
        pad=0
        
        master.bind('<Escape>',self.escape)
        master.bind('<F>',self.full)
        master.bind('<f>',self.full)      
    def escape(self,event):
        global SCREENHEIGHT,SCREENWIDTH,scaleH,scaleW
        # if self.flag==0:
        self.master.overrideredirect(False)
        self.flag=1
        scaleH=0.9

            
        Page(root)
        
    def full(self,event):
        global SCREENHEIGHT,SCREENWIDTH,scaleH,scaleW
        self.master.overrideredirect(True)
        self.flag=0
        scaleH=1
        
        Page(root)
        
      
app = FullScreenApp(root)



def pharsing(x):
    global suhu,tegangan,sudut_penyalaan,error,derror,out_fuzzy
    # data = x.split(",")
    listData=str(x).split(",")
    
    if listData[0]=="b'$fauqi":
        suhu=listData[1]
        tegangan=listData[2]
        sudut_penyalaan=listData[3]
        error=listData[4]
        derror=listData[5]
        out_fuzzy=listData[6]
        
        # print("suhu=" + suhu)
        # print("tegangan="+ tegangan)
        # print("sudut penyalaan=" + sudut_penyalaan)
        # print("error=" + error)
        # print("derror=" + derror)
        # print("out fuzzy="+ out_fuzzy)

    else :
        print("pharser failed")

def date_picker():
    a=dt.date.today()
    b=dt.datetime.now()
    date = b.strftime("%d/%m/%Y %H:%M:%S")
    listData=str(date).split(" ")
    # listData=str(a).split(" ")
    if a.weekday()==0:
        hari = "Senin"
    elif a.weekday()==1:
        hari = "Selasa"
    elif a.weekday()==2:
        hari = "Rabu"
    elif a.weekday()==3:
        hari = "Kamis"
    elif a.weekday()==4:
        hari = "Jumat"
    elif a.weekday()==5:
        hari = "Sabtu"
    elif a.weekday()==5:
        hari = "Minggu"
    tanggal = hari+","+listData[0]
    jam=listData[1]+" WIB"
    # print(tanggal)
    # print(jam)
    return tanggal,jam



class Page:
    def __init__(self,master):
        global SCREENHEIGHT,SCREENWIDTH,scaleH,scaleW
        SCREENWIDTH = int(root.winfo_screenwidth()*scaleW)
        SCREENHEIGHT = int(root.winfo_screenheight()*scaleH)
        master.geometry("{0}x{1}+0+0".format(SCREENWIDTH, SCREENHEIGHT))
        self.master=master
        self.master.title("HALF BRIDGE CALCULATION SOFTWARE")
        self.sW=SCREENWIDTH
        self.sH=SCREENHEIGHT
        self.frame=Frame(self.master,bg="RED")
        self.frame2=Frame(self.master,bg="RED")

        self.indeks=0
        self.page_init()
        self.showLayar()
        self.master.bind('<Enter>',self.off)
    def off(self,event):
        global proc
        threadPdf.clear()
        self.unloading()

    def page_init(self):
        x=0
        self.Giflabel = Label(root)
        self.frame.place_forget()
        self.frame2.place_forget()
        self.photo=Image.open("foto/awal.png")
        self.photo = self.photo.resize((self.sW, self.sH), Image.ANTIALIAS)
        self.gambar = ImageTk.PhotoImage(self.photo)
        self.photo2=Image.open("foto/tab2.png")
        self.photo2 = self.photo2.resize((self.sW, self.sH), Image.ANTIALIAS)
        self.gambar2 = ImageTk.PhotoImage(self.photo2)
        self.photo3=Image.open("foto/back.png")
        self.photo3 = self.photo3.resize((int(self.sW*0.032), int(self.sH*0.06)), Image.ANTIALIAS)
        self.backImage = ImageTk.PhotoImage(self.photo3)


        self.labelImage=Label(self.frame,height=SCREENHEIGHT,width=SCREENWIDTH,image=self.gambar)
        self.labelImage2=Label(self.frame2,height=SCREENHEIGHT,width=SCREENWIDTH,image=self.gambar2)
        self.exitButton = Button(self.frame,command=self.exit,bg="#EF5858",text="EXIT",font='Helvetica 30 bold')
        self.exitButton2 = Button(self.frame2,command=self.exit,bg="#EF5858",text="EXIT",font='Helvetica 20 bold')
        self.startButton = Button(self.frame,command=self.start,bg="#9561EB",text="START",font='Helvetica 30 bold')
        self.backBtn=Button(self.frame2,image=self.backImage,command=self.back)
        self.spBtn=Button(self.frame2,text="set",bg='red',command=self.sp)
        self.labelSuhu=Label(self.frame2)

        self.spMenu=OptionMenu(self.frame2,self.clicked,"40","50","61")
        self.labelDate=Label(self.frame,font='Helvetica 12',bg="#4591EA")
        self.labelTime=Label(self.frame,font='Helvetica 12',bg="#4591EA")
        self.labelDate2=Label(self.frame2,font='Helvetica 12',bg="#4591EA")
        self.labelTime2=Label(self.frame2,font='Helvetica 12',bg="#4591EA")
        self.HM_days=Label(self.frame2,font='Helvetica 12',bg="#ffffff")
        self.HM_hours=Label(self.frame2,font='Helvetica 12',bg="#ffffff")
        self.HM_minutes=Label(self.frame2,font='Helvetica 12',bg="#ffffff")
        self.teganganLabel=Label(self.frame2,font='Helvetica 12',bg="#7BD152")
        self.firingAngleLabel=Label(self.frame2,font='Helvetica 12',bg="#7BD152")
        self.errorLabel=Label(self.frame2,font='Helvetica 12',bg="#7BD152")
        self.derrorLabel=Label(self.frame2,font='Helvetica 12',bg="#7BD152")
        self.outFuzzyLabel=Label(self.frame2,font='Helvetica 12',bg="#7BD152")

    
    def reset_HM(self):
        global seconds,minutes,hours,days
        a=messagebox.askyesno(title="reset?",message="Apakah anda yakin ingin mereset Hour Meter?")
        if a == True:
            seconds=0
            minutes=0
            hours=0
            days=0
            
    def sp(self):

        self.labelSuhu.config(text="yott")
        # ser.write(b"14")

    def close(self):
        self.frame3.place_forget()
    def unloading(self):
        self.Giflabel.place_forget()
    def showLayar(self):
        global windowPage
        if windowPage==0:
            self.frame.place(x=0,y=0,height=SCREENHEIGHT,width=SCREENWIDTH)
            self.labelImage.place(x=0,y=0,height=SCREENHEIGHT,width=SCREENWIDTH)
            self.exitButton.place(x=self.sW*0.573 ,y=self.sH*0.77,width=self.sW*0.251,height=self.sH*0.1)
            self.startButton.place(x=self.sW*0.215 ,y=self.sH*0.77,width=self.sW*0.251,height=self.sH*0.1)
        elif windowPage==1:
            self.start()
    def exit(self):
        a=messagebox.askyesno(title="EXIT?",message="Apakah anda yakin ingin menutup aplikasi?")
        if a == True:
            root.destroy()
        
    def start(self):
        global windowPage
        windowPage=1
        self.frame.place_forget()
        self.frame2.place(x=0,y=0,height=SCREENHEIGHT,width=SCREENWIDTH)
        self.labelImage2.place(x=0,y=0,height=SCREENHEIGHT,width=SCREENWIDTH)
        self.backBtn.place(x=self.sW*0.01,y=self.sH*0.02,width=self.sW*0.032, height=self.sH*0.06)

        self.exitButton2.place(x=0.77*self.sW,y=0.011*self.sH,width=0.09*self.sW,height=0.054*self.sH)
        self.spBtn.place(x=self.sW*0.2,y=self.sH*0.02,width=self.sW*0.032, height=self.sH*0.06)
        self.labelSuhu.place(x=0.4*self.sW,y=0.011*self.sH,width=0.09*self.sW,height=0.054*self.sH)

        self.exitButton2.place(x=0.813*self.sW,y=0.86*self.sH,width=0.1661*self.sW,height=0.0666*self.sH)
        self.spBtn.place(x=self.sW*0.7515,y=self.sH*0.4731,width=self.sW*0.03489, height=self.sH*0.0407)
        self.loadBtn.place(x=0.813*self.sW,y=0.7666*self.sH,width=0.1661*self.sW,height=0.0666*self.sH)
        self.labelSuhu.place(x=0.6552*self.sW,y=0.3296*self.sH,width=0.04583*self.sW,height=0.0546*self.sH)
        self.spMenu.place(x=0.6552*self.sW,y=0.4657*self.sH,width=0.04583*self.sW,height=0.0546*self.sH)
        self.labelDate2.place(x=self.sW*0.83,y=self.sH*0.0231,width=self.sW*0.098,height=self.sH*0.0421)
        self.labelTime2.place(x=self.sW*0.83,y=self.sH*0.0652,width=self.sW*0.098,height=self.sH*0.0421)
        self.HM_days.place(x=self.sW*0.6218,y=self.sH*0.8222,width=self.sW*0.03437,height=self.sH*0.032407)
        self.HM_hours.place(x=self.sW*0.6703,y=self.sH*0.8222,width=self.sW*0.03437,height=self.sH*0.032407)
        self.HM_minutes.place(x=self.sW*0.7171,y=self.sH*0.8222,width=self.sW*0.03437,height=self.sH*0.032407)
        self.reset_HM.place(x=self.sW*0.665,y=self.sH*0.8824,width=self.sW*0.05,height=self.sH*0.0287)
        self.teganganLabel.place(x=self.sW*0.1682,y=self.sH*0.7564,width=self.sW*0.07812,height=self.sH*0.0472)
        self.firingAngleLabel.place(x=self.sW*0.1682,y=self.sH*0.8166,width=self.sW*0.07812,height=self.sH*0.0472)
        self.errorLabel.place(x=self.sW*0.1682,y=self.sH*0.8768,width=self.sW*0.07812,height=self.sH*0.0472)
        self.derrorLabel.place(x=self.sW*0.4312,y=self.sH*0.7564,width=self.sW*0.07812,height=self.sH*0.0472)
        self.outFuzzyLabel.place(x=self.sW*0.4312,y=self.sH*0.8166,width=self.sW*0.07812,height=self.sH*0.0472)



    def back(self):
        global windowPage
        windowPage=0
        self.showLayar()
        self.frame2.place_forget()
        self.frame.place(x=0,y=0,height=SCREENHEIGHT,width=SCREENWIDTH)
        self.master.unbind('<Return>')



screen = Page(root)

frameCnt = 29
frames = [PhotoImage(file='foto/loading gif.gif',format = 'gif -index %i' %(i)) for i in range(frameCnt)]       
def update(ind):
    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    screen.Giflabel.configure(image=frame,bg="WHITE")
    screen.frame.after(100, update, ind)

def loadGif():    
    screen.Giflabel.place(x=SCREENWIDTH_unscaled*0.5,y=SCREENHEIGHT_unscaled*0.5,width = 150,height=150,anchor=CENTER)
    screen.frame.after(0, update, 0)


def kill():
    
    screen.unloading()

def timer():
    global flag,proc
    while True:
        data = ser.readline(5)
        print(data)
        screen.labelSuhu.config(text=data)

def timer2():
    global flag,count,hours,days,minutes,seconds,flag_HM,tegangan,sudut_penyalaan,error,derror,out_fuzzy,suhu,ser
    while True:
        
        if flag_HM == 1:
            seconds=seconds+1
            if seconds>58:
                minutes=minutes+1
                seconds=0
            if minutes>59:
                hours=hours+1
                minutes=0
            if hours>23:
                days=days+1
                hours=0
            screen.HM_minutes.config(text=minutes)
            screen.HM_hours.config(text=hours)
            screen.HM_days.config(text=days)
        time.sleep(1)
        date_picker()
        date=date_picker()[0]
        current_time=date_picker()[1]
        screen.labelDate.config(text=date)
        screen.labelTime.config(text=current_time)
        screen.labelDate2.config(text=date)
        screen.labelTime2.config(text=current_time)
            
        # print(seconds)

def timer():
    global flag,count,hours,days,minutes,seconds,tegangan,sudut_penyalaan,error,derror,out_fuzzy,suhu,flag_HM
    while True:

        
        try:
            data = ser.readline(100)
            # print(data)
            screen.labelSuhu.config(text=suhu)
            pharsing(data)
            screen.teganganLabel.config(text=tegangan)
            screen.firingAngleLabel.config(text=sudut_penyalaan)
            screen.errorLabel.config(text=error)
            screen.derrorLabel.config(text=derror)
            screen.outFuzzyLabel.config(text=out_fuzzy)
        except:
            print("recieve gagal")

        count=count+1
        if count>=10:


            date_picker()
            date=date_picker()[0]
            current_time=date_picker()[1]
            screen.labelDate.config(text=date)
            screen.labelTime.config(text=current_time)
            screen.labelDate2.config(text=date)
            screen.labelTime2.config(text=current_time)
            
            count=0


        time.sleep(0.1)

        # if threadPdf.is_set():
            
            # data = ser.readline(1000)
            # print(data)

        time.sleep(0.1)
        if flag_HM == 1:
            try:
                data = ser.readline(100)
                # print(data)
                screen.labelSuhu.config(text=suhu)
                pharsing(data)
                screen.teganganLabel.config(text=tegangan)
                screen.firingAngleLabel.config(text=sudut_penyalaan)
                screen.errorLabel.config(text=error)
                screen.derrorLabel.config(text=derror)
                screen.outFuzzyLabel.config(text=out_fuzzy)
            except:
                print("recieve gagal")
                read_serial()
                messagebox.showerror(title="recieve gagal!",message="Recieve Gagal")

 
        


            

            

threadPdf=threading.Event()
t1= threading.Thread(target=timer)
t1.start()
threadPdf.set()

root.mainloop()