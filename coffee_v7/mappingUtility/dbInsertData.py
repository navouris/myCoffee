'''Εργαλείο για αρχικοποίηση της βάσης δεδομένων με βάση τα στοιχεία στα αρχεία greece.json που περιέχει
τα δεδομένα των μηχανών καφέ, και τα αρχεία coins.txt και drinks.txt
τυπώνει τις εντολές sql που μπορουν να χρησιμοποιηθούν για αρχικοποίηση της βάσης δεδομένων myCoffee7.db'''

maxCapacity = 10
import json
# διαγραφή των δεδομένων των πινάκων της βάσης
for table in ['buy', 'insertCoins', 'capacity', 'coffeMachine', 'coin', 'product']:
    print('delete from', table, ";")

# insert Coin data
out = f"INSERT INTO coin VALUES \n"
quantities = {}
for line in open('coins.txt', 'r', encoding='utf-8'):
    (description, value, quantity) = line.strip().split(";")
    out += f"({value}, '{description}'),"
    quantities[int(value)] = int(quantity)
print(out.rstrip(",")+";")
# insert Drink data
out = f"INSERT INTO product VALUES \n"
for line in open('drinks.txt', 'r', encoding='utf-8'):
    # 1;Καφές;150 
    (id, description, cost) = line.strip().split(';')
    out += f"({id}, '{description}', {cost}),"
print(out.rstrip(",")+";")
# insert coffeMachine data
file = 'greece.json'
with open(file, 'r', encoding='utf-8') as f:
    d = json.load(f)
out = f"INSERT INTO coffeMachine VALUES \n"
machines = []
for i, machine in enumerate(d):
    out += f"({i+1}, '{machine}', {d[machine]['x']}, {d[machine]['y']}),"
    machines.append(i+1)
print(out.rstrip(",")+";")

# insert capacity data
out = f"INSERT INTO capacity VALUES \n"
for machine in machines:
    for coin in quantities:
        out += f"({machine}, {coin}, {maxCapacity}, {quantities[coin]}),"
print(out.rstrip(",")+";")



