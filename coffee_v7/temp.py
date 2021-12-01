def giveRest(drinkPrice, paid):
    '''μέθοδος που για ορισμένο ποσό που πρέπει να πληρωθεί (drinkPrice), ελέγχει αν έχει
    ρέστα να δώσει, αν ναι, παραλαμβάνει τα νομισματα της λίστας paid, και επιστρέφει τα ρέστα
    αν όχι, επιστρέφει τα νομίσματα της paid και στέλνει αντίστοιχο μήνυμα, ότι δεν προχωράει
    η αγορά, αν justReturn, αγνοεί την τιμή του ποτού και απλά επιστρέφει τα νομίσματα στο paid
    επιστρέφει (True/False, restCoins)'''
    
    toReturn = sum(paid) - drinkPrice # το ποσό που πρέπει να επιστραφεί
    if toReturn < 0:
        return (False, {}) # αγορά δεν έγινε, η δοσοληψία είναι σε εξέλιξη (όχι αρκετά χρήματα)
    if toReturn == 0:
        return (True, {})
    # προσωρινή κατάσταση ταμείου αν προστεθούν και τα χρήματα που μόλις πήραμε
    tempCashier = {
        10: 1,
        20: 1,
        50: 0,
        100: 1,
        200: 2,
        500: 5,
    }
    
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

print(giveRest(150, [10, 10, 20, 50, 100, 100, 200]))