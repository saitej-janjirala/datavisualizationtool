from tkinter import *
from tkinter import filedialog, messagebox
import os,shutil
import pandas as pd
import webbrowser
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import ImageTk, Image
class popupWindow(object):
    def __init__(self, master):
        top = self.top = Toplevel(master)
        top.geometry("400x400")
        self.l = Label(top, text="Enter your project")
        self.l.pack()
        self.e = Entry(top)
        self.e.pack()
        self.b = Button(top, text='Ok', command=self.cleanup,bg="black",fg="white")
        self.b.pack()
        self.value = ""

    def cleanup(self):
        self.value = self.e.get()
        self.top.destroy()

class popupforplot(object):
    def __init__(self, master):
        top = self.top = Toplevel(master)
        top.geometry("400x400")
        self.l = Label(top, text="Enter the figure name",)
        self.l.place(x=100,y=100)
        self.e = Entry(top)
        self.e.place(x=100,y=200)
        self.b = Button(top, text='Ok', command=self.cleanup, bg="black", fg="white")
        self.b.place(x=150,y=250)
        self.value = ""

    def cleanup(self):
        if(self.e.get()!=""):
            self.value = self.e.get()
            self.top.destroy()

class Mainpage:
    def __init__(self, master):
        self.bgforframesandlabels="white"
        self.bgforbuttonsandmenus="black"
        self.fgforbuttonsandmenus="white"
        self.master = master

        self.oldname=list()
        menubar = Menu(self.master)
        getdatasetsmenu = Menu(menubar, tearoff=0)
        getdatasetsmenu.add_command(label="Get data sets", command=self.getlinks)
        menubar.add_cascade(label="Dowload datasets", menu=getdatasetsmenu)
        master.config(menu=menubar)
        path = os.getcwd()

        self.projectspath = path + '\datavisualizationprojects'
        if(os.path.exists(self.projectspath)):
            pass
        else:
            os.mkdir(self.projectspath)

        self.frame1 = Frame(master, width=master.winfo_screenwidth(), height=master.winfo_screenheight(),)
        self.frame2 = Frame(master, width=master.winfo_screenwidth(), height=master.winfo_screenheight(), bg=self.bgforframesandlabels)
        self.startframe = Frame(master, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
        for frames in (self.frame2, self.frame1, self.startframe):
            frames.grid(row=0, column=0)

        img = Image.open("cloudsandcrops.jpg")
        img = img.resize((w, h), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        bgforstartframe = Label(self.startframe, image=img,bg="white")
        bgforstartframe.image = img
        bgforstartframe.place(x=0, y=0)

        bgforframe1= Label(self.frame1, image=img,bg="white")
        bgforframe1.image = img
        bgforframe1.place(x=0, y=0)

        #bgforframe2 = Label(self.frame2, image=img, bg="white")
        #bgforframe2.image = img
        #bgforframe2.place(x=0, y=0)

        Button(self.startframe, text="Create new project", font=("times", 20), command=self.createnewproject,
               bg=self.bgforbuttonsandmenus, fg="white").place(x=w // 4, y=h//2)
        Button(self.startframe, text="Open existing projects", font=("times", 20), bg=self.bgforbuttonsandmenus, fg="white",
               command=self.openexisting).place(x=w // 2, y=h // 2)
        self.heading = Label(self.frame1, text="CROP DATA VISUALIZATION TOOL", font=("algerian", 30),bg=self.bgforframesandlabels).place(
            x=w // 4, y=50)
        self.panel = Label(self.frame2)
        self.filedescription = Label(self.frame1, text="", font=("Helvetica", 15), padx=2, pady=2,
                                     textvariable=filedescript, bg=self.bgforframesandlabels).place(x=100, y=150)
        self.choosebutton = Button(self.frame1, text="select the file", font=("times", 20), bg=self.bgforbuttonsandmenus, fg="white",
                                   padx=2,
                                   pady=2,
                                   command=self.open_file).place(x=100, y=200)
        filetype = Label(self.frame1, text="NOTE: select only csv files", font=("times", 15), padx=2, pady=2,
                         bg=self.bgforframesandlabels).place(x=100,y=270)

        gobackfromframe1 = Button(self.frame1,text="Go Back",font=("times", 15),bg=self.bgforbuttonsandmenus,fg="white",command=lambda :self.switch_frame(self.startframe)).place(x=100,y=400)
        self.startframe.tkraise()

    def openexisting(self):
        self.selectedproject_path = filedialog.askdirectory(initialdir=self.projectspath+"/", )
        if (self.selectedproject_path):
            self.switch_frame(self.frame1)
            print(self.selectedproject_path)
        else:
            messagebox.showerror("Error opening file", "Please Try Again")

    def copy_rename(self):
        self.newobj=popupforplot(self.master)
        self.master.wait_window(self.newobj.top)
        val = self.newobj.value
        if ('a' <= val <= 'z' or '0' < val < '9'):
            try:
                old=self.oldname[len(self.oldname)-1]
                new=val+".jpg"
                src_dir = os.curdir
                dst_dir = os.path.join(self.selectedproject_path)
                src_file = os.path.join(src_dir, old)
                shutil.copy(src_file, dst_dir)
                dst_file = os.path.join(dst_dir, old)
                new_dst_file_name = os.path.join(dst_dir, new)
                os.rename(dst_file, new_dst_file_name)

            except():
                messagebox.showerror("Error saving File", "Try again")

    def createnewproject(self):
        self.w = popupWindow(self.master)
        self.master.wait_window(self.w.top)
        val = self.w.value
        if ('a' <= val <= 'z' or '0' < val < '9'):
            print(val)
            try:
                self.pp = self.projectspath + "/{}".format(val)
                os.mkdir(self.pp)
                messagebox.showinfo("Success", "Your workspace is created")
                self.switch_frame(self.frame1)
                self.selectedproject_path=self.pp
            except():
                messagebox.showerror("Error creating file", "Your project cannot be created")
        else:
            messagebox.showerror("Error creating file", "Your project cannot be created")

    def switch_frame(self, next):
        next.tkraise()

    def getlinks(self):
        webbrowser.open("agriculture_based_websites.html", new=2)

    def open_file(self):
        self.import_file_path = filedialog.askopenfilename(filetypes=[('csvfiles', '*.csv')])
        try:
            self.dataframe = pd.read_csv(self.import_file_path)
            x = os.path.basename(self.import_file_path)
            filedescript.set(x)
            # differentiating numeric and non numeric attributes
            y = self.dataframe.select_dtypes(include=['int64', 'float64', 'int32', 'float32'])
            z = self.dataframe.select_dtypes(include=['object', 'bool'])
            self.listofnumericattributes = list(y.columns)

            self.listofallattributes = list(self.dataframe.columns)
            for i in self.listofnumericattributes:
                self.dataframe[i] = self.dataframe[i].fillna(self.dataframe[i].mean())
            # for the type of graph creating a menu
            self.listofgraphs = ['barplot', 'scatterplot', 'lineplot', 'histogram', 'piechart', 'boxplot',
                                 'violinplot', 'relplot', 'distplot', 'pairplot', 'swarmplot']

            droplistgraphs = OptionMenu(self.frame1, graphsattributevariable, *self.listofgraphs)
            graphsattributevariable.set("select the graph you want")
            droplistgraphs.config(width=50, bg="black", fg="white")
            droplistgraphs.place(x=w // 2 - 200, y=150)

            droplistnumeric = OptionMenu(self.frame1, numericattributevariable, *self.listofnumericattributes)
            numericattributevariable.set("select the numeric attribute")
            droplistnumeric.config(width=50, bg=self.bgforbuttonsandmenus, fg="white")
            droplistnumeric.place(x=w // 2 + 200, y=150)

            self.a = self.listofallattributes.copy()
            droplistcategorical = OptionMenu(self.frame1, categoricattributevariable, *self.a)
            categoricattributevariable.set("select the another attribute")
            droplistcategorical.config(width=50, bg=self.bgforbuttonsandmenus, fg="white")
            droplistcategorical.place(x=w // 2 - 200, y=200)

            self.hue = self.listofallattributes.copy()
            droplisthue = OptionMenu(self.frame1, hueattributevariable, *self.hue)
            hueattributevariable.set("select the hue attribute")
            droplisthue.config(width=50,bg=self.bgforbuttonsandmenus, fg="white")
            droplisthue.place(x=w // 2 + 200, y=200)

            selectedattributeslabel = Label(self.frame1, text="", font=("times", 20),
                                            textvariable=attributeerrorlabel, bg=self.bgforframesandlabels).place(x=700, y=350)
            attributeerrorlabel.set("")
            showplots = Button(self.frame1, text="", font=("times", 15), fg="white", bg=self.bgforbuttonsandmenus,
                               textvariable=buttontext,
                               command=self.checkandplot).place(x=800, y=400)
            buttontext.set("get plots")

        except:
            messagebox.showinfo("Error choosing file", "you must choose the file in order to visualize")

    def checkandplot(self):
        self.panel.configure(image=None,bg=self.bgforframesandlabels)
        self.panel.image=None
        goback = Button(self.frame2, text='goback',bg=self.bgforbuttonsandmenus,fg="white" ,command=lambda: self.switch_frame(self.frame1))
        goback.place(x=w // 2, y=10)
        savefig=Button(self.frame2,text="save the figure",bg=self.bgforbuttonsandmenus,fg="white",command=self.copy_rename)
        savefig.place(x=w//2+200,y=10)
        if (graphsattributevariable.get() != "select the graph you want"):
            if (graphsattributevariable.get() == 'distplot' or graphsattributevariable.get() == 'histogram'):
                if (numericattributevariable.get() != "select the numeric attribute"):
                    attributeerrorlabel.set("")
                    if (graphsattributevariable.get() == 'distplot'):
                        plt.figure(figsize=(20, 10))
                        sns_plot = sns.distplot(self.dataframe[numericattributevariable.get()])
                        plt.savefig("distplotoutput.jpg")
                        self.oldname.append("distplotoutput.jpg")
                        img = Image.open("distplotoutput.jpg")
                        img = img.resize((w // 2, w // 3), Image.ANTIALIAS)
                        img = ImageTk.PhotoImage(img)
                        self.panel = Label(self.frame2, image=img)
                        self.panel.image = img
                        self.panel.place(x=100, y=100)
                        self.switch_frame(self.frame2)
                        attributeerrorlabel.set("only numeric is enough for distplot and histogram")

                    elif (graphsattributevariable.get() == 'histogram'):
                        plt.figure(figsize=(20, 10))
                        sns_plot = sns.distplot(self.dataframe[numericattributevariable.get()], kde=False)
                        plt.savefig("histogram.jpg")
                        self.oldname.append("histogram.jpg")
                        img = Image.open("histogram.jpg")
                        img = img.resize((w // 2, w // 3), Image.ANTIALIAS)
                        img = ImageTk.PhotoImage(img)
                        self.panel = Label(self.frame2, image=img)
                        self.panel.image = img
                        self.panel.place(x=0, y=100)
                        self.switch_frame(self.frame2)
                        attributeerrorlabel.set("only numeric is enough for distplot and histogram")
                else:
                    attributeerrorlabel.set("you must select numeric attribute for histogram and distplot")
            elif (graphsattributevariable.get() == 'pairplot'):
                plt.figure(figsize=(20, 20))
                sns_plot = sns.pairplot(self.dataframe)
                plt.savefig("pairplotoutput.jpg")
                self.oldname.append("pairplotoutput.jpg")
                img = Image.open("pairplotoutput.jpg")
                img = img.resize((w, w // 3), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(img)
                self.panel = Label(self.frame2, image=img)
                self.panel.image = img
                self.panel.place(x=0, y=100)
                self.switch_frame(self.frame2)
                attributeerrorlabel.set("You don't have to select any attribute for pair plot")

            elif (
                    graphsattributevariable.get() in 'barplot piechart relplot swarmplot lineplot boxplot violinplot scatterplot'):
                if (
                        numericattributevariable.get() != "select the numeric attribute" or categoricattributevariable.get() != "select the another attribute"):
                    if (graphsattributevariable.get() == 'barplot'):
                        plt.figure(figsize=(20, 5))
                        if (hueattributevariable.get() == "select the hue attribute"):
                            sns_plot = sns.barplot(self.dataframe[categoricattributevariable.get()],
                                                   self.dataframe[numericattributevariable.get()])
                        else:
                            attributeerrorlabel.set("hue attribute is choice")
                            sns_plot = sns.barplot(self.dataframe[categoricattributevariable.get()],
                                                   self.dataframe[numericattributevariable.get()],
                                                   hue=self.dataframe[hueattributevariable.get()])

                        plt.savefig("barplotoutput.jpg")
                        self.oldname.append("barplotoutput.jpg")
                        img = Image.open("barplotoutput.jpg")
                        img = img.resize((w, w // 3), Image.ANTIALIAS)
                        img = ImageTk.PhotoImage(img)
                        self.panel = Label(self.frame2, image=img)
                        self.panel.image = img
                        self.panel.place(x=0, y=100)
                        self.switch_frame(self.frame2)
                    elif (graphsattributevariable.get() == 'scatterplot'):
                        plt.figure(figsize=(20, 5))
                        if (hueattributevariable.get() == "select the hue attribute"):
                            sns_plot = sns.scatterplot(self.dataframe[categoricattributevariable.get()],
                                                       self.dataframe[numericattributevariable.get()])
                        else:
                            attributeerrorlabel.set("hue attribute is choice")
                            sns_plot = sns.scatterplot(self.dataframe[categoricattributevariable.get()],
                                                       self.dataframe[numericattributevariable.get()],
                                                       hue=self.dataframe[hueattributevariable.get()])
                        plt.savefig("scatterplotoutput.jpg")
                        img = Image.open("scatterplotoutput.jpg")
                        self.oldname.append("scatterplotoutput.jpg")
                        img = img.resize((w, w // 3), Image.ANTIALIAS)
                        img = ImageTk.PhotoImage(img)
                        self.panel = Label(self.frame2, image=img)
                        self.panel.image = img
                        self.panel.place(x=0, y=100)
                        self.switch_frame(self.frame2)

                    elif (graphsattributevariable.get() == 'boxplot'):
                        print("hello")
                        plt.figure(figsize=(20, 5))
                        if (hueattributevariable.get() == "select the hue attribute"):
                            sns_plot = sns.boxplot(self.dataframe[categoricattributevariable.get()],
                                                   self.dataframe[numericattributevariable.get()])
                        else:
                            attributeerrorlabel.set("hue attribute is choice")
                            sns_plot = sns.boxplot(self.dataframe[categoricattributevariable.get()],
                                                   self.dataframe[numericattributevariable.get()],
                                                   hue=self.dataframe[hueattributevariable.get()])
                        plt.savefig("boxplotoutput.jpg")
                        img = Image.open("boxplotoutput.jpg")
                        self.oldname.append("boxplotoutput.jpg")
                        img = img.resize((w, w // 3), Image.ANTIALIAS)
                        img = ImageTk.PhotoImage(img)
                        self.panel = Label(self.frame2, image=img)
                        self.panel.image = img
                        self.panel.place(x=0, y=100)
                        self.switch_frame(self.frame2)

                    elif (graphsattributevariable.get() == 'lineplot'):
                        plt.figure(figsize=(20, 5))
                        if (hueattributevariable.get() == "select the hue attribute"):
                            sns_plot = sns.lineplot(self.dataframe[categoricattributevariable.get()],
                                                    self.dataframe[numericattributevariable.get()])
                        else:
                            attributeerrorlabel.set("hue attribute is choice")
                            sns_plot = sns.lineplot(self.dataframe[categoricattributevariable.get()],
                                                    self.dataframe[numericattributevariable.get()],
                                                    hue=self.dataframe[hueattributevariable.get()])
                        plt.savefig("lineplotoutput.jpg")
                        img = Image.open("lineplotoutput.jpg")
                        self.oldname.append("lineplotoutput.jpg")
                        img = img.resize((w, w // 3), Image.ANTIALIAS)
                        img = ImageTk.PhotoImage(img)
                        self.panel = Label(self.frame2, image=img)
                        self.panel.image = img
                        self.panel.place(x=0, y=100)
                        self.switch_frame(self.frame2)
                    elif (graphsattributevariable.get() == 'violinplot'):
                        plt.figure(figsize=(20, 5))
                        if (hueattributevariable.get() == "select the hue attribute"):
                            sns_plot = sns.violinplot(self.dataframe[categoricattributevariable.get()],
                                                      self.dataframe[numericattributevariable.get()])
                        else:
                            attributeerrorlabel.set("hue attribute is choice")
                            sns_plot = sns.violinplot(self.dataframe[categoricattributevariable.get()],
                                                      self.dataframe[numericattributevariable.get()],
                                                      hue=self.dataframe[hueattributevariable.get()])
                        plt.savefig("violinplotoutput.jpg")
                        img = Image.open("violinplotoutput.jpg")
                        self.oldname.append("violinplotoutput.jpg")
                        img = img.resize((w, w // 3), Image.ANTIALIAS)
                        img = ImageTk.PhotoImage(img)
                        self.panel = Label(self.frame2, image=img)
                        self.panel.image = img
                        self.panel.place(x=0, y=100)
                        self.switch_frame(self.frame2)
                    elif (graphsattributevariable.get() == 'relplot'):
                        plt.figure(figsize=(20, 5))
                        if (hueattributevariable.get() == "select the hue attribute"):
                            sns_plot = sns.lineplot(self.dataframe[categoricattributevariable.get()],
                                                    self.dataframe[numericattributevariable.get()])
                        else:
                            attributeerrorlabel.set("hue attribute is choice")
                            sns_plot = sns.lineplot(self.dataframe[categoricattributevariable.get()],
                                                    self.dataframe[numericattributevariable.get()],
                                                    hue=self.dataframe[hueattributevariable.get()])
                        plt.savefig("relplotoutput.jpg")
                        img = Image.open("relplotoutput.jpg")
                        self.oldname.append("relplotoutput.jpg")
                        img = img.resize((w, w // 3), Image.ANTIALIAS)
                        img = ImageTk.PhotoImage(img)
                        self.panel = Label(self.frame2, image=img)
                        self.panel.image = img
                        self.panel.place(x=0, y=100)
                        self.switch_frame(self.frame2)

                    elif (graphsattributevariable.get() == 'swarmplot'):
                        plt.figure(figsize=(20, 5))
                        if (hueattributevariable.get() == "select the hue attribute"):
                            sns_plot = sns.swarmplot(self.dataframe[categoricattributevariable.get()],
                                                     self.dataframe[numericattributevariable.get()])
                        else:
                            attributeerrorlabel.set("hue attribute is choice")
                            sns_plot = sns.swarmplot(self.dataframe[categoricattributevariable.get()],
                                                     self.dataframe[numericattributevariable.get()],
                                                     hue=self.dataframe[hueattributevariable.get()])
                        plt.savefig("swarmplotoutput.jpg")
                        img = Image.open("swarmplotoutput.jpg")
                        self.oldname.append("swarmplotoutput.jpg")
                        img = img.resize((w, w // 3), Image.ANTIALIAS)
                        img = ImageTk.PhotoImage(img)
                        self.panel = Label(self.frame2, image=img)
                        self.panel.image = img
                        self.panel.place(x=0, y=100)
                        self.switch_frame(self.frame2)
                    elif (graphsattributevariable.get() == "piechart"):
                        plt.figure(figsize=(20, 20))
                        x = self.dataframe[categoricattributevariable.get()].unique()
                        y = self.dataframe.groupby(categoricattributevariable.get())[
                            numericattributevariable.get()].sum()
                        autotexts = plt.pie(y, labels=x, autopct='%1.1f%%', shadow=True, startangle=90,
                                            textprops={'size': 40})
                        plt.title(numericattributevariable.get() + ' across ' + numericattributevariable.get(),
                                  fontsize=40)
                        plt.axis("equal")
                        plt.legend(fontsize=20,
                                   loc="upper right", )
                        plt.savefig("pieplotoutput.jpg")
                        img = Image.open("pieplotoutput.jpg")
                        self.oldname.append("pieplotoutput.jpg")
                        img = img.resize((700, 700), Image.ANTIALIAS)
                        img = ImageTk.PhotoImage(img)
                        self.panel = Label(self.frame2, image=img)
                        self.panel.image = img
                        self.panel.place(x=w // 4, y=50)
                        self.switch_frame(self.frame2)

                else:
                    attributeerrorlabel.set("You need to select atleast two attributes rather than graph and hue")
        else:
            attributeerrorlabel.set("you must select the graph first")

root = Tk()
root.title("Data Visualization Tool")
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
root.geometry(str(w) + "x" + str(h))
filedescript = StringVar()
numericattributevariable = StringVar()
hueattributevariable = StringVar()
savefileattributevariable=StringVar()
categoricattributevariable = StringVar()
graphsattributevariable = StringVar()
attributeerrorlabel = StringVar()
buttontext = StringVar()
start = Mainpage(root)

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        #root.destroy()
        root.quit()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()





