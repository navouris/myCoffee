# myCoffeeMaker - έκδοση 1

# ερώτημα (α)
choice = -1 # αρχικοποίηση επιλογής
while ( choice < 0 or choice > 4): # εμφάνιση επιλογών
    print(" Δίνονται οι παρακάτω επιλογές:")
    print(" 1. Καφές: 1.5 ευρώ")
    print(" 2. Καφές με γάλα: 1.8 ευρώ")
    print(" 3. Σοκολάτα: 2.1 ευρώ")
    print(" 4. Σοκολάτα με γάλα: 2.4 ευρώ")
    print(" 0. Έξοδος")
    reply = input("Παρακαλώ εισάγετε την επιλογή σας (1-4) ή πατήστε 0 για έξοδο: ") # είσοδος επιλογής
    if len(reply) == 1 and reply in "01234": choice = int(reply)

# ερώτημα (β)
if (choice != 0 ):
    if (choice == 1 ):
        antitimo = 150
    elif (choice == 2 ):    
        antitimo = 180
    elif (choice == 3 ):
        antitimo = 210
    elif (choice == 4 ):
        antitimo = 240
    poso = 0    # αρχικοποίηση
    while (poso < antitimo):    # αρχικοποίηση
        ikerma=0
        while (ikerma != 10 and ikerma != 20 and ikerma != 50 and ikerma != 100 and ikerma != 200 and ikerma != 500 ):
            print("Πρέπει να εισάγετε","{:3.1f}".format((antitimo - poso)/100),"ευρώ συνολικά")
            while True:
                try:
                    kerma = float(input("Πόσα εισάγετε; "))
                    break
                except:
                    print('παρακαλώ εισάγετε το ποσό σε ευρώ')
            ikerma = kerma * 100
            if (ikerma != 10 and ikerma != 20 and ikerma != 50 and ikerma != 100 and ikerma != 200 and ikerma != 500 ):
                print("\tΣΦΑΛΜΑ: εισαγωγή μη έγκυρου ποσού.");
                print("\tΠαρακαλώ, εισάγετε μία έγκυρη τιμή: 0.1 / 0.2 / 0.5 / 1 / 2 / 5 ");
        poso = poso + ikerma

# ερώτημα (γ)
    # υπολογισμός υπόλοιπου (ρέστα) και αριθμού κερμάτων ανά είδος κέρματος που πρέπει να επιστραφούν
    resta = poso - antitimo # υπολογισμός υπολοίπου
    print("Eπιστροφή", "{:3.1f}".format(resta/100), "ευρώ") 

# ερώτημα (δ)
    if (resta): # αν υπάρχουν ρέστα
        print("Παρακαλώ πάρτε")
        dieura = resta // 200 # υπολογισμός επιστροφής κερμάτων 2€
        resta = resta - 200 * dieura # ενημέρωση υπολοίπου ποσού
        if ( dieura > 0 ):
            print(" δίευρα :", int(dieura))
        monoeura = resta // 100 # υπολογισμός επιστροφής κερμάτων 1€
        resta = resta - 100 * monoeura # ενημέρωση υπολοίπου ποσού
        if ( monoeura > 0 ):
            print(" μονόευρα :", int(monoeura))
        penintalepta = resta // 50 # υπολογισμός επιστροφής κερμάτων 0.5€
        resta = resta - 50* penintalepta # ενημέρωση υπολοίπου ποσού
        if ( penintalepta > 0 ):
            print(" πενηντάλεπτα:", int(penintalepta))
        eikosalepta = resta // 20 # υπολογισμός επιστροφής κερμάτων 0.2€
        resta = resta - 20* eikosalepta # ενημέρωση υπολοίπου ποσού
        if ( eikosalepta > 0 ):
            print(" εικοσάλεπτα:", int(eikosalepta))
        dekalepta = resta // 10 # υπολογισμός επιστροφής κερμάτων 0.1€
        if ( dekalepta > 0 ):
            print(" δεκάλεπτα:", int(dekalepta))
    print(" ")
    print("\tΟλοκληρώθηκε η εκτέλεση του προγράμματος")
else: 
    print('Γεια σας!')
