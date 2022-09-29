from dzialanie import *


@timer_decorator
def zmiana_czasu_2(nazwa, zmiana, cofka):
    # wczytuje wszystkie linie do listy
    with timer(nazwa, 'r') as f:
        dialogi = f.readlines()

    # nowy plik z cofnietym czasem
    with timer(zmiana, 'w') as new:
        for line in dialogi:
            line = line.strip()
            k = 1
            while line[k] != '}':
                k += 1
            czas = int(line[1:k])-cofka
            new.write('{'+str(czas)+'}')

            k_2 = k+2
            while line[k+1] != '}':
                k += 1
            czas = int(line[k_2:k+1])-cofka
            new.write('{'+str(czas)+'}'+line[k+2::]+'\n')
