from typing import TextIO
import math
from time import perf_counter


def timer_decorator(funk):
    def wrapper(*args, **kwargs):
        start = perf_counter()
        funk(*args, **kwargs)
        end = perf_counter()
        print(f"Done! It took: {end - start : .3f}sec")
    return wrapper


class Timer:
    class _Time:
        def __init__(self, hours: int, minutes: int, seconds: int, millisecond: int) -> None:
            self.hours = hours
            self.minutes = minutes
            self.seconds = seconds
            self.millisecond = millisecond
        
        def __str__(self) -> str:
            return f"{self.hours:0>2}:{self.minutes:0>2}:{self.seconds:0>2},{self.millisecond:0>3}"

    def __init__(self, file: str, mode: str) -> None:
        self._file = open(file, mode=mode, encoding='utf-8')
        self._mode = mode

    @property
    def file(self) -> TextIO:
        return self._file

    @property
    def mode(self) -> str:
        return self._mode

    def __enter__(self) -> TextIO:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.file:
            self.file.close()
    
    def pars_time(self, old_time: str) -> _Time:
        hours = int(old_time[0:2])
        minutes = int(old_time[3:5])
        seconds = int(old_time[6:8])
        millisecond = int(old_time[9:12])
        
        return self._Time(hours, minutes, seconds, millisecond)

    def shift(self, time: _Time, shift_by: int) -> _Time:
        shift_time = time.hours * 3_600_000 \
                     + time.minutes * 60_000 \
                     + time.seconds * 1_000 \
                     + time.millisecond \
                     - shift_by
        h = math.floor(shift_time / 3_600_000)
        m = math.floor(shift_time % 3_600_000 / 60_000)
        s = math.floor(shift_time % 60_000 / 1_000)
        ms = math.floor(shift_time % 1_000)
        new_time = self._Time(h, m, s, ms)
        return new_time

    @staticmethod
    def print_time(time: _Time) -> str:
        return str(time)


@timer_decorator
def shift_time_1(file: str, new_file: str, shift_by: int):
    shift_by *= 1000
    
    with Timer(file, 'r') as f:
        text = f.file.readlines()

    with Timer(new_file, 'w') as shifter:
        text_number = 1
        line_number = 0

        shifter.file.write('1\n')
        for line in text:
            if str(text_number) == line.strip() or text_number == 1:
                text_number += 1                
                hour = text[line_number + 1]

                shifted_time = "{} --> {}\n"

                parsed_1st_part = shifter.pars_time(hour[ 0 : hour.find(" --> ") ])
                shifted_parsed_1st_parth = shifter.shift(parsed_1st_part, shift_by)
                shifted_1st_part = shifter.print_time(shifted_parsed_1st_parth)

                parsed_2nd_part = shifter.pars_time(hour[ hour.find(" --> ") + len(" --> ") : -1])
                shifted_parsed_2nd_parth = shifter.shift(parsed_2nd_part, shift_by)
                shifted_2nd_part = shifter.print_time(shifted_parsed_2nd_parth)

                shifted_time = shifted_time.format(shifted_1st_part, shifted_2nd_part)
                shifter.file.write(shifted_time)
            else:
                try:
                    shifter.file.write(text[line_number + 1])
                except Exception:
                    continue
            line_number += 1


@timer_decorator
def zmiana_czasu_2(nazwa, zmiana, cofka):
    with Timer(nazwa, 'r') as f:
        dialogi = f.readlines()

    with Timer(zmiana, 'w') as new:
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
