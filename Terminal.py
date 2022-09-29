from time import sleep
import Timer
import Timer_2

if __name__ == '__main__':
    print("Ktory typ pliku napisow")
    print("Z numerami linji dialogowych - 1")
    print("Bez numeru linji dialogowych - 2")

    dezycja = input("Wybor: ")

    nazwa = input("wczytaj nazwe: ")
    zmiana = input("jak chcesz zapisać: ")
    cofka = float(input("o ile chcesz cofnac: "))

    try:
        if ord(dezycja) == 49:
            Timer.zmiana_czasu_1(nazwa, zmiana, cofka*1000)
        else:
            Timer_2.zmiana_czasu_2(nazwa, zmiana, cofka)
    except Exception as e:
        print("Cos nie dziala\n"+str(e))
    finally:
        sleep(2)
