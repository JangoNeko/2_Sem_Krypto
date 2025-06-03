def square_multiply(a, x, n):                                     #um RSA zu berechnen
    k = bin(x)[2:]
    a = a % n
    y = 1
    for i, v in enumerate(k):
        if v == "0":
            y = (y ** 2) % n
        else:
            y = (y ** 2) % n
            y = (y * a) % n
    assert pow(a, x, n) == y
    return y

def rsa_encode(msg, rsa_modulus, public_exp):                       #Enstschlüsselung mit RSA-Verfahren
    return (square_multiply(msg, public_exp, rsa_modulus))

def breaking_bob():
    encoded = [2514, 2929, 333, 333, 153, 1204]                     #Secret Message
    decoded = {}                                                    #Dictionary für Chiffrat-Klartext-Paare
    result = []                                                     #Ausgabearray
    for bob in encoded:
        i = 64
        while i <= 90:
            if bob in decoded:                                      #Prüfen, ob Chiffrat im dictionary liegt -> Wenn vorhanden, anhängen an Ausgabearray
                result.append(chr(decoded.get(bob)))
                break

            if rsa_encode(i, 3763, 11) == bob:  #RSA-Verschlüsseln und bei Kollision Chiffrat mit Klartext ins Dictionary und ausgabearray
                decoded.update({bob : i})
                result.append(chr(i))
                break
            i += 1
    return result

print(breaking_bob())                                                #Ausgabe: ['S', 'O', 'M', 'M', 'E', 'R']