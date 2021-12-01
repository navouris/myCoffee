# myCoffeeMaker - έκδοση 3 - κλάσεις
# στην έκδοση αυτή επίσης τα δεδομένα εισόδου, νομίσματα και ροφήματα περιέχονται σε εξωτερικά αρχεία

class Drink():
    '''κλάση για τα ροφήματα που προσφέρει η μηχανή'''
    panel = {} # μεταβλητή κλάσης για αναφορά στα ροφήματα
    def __init__(self, id, description, price):
        self.id = id
        self.description = description
        self.price = int(price)
        self.stats = {}
        Drink.panel[id] = self
    def buy(self):
        toPay = self.price
        print(f'Πρέπει να πληρώσετε {self.price/100:.2f}€')
        print('Δεκτά νομίσματα: ', end="")
        for coin, obj in Coin.cashier.items():
            print(f"{obj.description}, ", end="")
        print()
        while True:
            try:
                print(f'οφείλετε ακόμη {toPay/100:.2f}€')
                paid = float(input(f'Πληρωμή({",".join([f"{x/100:.2f}" for x in Coin.cashier.keys()])}):'))
                if paid in [x/100 for x in Coin.cashier.keys()]:
                    paid = int(paid*100)
                else: continue
            except: continue
            toPay -= paid
            if toPay <= 0: break # έχει πληρωθεί το ποσόν
        if toPay < 0:
            Coin.give_rest(-toPay) # επιστροφή ρέστων
        print('Απολαύστε το ρόφημά σας....')

class Coin():
    '''κλάση διαχείρισης των κερμάτων που πληρώνει ο χρήστης και επιστρέφει η μηχανή'''
    cashier = {}

    @staticmethod
    def give_rest(toReturn):
        '''υπολογίζει και πληροφορεί τον χρήστη για τα ρέστα του'''
        # TODO: να υλοποιήσουμε τη δυνατότητα ακύρωσης παραγγελίας ενώ γίνεται η πληρωμή
        if toReturn: 
            print(f'Παρακαλώ παραλάβετε {toReturn/100:.2f} ρέστα...')
            coinsToReturn = {} # collect coins to return
            for coin in sorted(Coin.cashier.keys(), reverse=True ):
                quantity = toReturn//coin
                if quantity : 
                    coinsToReturn[coin] = quantity
                    toReturn -= coin * quantity
                    if not toReturn: break
            # give the rest
            for c in coinsToReturn:
                print(f'ρέστα: {coinsToReturn[c]} x {c/100:.2f}€')

    def __init__(self, description, value, ammount=0):
        ''' assume infinite capacity'''
        self.description = description
        self.value = int(value)
        self.ammount = int(ammount)
        Coin.cashier[self.value] = self

class Controller():
    '''κεντρικός ελεγκτής της εφαρμογής, μόνο ένα στιγμιότυπο της κλάσης'''
    def __init__(self):
        self.loadDrinks('drinks.txt')
        self.loadCoins('coins.txt')
        self.run()
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
            print('Επιλέξτε ρόφημα:')
            for id,d in Drink.panel.items():
                print(f"{d.id}: {d.description} - Τιμή: {d.price/100:2.2f}€")
            print("0: Έξοδος")
            selection = input('Επιλογή:')
            if selection == "0": break
            if selection in Drink.panel.keys():
                selected = Drink.panel[selection]
                selected.buy()

if __name__ == "__main__": Controller()