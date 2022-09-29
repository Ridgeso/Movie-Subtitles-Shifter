from dzialanie import *


@timer_decorator
def zmiana_czasu_1(nazwa, zmiana, cofka):
    with timer(nazwa, 'r') as f:
        tekst = f.readlines()

    with timer(zmiana, 'w') as plik_zmiana:
        nr_napisu = 1
        nr_lini = 0

        plik_zmiana.write('1'+'\n')
        for line in tekst:  # wczytywanie i przepisywanie pliku
            if str(nr_napisu) == line.strip() or nr_napisu == 1:

                nr_napisu += 1
                godz = tekst[nr_lini+1]

                gg = int(godz[0:2])
                mm = int(godz[3:5])
                sec = int(godz[6:8])
                msec = int(godz[9:12])
                gg, mm, sec, msec = cofnij(gg, mm, sec, msec, cofka)

                godz_zmie = wypisz(gg, mm, sec, msec)+" --> "

                gg = int(godz[17:19])
                mm = int(godz[20:22])
                sec = int(godz[23:25])
                msec = int(godz[26:29])
                gg, mm, sec, msec = cofnij(gg, mm, sec, msec, cofka)

                godz_zmie += wypisz(gg, mm, sec, msec)

                plik_zmiana.write(godz_zmie+'\n')
            else:
                try:
                    plik_zmiana.write(tekst[nr_lini+1])
                except Exception:
                    continue
            nr_lini += 1
