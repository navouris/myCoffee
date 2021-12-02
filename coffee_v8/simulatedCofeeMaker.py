# simulatedCofeeMaker (έκδοση 7) στηρίζεται στην έκδοση myCoffeeMaker έκδοση 4, 
# με τις εξής διαφορές: Δεν αλληλεπιδρά με τον χρήστη,αφού χρησιμοποιείται κλήση τυχαίων συμβάντων,
# επιλογής ροφήματος και πληρωμής, ενημερώνοντας τη βάση δεδομένων.
# Επίσης υλοποιεί κλήση της βάσης δεδομένω (με χρήση του db.py).
# όταν καλείται υλοποιεί τα συμβάντα μιας τυχαίας μέρας που ορίζεται κατά την κλήση και παράγει
# συνολικό report των συμβάντων της ημέρας. Για μελλοντική χρήση από ένα πρόγραμμα
# προσομοίωσης λειτουργίας πολλών μηχανών παράγει συνοπτική έκθεση της ημέρας, με 
# στοχεία όπως το ταμειακό υπόλοιπο της μέρας, το συνολικό κέρδος, σύνολο πωλήσεων και
# σύνολο αποτυχημένων πωλήσεων (περιπτώσεις που δεν είχε η μηχανή να δώσει ρέστα).

import random
import db

DATABASE_FILE = "myCoffee8.db"

class Drink():
    panel = {}
    def __init__(self, id, description, price, machineID):
        self.id = str(id)
        self.description = description
        self.price = int(price)
        self.machineID = machineID
        Drink.panel[self.id] = self

    def buy(self):
        # διαχείριση διαλόγου με τον χρήστη για πληρωμή του ροφήματος
        # υλοποιεί τη δυνατότητα ακύρωσης παραγγελίας ενώ γίνεται η πληρωμή

        def message(myrest):
            print('επιστροφή:')
            for r in sorted(myrest):
                if myrest[r]: print(f"{myrest[r]} x {r/100:.2f}€")
        
        def f(a,b): return f"{str(random.randint(a,b)).zfill(2)}"

        whatHappened = None
        self.paid = []
        toPay = self.price
        print(f'Πρέπει να πληρώσετε {self.price/100:.2f}€')
        print('Δεκτά νομίσματα: ', end="")
        for coin, obj in Coin.cashier.items():
            print(f"{obj.description}, ", end="")
        print()
        while True: # διαδικασία πληρωμής
            try:
                print(f'οφείλετε ακόμη {(self.price-sum(self.paid))/100:.2f}€')
                # υλοποίηση ακύρωσης πληρωμής σε οποιαδήποτε ενδιάμεση φάση
                # reply = input(f'Πληρωμή({",".join([f"{x/100:.2f}" for x in Coin.cashier.keys()])}) ή x (cancel):')
                reply = random.choice(['0.5', '0.2', '0.1', '1', '2', '5'])
                if reply.lower() == 'x':
                    # to return coins self.price - toPay
                    whatHappened = (False, dict([(x, self.paid.count(x)) for x in self.paid]))
                    message(whatHappened[1])
                    toPay = 0
                    break
                else:
                    paid = float(reply)
                    if paid in [x/100 for x in Coin.cashier.keys()]:
                        paid = int(paid*100)
                        self.paid.append(paid)
                    else: continue
            except: continue
            toPay -= paid
            if toPay <= 0: break # έχει πληρωθεί το ποσόν

        if toPay < 0:
            whatHappened = Coin.giveRest(self.price, self.paid, self.machineID)
            message(whatHappened[1])
        if whatHappened and whatHappened[0]: 
            print('Απολαύστε το ρόφημά σας....')
            ### add to database
            ######## αποθήκευση της αγοράς στη βάση δεδομένων ##################
            timestamp = self.machineID.date + f" {f(0,23)}:{f(0,59)}:{f(0,59)}"
            purchase = {'machine': self.machineID.id, 'datetime': timestamp, \
                'drink': self.id, 'coins' :{}}
            for item in self.paid:
                purchase['coins'][item] = purchase['coins'].get(item,0) + 1
            for item in whatHappened[1]:
                purchase['coins'][item] = purchase['coins'].get(item,0) - whatHappened[1][item]
            print(purchase)
            self.machineID.db.insertPurchase(purchase)
            ########### ενημέρωσε το ταμείο  ################################
            for coin in purchase['coins']:
                Coin.cashier[coin].ammount += purchase['coins'][coin]
            self.machineID.reporting()

class Coin():
    cashier = {}

    @staticmethod
    def printCashier():
        print(10*'=', 'CASHIER', 10*'=')
        total = 0
        for val,coin in Coin.cashier.items():
            print(f"{coin.description}: {coin.ammount}")
            total += val * coin.ammount
        print(f'TOTAL {total/100:5.2f}€')
        print(30*'=')
    
    @staticmethod
    def giveRest(drinkPrice, paid, machine):
        '''μέθοδος που για ορισμένο ποσό που πρέπει να πληρωθεί (drinkPrice), ελέγχει αν έχει
        ρέστα να δώσει, αν ναι, παραλαμβάνει τα νομισματα της λίστας paid, και επιστρέφει τα ρέστα
        αν όχι, επιστρέφει τα νομίσματα της paid και στέλνει αντίστοιχο μήνυμα, ότι δεν προχωράει
        η αγορά επιστρέφει (True/False, restCoins)'''
        
        toReturn = sum(paid) - drinkPrice # το ποσό που πρέπει να επιστραφεί
        if toReturn < 0:
            return (False, {}) # αγορά δεν έγινε, η δοσοληψία είναι σε εξέλιξη (όχι αρκετά χρήματα)
        if toReturn == 0:
            return (True, {})
        # προσωρινή κατάσταση ταμείου αν προστεθούν και τα χρήματα που μόλις πήραμε
        tempCashier = {}
        for coin in Coin.cashier:
            tempCashier[coin] = Coin.cashier[coin].ammount
        for coin in paid:
            tempCashier[coin] += 1
        
        # έλεγχος αν μπορούμε να δώσουμε ρέστα
        restCoins = {}
        for coin in sorted(tempCashier.keys(), reverse=True ):
            quantity = toReturn//coin
            if quantity :
                if tempCashier[coin] >= quantity:
                    restCoins[coin] = quantity
                else:
                    restCoins[coin] = tempCashier[coin]
                toReturn -= coin * restCoins[coin]
                if not toReturn: # βρέθηκαν ρέστα
                    return (True, restCoins)
        else: # δεν βρέθηκαν ρέστα
            print('undo.... δεν υπάρχουν ρέστα, πληρώστε ακριβές ποσό.')
            restCoins = {}
            for coin in paid:
                restCoins[coin] = restCoins.get(coin, 0) + 1
            machine.report['fail'] += 1
            return (False, restCoins)

    def __init__(self, description, value, ammount):
        self.description = description
        self.value = int(value)
        self.ammount = int(ammount)
        Coin.cashier[self.value] = self

class Controller():
    def __init__(self, newDate, id):
        self.db = db.DataModel(DATABASE_FILE)
        self.id = id
        self.loadData()
        self.report = {'sales':0, 'cash':0, 'drinks':0, 'fail':0}
        self.date = newDate
        self.reporting("ΑΡΧΙΚΟ")
        self.run()
        self.reporting("ΤΕΛΙΚΟ")
        
    def loadData(self):
        '''φόρτωμα των δεδομένων από τη βάση δεδομένων'''
        result = self.db.readTable('product')
        for drink in result:
            Drink(*drink.values(), self)
        coins = self.db.readTable('coin')
        capacity = self.db.readTable('capacity', machine= self.id)
        for coin in coins:
            ammount = [x['current'] for x in capacity if x['value'] == coin['value']]
            if ammount: Coin(description = coin['description'], value=coin['value'], ammount= ammount[0])
            else: 
                print('Error in data, abort')
                exit()
    def reporting(self, txt=""):
        ########### Καταγραφή κατάστασης από τη βάση δεδομένων ####
        print(20*"=", txt, 25*"=")
        report = self.db.readTable('capacity', machine=self.id)
        out = f'ΤΑΜΕΙΟ - κλείσιμο ημέρας {self.date} ΜΗΧΑΝΗ: {self.id} \n'
        cash = 0
        for item in report:
            out += f"{Coin.cashier[item['value']].description}\t {item['current']}\n"
            cash += item['value']*item['current']
        out +=  f"ΣΥΝΟΛΟ ΤΑΜΕΙΟΥ ημέρας {self.date} ΜΗΧΑΝΗ {self.id} ΕΙΝΑΙ: {cash/100:.2f}"
        self.report['cash'] = cash/100
        print(out)
        report = self.db.readTable('buy', machine=self.id)
        Coin.printCashier()
        if txt:
            total = 0
            drinks = 0
            out = f'\nSALES Report Μηχανής {self.id} Ημέρα: {self.date}\n'
            for item in report:
                if self.date in item['datetime']:
                    out += f"{item['datetime']}\t{Drink.panel[str(item['productid'])].description}\t{item['cost']/100:.2f}€\n"
                    total += item['cost']
                    drinks += 1
            out += f"ΣΥΝΟΛΟ ΠΩΛΗΣΕΩΝ ημέρας {self.date} ΜΗΧΑΝΗ {self.id} EINAI: {total/100:.2f}€\n\n"
            self.report['sales'] = total/100
            self.report['drinks'] = drinks
            print(out)
        if txt == "ΤΕΛΙΚΟ": 
            print("Τελική έκθεση")
            for i,k in self.report.items():
                print(i,"\t", k)
        print(50*"=")


    def run(self):
        # κύριος βρόχος - μενού
        numberDrinks = random.randint(10,50) #sell between 10 and 50 drinks daily
        for _i in range(numberDrinks):
            print('Επιλέξτε ρόφημα:')
            for id,d in Drink.panel.items():
                print(f"{d.id}: {d.description} - Τιμή: {d.price/100:2.2f}€")
            print("0: Έξοδος")
            # selection = input('Επιλογή:')
            selection = random.choice(['1', '2', '3', '4'])
            if selection == "0": break
            if selection in Drink.panel.keys():
                selected = Drink.panel[selection]
                selected.buy()
        
# main program
if __name__ == "__main__": # τρέξε το πρόγραμμα από CLI
    loader = Controller('1821-03-25', 1)