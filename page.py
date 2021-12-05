#from tkinter import *
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
# ser = serial.Serial('COM9',9600)
# data = ser.readline(5)
# print(data)

windowPage=0
x=0
fulltext=[0 for x in range(88)]  
flag=0
scaleW=1
scaleH=0.9
root=Tk()

SCREENWIDTH_unscaled = int(root.winfo_screenwidth())
SCREENHEIGHT_unscaled = int(root.winfo_screenheight())
SCREENWIDTH = int(root.winfo_screenwidth()*scaleW)
SCREENHEIGHT = int(root.winfo_screenheight()*scaleH)
root.state("zoomed")
root.overrideredirect(False)
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
class Page:
    def __init__(self,master):
        global SCREENHEIGHT,SCREENWIDTH,scaleH,scaleW
        SCREENWIDTH = int(root.winfo_screenwidth()*scaleW)
        SCREENHEIGHT = int(root.winfo_screenheight()*scaleH)
        master.geometry("{0}x{1}+0+0".format(SCREENWIDTH, SCREENHEIGHT))
        self.master=master
        self.master.title("UI TUGAS AKHIR FAUQI")
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
        self.exitButton = Button(self.frame,command=self.exit,bg="#FE6464",text="EXIT",font='Salsa 25 bold')
        self.exitButton2 = Button(self.frame2,command=self.exit,bg="#EF5858",text="EXIT",font='Helvetica 20 bold')
        self.startButton = Button(self.frame,command=self.start,bg="#42EA27",text="START",font='Salsa 25 bold')
        self.backBtn=Button(self.frame2,image=self.backImage,command=self.back)
        self.spBtn=Button(self.frame2,text="set",bg='red',command=self.sp)
        self.labelSuhu=Label(self.frame2)
    def sp(self):

        self.labelSuhu.config(text="yott")
        ser.write(b"14")

    def close(self):
        self.frame3.place_forget()
    def unloading(self):
        self.Giflabel.place_forget()
    def showLayar(self):
        global windowPage
        if windowPage==0:
            self.frame.place(x=0,y=0,height=SCREENHEIGHT,width=SCREENWIDTH)
            self.labelImage.place(x=0,y=0,height=SCREENHEIGHT,width=SCREENWIDTH)
            self.exitButton.place(x=self.sW*0.5775 ,y=self.sH*0.7046,width=self.sW*0.1645,height=self.sH*0.0824)
            self.startButton.place(x=self.sW*0.28958 ,y=self.sH*0.7046,width=self.sW*0.1645,height=self.sH*0.0824)
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
        # data = ser.readline(5)
        # print(data)
        # screen.labelSuhu.config(text=data)
        time.sleep(0.1)

        # if threadPdf.is_set():
            
            # data = ser.readline(1000)
            # print(data)

            

            

threadPdf=threading.Event()
t1= threading.Thread(target=timer)
t1.start()
threadPdf.set()

root.mainloop()