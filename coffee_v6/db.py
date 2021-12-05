import sqlite3

import os
DIR = os.path.dirname(__file__)

class DataModel():
    '''Κλάση σύνδεσης με τη βάση δεδομένων και δημιουργίας δρομέα'''
    def __init__(self, filename):
        self.filename = filename
        try:
            self.con = sqlite3.connect(filename)
            self.con.row_factory = sqlite3.Row  # ώστε να πάρουμε τα ονόματα των στηλών του πίνακα
            self.cursor = self.con.cursor()
            print("Επιτυχής σύνδεση στη βάση δεδομένων", filename)
            sqlite_select_Query = "select sqlite_version();"
            self.cursor.execute(sqlite_select_Query)
            record = self.cursor.fetchall()
            for rec in record:
                print("SQLite Database Version is: ", rec[0])
        except sqlite3.Error as error:
            print("Σφάλμα σύνδεσης στη βάση δεδομένων sqlite", error)

    def readTable(self, table, machine=""):
        '''Φόρτωμα ενός πίνακα, όταν το προαιρετικό όρισμα machine πάρει τιμή, τότε επιστρέφει μόνο 
        τις εγγραφές που αφορούν τη συγκεκριμένη μηχανή'''
        try:
            if machine:
                query = f'''SELECT * FROM {table} WHERE machineID = ?;'''
                self.cursor.execute(query, tuple([machine]))
            else:
                query = f'''SELECT * FROM {table};'''
                self.cursor.execute(query)
            records = self.cursor.fetchall()
            result = []
            for row in records:
                result.append(dict(row))
            return result
        except sqlite3.Error as error:
            print(f"Σφάλμα φόρτωσης πίνακα {table}", error)
    
    def _insertIntoTable(self, table, row_dict):
        ''' Εισαγωγή εγγραφής σε πίνακα'''
        try:
            query_param = f"""INSERT INTO {table} ({",".join(row_dict.keys())}) VALUES ({", ".join((len(row_dict)-1) * ["?"])}, ?);"""
            data = tuple(row_dict.values())
            self.cursor.execute(query_param, data)
            self.con.commit()
            return True
        except sqlite3.Error as error:
            print(f"Σφάλμα εισαγωγής στοιχείων στον πίνακα {table}", error)
            return False

    def _updateCapacity(self, value, quantity, machine):
        ''' ενημέρωση του πίνακα capacity'''
        try:
            query = f'''UPDATE capacity SET current = current + {quantity} WHERE value = {value} and machineID = (?);'''
            self.cursor.execute(query, tuple([machine]))
            self.con.commit()
            return True
        except sqlite3.Error as error:
            print(f"Σφάλμα φόρτωσης πίνακα capacity", error)     
            return False

    def insertPurchase(self, purchase) :
        ''' ενημέρωση σχετικά με αγορά 
        μετά από κάθε αγορά ροφήματος, θα πρέπει να γίνεται νέα εγγραφή στον 
        πίνακα buy, καθώς και νέες εγγραφές στον πίνακα insertCoins και ενημέρωση 
        του πεδίου current capacity.
        purchase = {'machine': id, 'drink': id, 'datetime': d, coins: {value: quantity, ... }}'''

        print('...', purchase)

        # αυτή είναι η βασική διεπαφή για καταχώρηση αγοράς προϊόντος

        # εισαγωγή στον πίνακα buy
        try:
            self._insertIntoTable("buy", {"machineid": purchase["machine"], 
                                        "datetime": purchase["datetime"],
                                        "productid": purchase["drink"],
                                        "cost" : sum([x*purchase["coins"][x] for x in purchase["coins"]]),
                                        })
            # εισαγωγές στον πίνακα insertCoins και ενημέρωση πίνακα capacity
            for coin in purchase["coins"]:
                self._insertIntoTable("insertCoins", {
                    "machineid": purchase["machine"],
                    "datetime": purchase["datetime"],
                    "coinvalue": coin,
                    "quantity": purchase["coins"][coin]
                })
                self._updateCapacity(coin, purchase["coins"][coin], purchase["machine"] )
            self.con.commit();
        except sqlite3.Error as error:
            print(f"Σφάλμα ενημέρωσης αγοράς", error)     
            return False

if __name__ == "__main__":
    ################ MYTESTS ########################
    dbfile = os.path.join(DIR, "db/myCoffee.db")
    #test 1: open db
    d = DataModel(dbfile)

    #test 2: ανάγνωση πινάκων
    for t in ['coin', 'product', 'coffeMachine' ]:
        print(t, d.readTable(t))
    
    #test 3: υλοποίηση δύο αγορών
    import datetime
    import time
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    d.insertPurchase({'machine': 1, 'drink': 1, 'datetime': dt, "coins": {200: 1, 50: -1}})
    time.sleep(10)
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    d.insertPurchase({'machine': 1, 'drink': 1, 'datetime': dt, "coins": {500: 1, 50: -1, 200:-1, 100:-1}})
    # purchase = {'machine': id, 'drink': id, 'datetime': d, coins: {value: quantity, ... }}'''

    #finally...: διάβασε τους πίνακες που έχουν αλλάξει
    for t in ['capacity', 'insertCoins', 'buy']:
        print(t, d.readTable(t, 1))