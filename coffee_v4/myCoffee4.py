# myCoffeeMaker έκδοση 4, με χρήση κλάσεων και επέκταση των προδιαγραφών
# περιλαμβάνει: διαχείριση των μετρητών, στατιστικά πωλήσεων 
# υλοποίηση  undo σε οποιαδήποτε φάση της πληρωμής

import datetime

class Drink():
    panel = {}
    @staticmethod
    def printStats():
        print(10*'=', ' STATS  ', 10*'=')
        for id,drink in Drink.panel.items():
            stats = ", ".join([':'.join([x, str(drink.stats[x])]) for x in drink.stats])
            print(f"{drink.description}: {stats}")
        print(30*'=')

    def __init__(self, id, description, price):
        self.id = str(id)
        self.description = description
        self.price = int(price)
        self.stats = {}
        Drink.panel[self.id] = self

    def buy(self):
        # διαχείριση διαλόγου με τον χρήστη για πληρωμή του ροφήματος
        # υλοποιεί τη δυνατότητα ακύρωσης παραγγελίας ενώ γίνεται η πληρωμή

        def message(myrest):
            print('επιστροφή:')
            for r in sorted(myrest):
                print(f"{myrest[r]} x {r/100:.2f}€")

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
                # print(f'οφείλετε ακόμη {toPay/100:.2f}€')
                # υλοποίηση ακύρωσης πληρωμής σε οποιαδήποτε ενδιάμεση φάση
                reply = input(f'Πληρωμή({",".join([f"{x/100:.2f}" for x in Coin.cashier.keys()])}) ή x (cancel):')
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
            whatHappened = Coin.giveRest(self.price, self.paid)
            message(whatHappened[1])
        if whatHappened and whatHappened[0]: 
            print('Απολαύστε το ρόφημά σας....')
            today = datetime.datetime.now().strftime('%d-%m-%Y')
            self.stats[today] = self.stats.get(today, 0) + 1
            # ενημέρωση ταμείου 
            toUpdateCashier = {}
            for item in self.paid:
                toUpdateCashier[item] = toUpdateCashier.get(item,0) + 1
            for item in whatHappened[1]:
                toUpdateCashier[item] = toUpdateCashier.get(item,0) - whatHappened[1][item]
            print(toUpdateCashier)
            for coin in toUpdateCashier:
                Coin.cashier[coin].ammount += toUpdateCashier[coin]

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
    def giveRest(drinkPrice, paid):
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
            return (False, restCoins)

    def __init__(self, description, value, ammount):
        self.description = description
        self.value = int(value)
        self.ammount = int(ammount)
        Coin.cashier[self.value] = self

class Controller():
    def __init__(self):
        self.loadDrinks('drinks.txt')
        self.loadCoins('coins.txt')

    def loadDrinks(self, filename):
        for drink in open(filename, 'r', encoding='utf8'):
            drink = drink.strip().split(';')
            Drink(*drink)

    def loadCoins(self, filename):
        for coin in open(filename, 'r', encoding='utf8'):
            coin = coin.strip().split(';')
            Coin(*coin)
            
    def run(self):
        # κύριος βρόχος - μενού
        while True:
            Coin.printCashier() # coins left
            Drink.printStats() # στατιστικά πωλήσεων TODO: να αποθηκεύονται σε αρχείο
            print('Επιλέξτε ρόφημα:')
            for id,d in Drink.panel.items():
                print(f"{d.id}: {d.description} - Τιμή: {d.price/100:2.2f}€")
            print("0: Έξοδος")
            selection = input('Επιλογή:')
            if selection == "0": break
            if selection in Drink.panel.keys():
                selected = Drink.panel[selection]
                selected.buy()

# main program
if __name__ == "__main__": # τρέξε το πρόγραμμα από CLI
    loader = Controller()
    loader.run()