# myCoffee έκδοση 6. επέκταση της έκδοσης 5 με χρήση της βάσης δεδομένων (η διεπαφή βρίσκεται στο αρχείο db.py)

import tkinter as tk
import datetime as dt
import sys
import os

DIR = os.path.dirname(__file__)

def myPath(f): #βοηθητική συνάρτηση για σχετικό μονοπάτι προς τον φάκελο DIR του αρχείου
    return os.path.join(DIR,f)

sys.path.insert(1, myPath('../coffee_v4'))
import myCoffee4 as cv # εισάγουμε τις κλάσεις Drink και Coin
import db # εισάγουμε την κλάση σύνδεσης με τη βάση δεδομένων (αρχείο db.py)

DEBUG = True

class Coin(cv.Coin):
    coords = {'5€': [15, 265, 48,300],
            '2€': [53, 265, 90, 300],
            '1€': [95, 265, 165, 300],
            '.50€': [135, 265, 170, 300],
            '.20€': [175, 265, 207, 295],
            '.10€': [213, 265, 245, 295]}

    def __init__(self, description, value, ammount):
        cv.Coin.__init__(self, description, value, ammount )
        self.coords = Coin.coords[description]

class CofeeMaker():
    def __init__(self, root, id):
        ### φόρτωμα στοιχείων από τη βάση δεδομένων
        self.id = id
        self.db = db.DataModel(myPath("db/myCoffee.db"))
        self.loadData()

        self.welcome = 'Επιλέξτε ρόφημα...'
        self.drink = tk.PhotoImage(file=myPath('drink.gif'))
        self.cup = None # δεν υπάρχει ρόφημα
        self.drinkSelected = None
        self.paid = []
        self.root = root
        self.root.title('CoffeeMaker v.6')
        self.canvas = tk.Canvas(self.root, width=300, height=525 )
        self.canvas.pack()
        self.img = tk.PhotoImage(file=myPath('coffeemaker3.gif'))
        self.canvas.create_image(0,0, image=self.img, anchor='nw')
        self.canvas.create_rectangle(30,15, 260, 50, fill='black', outline='grey')
        self.panel = self.canvas.create_text(35,20, anchor='nw', font='TkMenuFont 18', fill='lightgreen')
        self.restPanel = self.canvas.create_text(230, 307, anchor='nw', font='TkMenuFont 10', fill='lightyellow')
        self.message(self.welcome)
        self.canvas.bind('<Button-1>', lambda e: self.handleClick(e))
        self.defineDrinksCancelAreas()
    
    def loadData(self):
        '''φόρτωμα των δεδομένων από τη βάση δεδομένων'''
        result = self.db.readTable('product')
        for drink in result:
            cv.Drink(*drink.values())
        coins = self.db.readTable('coin')
        capacity = self.db.readTable('capacity', machine= self.id)
        for coin in coins:
            ammount = [x['current'] for x in capacity if x['value'] == coin['value']]
            if ammount: Coin(description = coin['description'], value=coin['value'], ammount= ammount[0])
            else: 
                print('Error in data, abort')
                exit()

    def defineDrinksCancelAreas(self):
        ''' όρισε τις περιοχές ροφημάτων και την περιοχή 'ακυρο' που ο χρήστης μπορεί να επιλέξει'''
        drinkSize = 70
        self.drinks = {'1':{'coords':[55, 65, 55+drinkSize, 65+drinkSize],
                        'img':tk.PhotoImage(file=myPath("1.gif"))},
                        '2': {'coords':[160, 65, 160+drinkSize, 65+drinkSize],
                        'img':tk.PhotoImage(file=myPath("2.gif"))},
                        '3': {'coords':[55, 145, 55+drinkSize, 145+drinkSize],
                        'img':tk.PhotoImage(file=myPath("3.gif"))},
                        '4': {'coords':[160, 145, 160+drinkSize, 145+drinkSize],
                        'img':tk.PhotoImage(file=myPath("4.gif"))}}
        self.cancel =   [250, 265, 282, 295 ]

        for d in self.drinks:
            self.drinks[d]['area'] = self.canvas.create_image(*self.drinks[d]['coords'][:2], \
                image=self.drinks[d]['img'], anchor='nw')
            # self.drinks[d]['area'] = self.canvas.create_rectangle(*self.drinks[d]['coords'], fill='', outline='yellow')
            self.canvas.tag_bind(self.drinks[d]['area'], "<Button-1>", lambda e: self.selectedDrink(e))
        print(self.drinks)

    def selectedDrink(self, event):
        '''έλεγξε αν έχει επιλεγεί ρόφημα'''
        if self.cup: return # δεν επιτρέπεται η επιλογή αν το κύπελο δεν έχει απομακρυνθεί
        print(event)
        # current : https://stackoverflow.com/questions/7602122/how-to-get-the-tag-of-a-shape-when-clicked?rq=1
        self.drinkSelected = cv.Drink.panel [str(event.widget.find_withtag('current')[0] - 4 )]# the drinks start from 3
        msg = f"{self.drinkSelected.description}: {self.drinkSelected.price/100:.2f}€" 
        print(msg)
        self.message(msg)
        self.calculateBalance()
     
    def showRest(self, coins):
        '''εμφάνισε τα ρέστα προς επιστροφή στην περιοχή (rest)'''
        self.clearRest()
        if not coins: return
        toShow = '...ρέστα\n'
        for r in sorted(coins, reverse=True):
            if coins[r]: toShow += f"{coins[r]} x {r/100:.2f}€\n"
        print(toShow)
        self.canvas.itemconfig(self.restPanel, text=toShow) 
    
    def clearRest(self):
        '''καθάρισε την περιοχή (rest) από πληροφορία'''
        self.canvas.itemconfig(self.restPanel, text="") 
        
    def showDrink(self):
        '''εμφάνισε το κύπελο με το ρόφημα'''
        print('showDrink')
        self.cup = self.canvas.create_image(110, 370,  image=self.drink, anchor='nw') # 335, 90
        self.canvas.tag_bind(self.cup, "<Button-1>", lambda e: self.drinkit())

    def drinkit(self):
        '''όταν επιλεγεί το κύπελο με το ρόφημα, σβήσε το και επανάφερε τη μηχανή στην αρχική κατάσταση'''
        self.drinkSelected = None
        self.canvas.delete(self.cup)
        self.cup = None
        self.message(self.welcome)
        self.clearRest()

    def calculateBalance(self):
        ''' Έλεγξε αν έχει πληρωθεί το ποσό ώστε το ρόφημα να μπορεί να σερβιριστεί ''' 
        msg = ''
        print(self.paid, self.drinkSelected.price if self.drinkSelected else "")
        paid = sum([x.value for x in self.paid])
        if not paid: return
        if not self.drinkSelected: # no drink selected yet
            msg = f'Πληρωμή:{paid/100:.2f}'
        else: 
            toReturn = paid - self.drinkSelected.price
            if toReturn >= 0:
                msg = f'επιστροφή: {toReturn/100:.2f} '
                whatHappened = cv.Coin.giveRest(self.drinkSelected.price, [x.value for x in self.paid])
                print(whatHappened[1]) 
                self.showRest(whatHappened[1])
                if whatHappened[0]: # αν πληρώθηκε οκ το ποσό δώσε το ρόφημα
                    self.showDrink()
                    # αποθήκευση της αγοράς στη βάση δεδομένων ##################
                    purchase = {'machine': self.id, 'datetime': dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), \
                        'drink': self.drinkSelected.id, 'coins' :{}}
                    for item in self.paid:
                        purchase['coins'][item.value] = purchase['coins'].get(item.value,0) + 1
                    for item in whatHappened[1]:
                        purchase['coins'][item] = purchase['coins'].get(item,0) - whatHappened[1][item]
                    print(purchase)
                    self.db.insertPurchase(purchase)
                    ############################################################
                    # ενημέρωση ταμείου 
                    toUpdateCashier = {}
                    for item in self.paid:
                        toUpdateCashier[item.value] = toUpdateCashier.get(item.value,0) + 1
                    for item in whatHappened[1]:
                        toUpdateCashier[item] = toUpdateCashier.get(item,0) - whatHappened[1][item]
                    print(toUpdateCashier)
                    for coin in toUpdateCashier:
                        cv.Coin.cashier[coin].ammount += toUpdateCashier[coin]
                else:
                    self.drinkSelected = None
                    msg = "πληρώστε ακριβές ποσό"
                self.paid = []
                
            elif toReturn < 0: 
                msg = f'Τιμή:{self.drinkSelected.price/100:.2f}€, ακόμη {-toReturn/100:.2f}€'
        self.message(msg)

    def handleClick(self, event):
        '''έλεγχος αν επιλέχτηκε νόμισμα ή το πλήκτρο "cancel"'''
        if DEBUG:
            cv.Coin.printCashier()
            cv.Drink.printStats()
            ########### Καταγραφή κατάστασης από τη βάση δεδομένων ####
            report = self.db.readTable('capacity', machine=self.id)
            print('CASHIER Report')
            for item in report:
                print(Coin.cashier[item['value']].description, item['current'])
            report = self.db.readTable('buy', machine=self.id)
            print('SALES Report')
            for item in report:
                print(item['datetime'], cv.Drink.panel[str(item['productid'])].description, f"{item['cost']/100:.2f}€")
            ####################### τέλος καταγραφής  ###############
        if self.cup: return # αν δεν πάρεις το ποτό δεν έχει νόημα να πληρώνεις άλλο...
        # βοηθητική συνάρτηση για έλεγχο περιοχής εντός ορθογωνίου rect
        def checkPoint(x,y, rect):
            if rect[0] < x < rect[2] and rect[1] < y < rect[3] : return True
            return False

        # έλεγχος αν πατήθηκε κάποιο νόμισμα
        for c,coin in Coin.cashier.items():
            if checkPoint(event.x, event.y, coin.coords): # έχει πληρωθεί ένα νόμισμα
                self.paid.append(coin)
                self.calculateBalance()
                return

        # έλεγχος αν πατήθηκε το "cancel"       
        if checkPoint(event.x, event.y, self.cancel): 
            whatHappened = cv.Coin.giveRest(0, [x.value for x in self.paid], True)
            self.showRest(whatHappened[1])
            print(whatHappened[1]) 
            self.drinkSelected = None
            returned_coins = sum([x.value for x in self.paid])
            self.paid = []
            self.message(f"επιστροφή {returned_coins/100:.2f}")
            return True
        return False

    def message(self, txt):
        '''εμφανίζει το μήνυμα txt στην οθόνη (panel)'''
        self.canvas.itemconfig(self.panel, text=txt) 
        print(txt)
       
if __name__ == '__main__':
    root = tk.Tk()
    myCoffee = CofeeMaker(root, id='1')
    tk.mainloop()