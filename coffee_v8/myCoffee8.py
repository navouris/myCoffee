# myCoffee v.8 προσομοίωση λειτουργίας επιχείρησης
# περιλαμβάνει ασύγχρονη εκτέλεση της προσομοίωσης
# επιλογή χρόνου (ημερομηνίας, αριθμού ημερών)
# παρουσίαση αποτελεσμάτων

import tkinter as tk
from tkinter import ttk
import datetime
import threading
import time
from tkcalendar import Calendar
from tkinter import simpledialog
from tkinter import messagebox
import json
import os
import db
import simulatedCofeeMaker as sim

DIR = os.path.dirname(__file__)

months = {1:"ΙΑΝ", 2:"ΦΕΒ", 3:"ΜΑΡ", 4:"ΑΠΡ", 5:"ΜΑΙ", 6:"ΙΟΥΝ", 7:"ΙΟΥΛ",
        8:"ΑΥΓ", 9:"ΣΕΠ", 10:"ΟΚΤ", 11:"ΝΟΕ", 12:"ΔΕΚ"}

def myPath(f): return os.path.join(DIR, f) # βοηθητική συνάρτηση αναφοράς στο DIR

### the map
theMap = myPath('greece.png')
DATABASE = myPath("myCoffee8.db")
backColor = "#ffe300"
padding = 5
###
# copy map from https://www.openstreetmap.org/#map=10/38.2444/21.4207&layers=T

class Map(tk.Frame):
    def __init__(self, map):
        tk.Frame.__init__(self)
        self.date = datetime.datetime.now()
        self.simulation = []
        self.report = {}
        self.simDate = None
        self.shownMachine = None
        self.animate = False
        self.pack(expand=True, fill='both')
        self.img = tk.PhotoImage(file=map)
        self.coffeImg = tk.PhotoImage(file = myPath('myCoffee.gif'))
        self.play = tk.PhotoImage(file=myPath('play1.gif'))
        self.canvas = tk.Canvas(self, width=self.img.width(), height=self.img.height())
        self.canvas.pack(expand=True)
        self.canvas.create_image(0,0, image=self.img, anchor='nw')
        self.base = tk.PhotoImage(file=myPath('base.gif'))
        self.canvas.create_image(self.img.width()-self.base.width(), -padding, \
            image=self.base, anchor='nw')
        self.playMenu = self.canvas.create_image(self.img.width()-self.play.width()-2*padding,\
            2*padding, image=self.play, anchor='nw')
        self.canvas.tag_bind(self.playMenu,'<Button-1>', lambda e: self.setSimulation(e))
        self.resetImg = tk.PhotoImage(file=myPath('reset1.gif'))
        self.resetMenu = self.canvas.create_image(self.img.width()-self.play.width() - self.resetImg.width()-4*padding,\
            2*padding, image=self.resetImg, anchor='nw')
        self.canvas.tag_bind(self.resetMenu,'<Button-1>', lambda e: self.resetDB(e))
        self.settingsImg = tk.PhotoImage(file=myPath('settings1.gif'))
        self.settingsMenu = self.canvas.create_image(self.img.width()-self.play.width()-self.settingsImg.width()- \
            self.resetImg.width()-6*padding, 2*padding, image=self.settingsImg, anchor='nw')
        self.frameCnt = 10
        self.workingImg = [tk.PhotoImage(file=myPath('settings2.gif'),format = 'gif -index %i' %(i)) for i in range(self.frameCnt)]
        self.dateImg = tk.PhotoImage(file=myPath('dateBox.gif'))
        self.dateMenu = self.canvas.create_image(2*padding, 2*padding, image=self.dateImg, anchor='nw')
        self.canvas.bind('<Button-1>', lambda e: self.showMachine(e))
        self.showDate()
        self.db = db.DataModel(DATABASE)
        self.readMachines()
        self.showMyCoffee()
    
    def resetDB(self, e):
        try:
            f = open(myPath('resetDB.sql'), 'r', encoding='utf-8')
            query = f.read()
            if self.db.executeSQL(query):
                messagebox.showerror('Επιτυχία', "Επιτυχής επαναφορά δεδομένων προσομοίωσης")
            else: messagebox.showinfo('Προσοχή', "Σφάλμα επαναφοράς δεδομένων προσομοίωσης")
        except:
            messagebox.showerror('Προσοχή', "Σφάλμα επαναφοράς δεδομένων προσομοίωσης")
    
    def showDate(self, date=None):
        if date:
            self.date = date
        d = f"{self.date.day}-{months[self.date.month]}-{self.date.year}"
        if not self.simDate:
            self.simDate = self.canvas.create_text(padding*4, padding*6, text=d, font="Helvetica 40", \
                fill='black', anchor='nw')
        else:
            self.canvas.itemconfig(self.simDate, text=d)

    def selectDate(self, e):
        today = self.date
        def handleDate():
            self.showDate(cal.selection_get())
            self.cal.destroy()
        self.cal = tk.Toplevel(root)
        cal = Calendar(self.cal, font="Arial 20", selectmode='day', locale='el',
            year=today.year, month=today.month, day=today.day)
        cal.pack(fill="both", expand=True)
        ttk.Button(self.cal, text="ok", command=handleDate).pack()

    def showMyCoffee(self):
        self.mapping = {}
        for id,machine in self.machines.items():
            self.mapping[id] = self.canvas.create_image(machine['x'], machine['y'], image = self.coffeImg)
            self.canvas.create_text(machine['x'], machine['y']-35, text=machine["place"], fill='red')

    def readMachines(self):
        self.machines = {}
        machines = self.db.readTable('coffeMachine')
        for item in machines:
            self.machines[item['id']] = {'place':item['place'], 'x':item['coordX'], 'y':item['coordY']}

    def setSimulation(self, e):
        print('we will run a simulation from date', self.date.strftime("%d-%m-%Y"))
        reply = simpledialog.askinteger(\
            title = 'Προσομοίωση λειτουργίας...', \
            prompt = f"Για πόσες μέρες θα θέλατε να τρέξει η \nπροσομοίωση λειτουργίας;\n" +
                    f"Αρχική ημερομηνία: {self.date.strftime('%d-%m-%Y')},  (1-20 μέρες)")
        if reply and 1 <= reply <= 20:
            self.simulation = []
            self.report = {}
            for i in range(reply):
                self.simulation.append(self.date + datetime.timedelta(i))
            yes = messagebox.askyesno(title="Ημερομηνίες προσομοίωσης λειτουργίας",
            message="Η προσομοίωση λειτουργίας θα γίνει για τις εξής μέρες, συμφωνείτε;",
            detail="\n".join(d.strftime("%d-%m-%Y") for d in self.simulation))
            print(yes)
            if yes: 
                threading.Thread(target=self.runSimulation).start() #ξεκινάμε ένα ξεχωριστό νήμα που τρέχει τον προσομοιωτή
            else: self.simulation = []; self.report = {}
        else:
            if reply != None:
                messagebox.showerror(title = 'Προσομοίωση λειτουργίας...', \
                message="Παρακαλώ δώστε έγκυρο αριθμό ημερών προσμοίωσης")
    
    def runSimulation(self):
        # δείξε κίνηση στο γρανάζι...
        self.animate = True
        threading.Thread(target=self.animateSimulration).start() #ξεκίνα κίνηση γραναζιού
        for day in self.simulation:
            for machine in self.machines:
                if machine not in self.report: self.report[machine] = {}
                machineRun = sim.Controller(day.strftime("%Y-%m-%d"), machine)
                self.report[machine][day.strftime("%Y-%m-%d")] = machineRun.report
        self.animate = False
        self.canvas.itemconfig(self.settingsMenu, image=self.settingsImg)

    def animateSimulration(self, ind=0):
        if not self.animate: return False
        print(ind)
        frame = self.workingImg[ind]
        ind += 1
        if ind == self.frameCnt:
            ind = 0
        self.canvas.itemconfig(self.settingsMenu, image=frame)
        root.after(100, self.animateSimulration, ind)

    def showMachine(self, e):
        print(e.x, e.y)
        selected = self.canvas.find_withtag("current")
        print(selected)
        if selected:
            for m in self.mapping:
                if self.mapping[m] == selected[0]:
                    self.showMachineResults(m)
                    print (self.machines[m]['place'])
                    return
            if selected[0] == self.simDate:
                self.selectDate(e)

    def showMachineResults(self, m):
        if self.report:
            out = f"Κατάσταση μηχανής:{self.machines[m]['place']}\n{45*'-'}\nΗμερομηνία  Ταμείο  Πωλήσεις  Ποτά  Αποτυχίες\n"
            for d in sorted(self.report[m]):
                print(d, self.report[m][d])
                out += f"{d} {self.report[m][d]['cash']:8.2f}  {self.report[m][d]['sales']:5.2f}   {self.report[m][d]['drinks']:5d}   {self.report[m][d]['fail']:6d}\n"
        else:
            out = f"Δεν υπάρχουν δεδομένα προσομοίωσης λειτουργίας της μηχανής"
        if self.shownMachine in self.canvas.find_all():
            self.canvas.delete(self.shownMachine)
        self.shownMachine = self.canvas.create_text(200,200, anchor='nw', text=out, justify='left', font='Courier 20')
        self.canvas.tag_bind(self.shownMachine, "<1>", lambda e: self.canvas.delete(self.shownMachine))

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(0,0)
    root.title("MyCoffeeMaker v.8")
    greece = Map(theMap)
    root.mainloop()
