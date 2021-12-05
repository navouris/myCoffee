# myCoffeeMaker - έκδοση 2 - συναρτήσεις και λίστες/λεξικά

drinks = {
    '1': ['Καφές: 1.50 €', 150],
    '2': ['Καφές με γάλα: 1.80 €', 180],
    '3': ['Σοκολάτα: 2.10 €', 210],
    '4': ['Σοκολάτα με γάλα: 2.40 €', 240]
}
currencies = [10, 20, 50, 100, 200, 500] # accepted coins/notes

def menu():
    '''βασικό μενού επιστρέφει ως ακέραιο την επιλογή του χρήστη'''
    print(30*"_")
    for drink in drinks:
        print(drink, drinks[drink][0])
    print("0", "Έξοδος")
    print(30*"_")
    while True:
        reply = input("Επιλέξτε ρόφημα (1-4) ή 0 για έξοδο: ")
        if reply in drinks.keys() or reply == '0': break
    return reply

def process_payment(selection):
    '''μηχανισμός πληρωμής με βάση την επιλογή του χρήστη'''
    # msg_currencies = '\nΠαρακαλώ εισάγετε .10, .20, .50, 1, 2, 5 :'
    msg_currencies = '\nΠαρακαλώ εισάγετε '
    for currency in sorted(currencies):
        msg_currencies += f"{currency/100:.2f}, "
    msg_currencies = msg_currencies.rstrip(", ") + "€ :"
    to_pay = drinks[selection][1]
    print(f'\nΈχει παραγγελθεί: {drinks[selection][0]}\n')
    while True:
        try:
            new_payment = int(float(input(msg_currencies))*100)
        except ValueError:
            # print('Προσοχή επιλέξτε αποδεκτά νομίσματα')
            continue
        if new_payment in currencies:
            to_pay -= new_payment
            if to_pay > 0:
                print(f"Πρέπει να πληρώσετε {to_pay/100:.2f}€ ακόμη")
            else: break
    manage_rest(-to_pay)

def manage_rest(rest, cancel=False):
    '''υπολογίζει και πληροφορεί τον χρήστη για τα ρέστα του'''
    # TODO: να υλοποιήσουμε τη δυνατότητα ακύρωσης παραγγελίας ενώ γίνεται η πληρωμή
    if rest: 
        print(f'Παρακαλώ παραλάβετε {rest/100:.2f} ρέστα...')
        reverse_sorted_currencies = sorted(currencies, reverse=True )
        for currency in reverse_sorted_currencies[:-1]:
            quantity = rest//currency
            if quantity: 
                print(f'ρέστα: {quantity} x {currency/100:.2f}€')
                rest -= quantity * currency
                if not rest: break
    if not cancel: print('\nΑπολαύστε το ρόφημά σας...')

##  κυρίως πρόγραμμα 
if __name__ == "__main__":
    while True:
        user_selection = menu()
        if user_selection == "0": break
        process_payment(user_selection)