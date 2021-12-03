#from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox,ttk,Tk,Frame,Label,Button,Entry,PhotoImage,END,Toplevel,NW,CENTER
import math
import os
import threading
import time
import subprocess

windowPage=0
tfall=[]
splitL=[]
splitP=[]
wireLengthTolerance=[]
additionalWinding=[]
effesiensi=[]
vinMax=[]
vinMin=[]
vOut=[]
iOut=[]
duty=[]
frekuensi=[]
rIl=[]
rVo=[]
Vf=[]
ac_ind=[]
dBob_ind=[]
ac_trafo=[]
dBob_trafo=[]
bMax=[]
j=[]
s=[]
sigma_split=[]
cnt=0

fulltext=[0 for x in range(88)]  
flag=0
scaleW=1
scaleH=1
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
def splitter(s,maksChar):
    total =0
    result=""
    c = s.split()
    for i in range(len(c)):
        counter=len(c[i])
        total=total+counter
     
        if(total<maksChar):
            result=result+" "+c[i]
        else :
            result=result+"\n"+c[i]
            total=0
    return (result)
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


        # else:
        #     self.master.overrideredirect(True)
        #     self.flag=0
        #     scaleH=1
            
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
        self.master.title("HALF BRIDGE CALCULATION SOFTWARE")
        self.sW=SCREENWIDTH
        self.sH=SCREENHEIGHT
        self.frame=Frame(self.master,bg="RED")
        self.frame2=Frame(self.master,bg="RED")
        self.frame3=Frame(self.master,bg="#D7D3D3")
        self.entry =[[0 for x in range(6)]  for x in range(6)]
        self.outLabel =[[0 for x in range(5)]  for x in range(5)]
        self.btnHistory=[0 for x in range(88)]
        self.labelHistory=[0 for x in range(88)]   
        self.indeks=0
        self.page_init()
        self.showLayar()
        self.master.bind('<Enter>',self.off)
    def off(self,event):
        global proc
        threadPdf.clear()
        self.unloading()

        # os._exit()
        #sys.exit()
    def page_init(self):
        x=0
        self.Giflabel = Label(root)
        self.frame.place_forget()
        self.frame2.place_forget()
        self.frame3.place_forget()
        self.photo=Image.open("foto/awal.png")
        self.photo = self.photo.resize((self.sW, self.sH), Image.ANTIALIAS)
        self.gambar = ImageTk.PhotoImage(self.photo)
        self.photo2=Image.open("foto/tab2.png")
        self.photo2 = self.photo2.resize((self.sW, self.sH), Image.ANTIALIAS)
        self.gambar2 = ImageTk.PhotoImage(self.photo2)
        self.photo3=Image.open("foto/back.png")
        self.photo3 = self.photo3.resize((int(self.sW*0.032), int(self.sH*0.06)), Image.ANTIALIAS)
        self.backImage = ImageTk.PhotoImage(self.photo3)
        # self.photo4=Image.open("foto/calculate.png")
        # self.photo4 = self.photo4.resize((int(self.sW*0.132), int(self.sH*0.06)), Image.ANTIALIAS)
        # self.calculateImage = ImageTk.PhotoImage(self.photo4)
        self.photo5=Image.open("foto/reset.png")
        self.photo5 = self.photo5.resize((int(self.sW*0.1322), int(self.sH*0.0537)), Image.ANTIALIAS)
        self.resetImage = ImageTk.PhotoImage(self.photo5)
        self.photo6=Image.open("foto/default.png")
        self.photo6 = self.photo6.resize((int(self.sW*0.1322), int(self.sH*0.0537)), Image.ANTIALIAS)
        self.defaultImage = ImageTk.PhotoImage(self.photo6)
        self.photo7=Image.open("foto/help.png")
        self.photo7 = self.photo7.resize((int(self.sW*0.026), int(self.sH*0.0488)), Image.ANTIALIAS)
        self.helpImage = ImageTk.PhotoImage(self.photo7)
        self.photo8=Image.open("foto/history.png")
        self.photo8= self.photo8.resize((int(self.sW*0.062), int(self.sH*0.036)), Image.ANTIALIAS)
        self.historyImage = ImageTk.PhotoImage(self.photo8)
        self.photo9=Image.open("foto/history_page.png")
        self.photo9= self.photo9.resize((int(self.sW*0.312), int(self.sH*0.683)), Image.ANTIALIAS)
        self.historyPageImage = ImageTk.PhotoImage(self.photo9)
        self.photo10=Image.open("foto/history_bar.png")
        self.photo10= self.photo10.resize((int(self.sW*0.296), int(self.sH*0.083)), Image.ANTIALIAS)
        self.historyBarImage = ImageTk.PhotoImage(self.photo10)
        self.photo11=Image.open("foto/close.png")
        self.photo11= self.photo11.resize((int(self.sW*0.0145), int(self.sH*0.027)), Image.ANTIALIAS)
        self.closeImage = ImageTk.PhotoImage(self.photo11)

        self.labelImage=Label(self.frame,height=SCREENHEIGHT,width=SCREENWIDTH,image=self.gambar)
        self.labelImage2=Label(self.frame2,height=SCREENHEIGHT,width=SCREENWIDTH,image=self.gambar2)
        self.labelImage3=Label(self.frame3,height=self.sH*0.683,width=self.sW*0.312,image=self.historyPageImage)
        self.exitButton = Button(self.frame,command=self.exit,bg="#EF5858",text="EXIT",font='Helvetica 30 bold')
        self.exitButton2 = Button(self.frame2,command=self.exit,bg="#EF5858",text="EXIT",font='Helvetica 20 bold')
        self.startButton = Button(self.frame,command=self.start,bg="#9561EB",text="START",font='Helvetica 30 bold')
        self.backBtn=Button(self.frame2,image=self.backImage,command=self.back)

        
        #self.entry[0][0]=Entry(self.frame2,font=20)

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
        
       
        j=0
        k=0
        x=0
        y=0
        offsetH=self.sH*0.173
        offsetW=self.sW*0.181
        jarakW=self.sW*0.141
        jarakH=self.sH*0.0146
        entryWidth=self.sW*0.065
        entryHeight=self.sH*0.044

        
        offsetH2=self.sH*0.6367
        offsetW2=self.sW*0.181
        jarakW2=self.sW*0.141
        jarakH2=self.sH*0.0195
        labelWidth=self.sW*0.065
        labelHeight=self.sH*0.044
       

        


        # self.outLabel[4][1].place_forget()
        # self.outLabel[3][3].place_forget()
        #self.outLabel[4][3].place_forget()
   
        self.master.bind('<Return>',self.enter)
        self.reset()
        self.default()
        # self.calculate()
    def btnHistory_event(self,event,a):
        self.btnHistory_func(a)
    def help(self):
        self.page=Page2()

        
    def enter(self,event):
        self.calculate()
        

    def back(self):
        global windowPage
        windowPage=0
        self.showLayar()
        self.frame2.place_forget()
        self.frame.place(x=0,y=0,height=SCREENHEIGHT,width=SCREENWIDTH)
        self.master.unbind('<Return>')
    def calculate(self):
        global vinMax,cnt
        try:
            self.hitung()
            self.show_historyPage()
            
        except ValueError :
             messagebox.showerror("warning","ganti koma(,) dengan titik(.) untuk pecahan dan pastikan semua parameter terisi(jika tidak digunakan isi dengan nol(0))")
        
    def show_historyPage(self):
        global vinMax,cnt
        a=len(vinMax)
        jarak = self.sH*0.0094
        offsetH= self.sH*0.0732
        offsetW = self.sW*0.00729
        width = self.sW*0.296
        height = self.sH*0.083

        jarak2 = self.sH*0.03
        offsetH2= self.sH*0.083
        offsetW2 = self.sW*0.0625
        width2 = self.sW*0.222
        height2 = self.sH*0.063



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
class Page2:
    def __init__(self):
        self.help=Toplevel()
        self.help.bind('<Escape>',app.escape)
        self.help.bind('<F>',app.full)
        self.help.bind('<f>',app.full)
        self.help.title("HELP PAGE")
        self.a=int(0.55*screen.sW)
        self.help.geometry("%dx%d+%d+0" % (int(screen.sW*0.44), int(screen.sH*0.9),self.a))
        self.frame=Frame(self.help)
        self.help.resizable(0,0)
        self.help.attributes('-toolwindow', True)
        #root.after(0,loadGif)
        self.page_init()
        self.show()
    def page_init(self):
        self.photo=Image.open("foto/help_page.png")
        self.photo= self.photo.resize((int(screen.sW*0.44), int(screen.sH*0.9)), Image.ANTIALIAS)
        self.helpPageImage = ImageTk.PhotoImage(self.photo)
        self.photo2=Image.open("foto/pdf.png")
        self.photo2= self.photo2.resize((int(screen.sW*0.0458), int(screen.sH*0.077)), Image.ANTIALIAS)
        self.pdfImage = ImageTk.PhotoImage(self.photo2)
        

        self.labelImage=Label(self.help,width=int(screen.sW*0.44),height= int(screen.sH*0.9),bg="WHITE")
        self.pdfBtn=Button(self.help,command=self.pdf,activebackground="#1F4DC5",bg="#1F4DC5",borderwidth=0,image=self.pdfImage)
        
    def show(self):
        self.frame.place(x=0,y=0,width=int(screen.sW*0.44),height=int(screen.sH*0.9))
        self.labelImage.place(x=0,y=0)
        self.labelImage.config(image=self.helpPageImage)
        self.pdfBtn.place(y=screen.sH*0.715,x=screen.sW*0.061,width=screen.sW*0.0458,height=screen.sH*0.077,anchor=NW)
        self.help.mainloop()
    def pdf(self):
        global flag
        
        if flag == 0:
            self.help.after(0,loadGif)
            threadPdf.set()
            flag=1
        else:
            messagebox.showerror("warning","File PDF MANUAL CALCULATION SUDAH TERBUKA SILAHKAN CEK PADA TASKBAR ANDA")
        app.escape(root)
def kill():
    
    screen.unloading()
def timer():
    global flag,proc
    while True:
        time.sleep(0.1)

        if threadPdf.is_set():
            threadPdf.clear()
            #screen.frame.after(1000,kill)
            # os.open("pdf.pdf")
            subprocess.Popen(["pdf.pdf"], shell=True)
            flag=0

            

threadPdf=threading.Event()
t1= threading.Thread(target=timer)
t1.start()


root.mainloop()