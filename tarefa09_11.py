def mediafinal():
    a = int(input("Escreve a primeira nota: "))
    b = int(input("Escreve a segunda nota: "))
    c = int(input("Escreve a terceira note: "))

    media = (a+b+c)/3

    print(media)

    if media <9:
        print("Infelizmente você está reprovado.")
    else:
        print("Parabéns você está aprovado")

mediafinal()