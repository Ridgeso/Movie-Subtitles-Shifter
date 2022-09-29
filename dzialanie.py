import math
from time import perf_counter


def timer_decorator(funk):
    """Wypisuje jak dlugo to zajelo"""
    def wrapper(*args, **kwargs):
        start = perf_counter()
        funk(*args, **kwargs)
        end = perf_counter()
        print(f"Gotowe! Zajelo to: {round(end-start,3)}sec")
    return wrapper


class timer:  # dzialanie Timer_2
    def __init__(self, file, mode):
        self.file = open(file, mode=mode, encoding='utf-8')

    def __enter__(self):
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()


# Dzialanie Timer
def cofnij(_gg, _mm, _sec, _msec, _cofka):  # cofa kolejno czasy
    czas = _gg*3600000+_mm*60000+_sec*1000+_msec-_cofka
    _gg = math.floor(czas/3600000)
    _mm = math.floor(czas % 3600000/60000)
    _sec = math.floor(czas % 60000/1000)
    _msec = math.floor(czas % 1000)
    return _gg, _mm, _sec, _msec


def wypisz(_gg, _mm, _sec, _msec):  # wypisuje czas w odpowiedniej formie
    # godz = ""
    godz = f"{_gg:0>2}:{_mm:0>2}:{_sec:0>2},{_msec:0>3}"
    # godz+='0'+str(_gg)+':' if _gg<10 else godz+=str(_gg)+':'
    # if _gg < 10:
    #     godz += '0'+str(_gg)+':'
    # else:
    #     godz += str(_gg)+':'
    # if _mm < 10:
    #     godz += '0'+str(_mm)+':'
    # else:
    #     godz += str(_mm)+':'
    # if _sec < 10:
    #     godz += '0'+str(_sec)+','
    # else:
    #     godz += str(_sec)+','
    # if _msec < 10:
    #     godz += '00'+str(_msec)
    # elif _msec < 100:
    #     godz += '0'+str(_msec)
    # else:
    #     godz += str(_msec)
    return godz
