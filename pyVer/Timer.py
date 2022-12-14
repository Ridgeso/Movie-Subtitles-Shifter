from typing import Any, Callable, TextIO
import math
from time import perf_counter


def timer_decorator(funk: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        start = perf_counter()
        funk(*args, **kwargs)
        end = perf_counter()
        print(f"Done! It took: {end - start : .3f}sec")
    return wrapper


class Timer:
    class _Time:
        def __init__(self, hours: int, minutes: int, seconds: int, milliseconds: int) -> None:
            self.hours = hours
            self.minutes = minutes
            self.seconds = seconds
            self.milliseconds = milliseconds
        
        def __str__(self) -> str:
            return f"{self.hours:0>2}:{self.minutes:0>2}:{self.seconds:0>2},{self.milliseconds:0>3}"
        
        @property
        def collapsed_time(self):
            return self.hours * 3_600_000 \
                 + self.minutes * 60_000 \
                 + self.seconds * 1_000 \
                 + self.milliseconds

    def __init__(self, source: str, file: str, binaryMode: bool = False) -> None:
        if binaryMode:
            self._source = open(source, mode="rb")
            self._file = open(file, mode="wb")
        else:
            self._source = open(source, mode="r", encoding='utf-8')
            self._file = open(file, mode="w", encoding='utf-8')

    @property
    def source(self) -> TextIO:
        return self._source

    @property
    def file(self) -> TextIO:
        return self._file

    def __enter__(self) -> TextIO:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.source:
            self.source.close()
        if self.file:
            self.file.close()
    
    def pars_time(self, old_time: str) -> _Time:
        old_time = old_time.replace(',', ':')
        return self._Time(*map(int, old_time.split(':')))

    def shift(self, time: _Time, shift_by: int) -> _Time:
        shift_time = time.collapsed_time - shift_by

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
def shift_time_1(file: str, new_file: str, shift_by: int) -> None:
    shift_by *= 1000
    
    with Timer(file, new_file) as shifter:
        text_number = 1
        line_number = 0

        while line := shifter.source.readline():
            if str(text_number) == line.strip() or text_number == 1:
                hour = shifter.source.readline()

                shifted_time = "{} --> {}\n"

                time_parts = hour.split(" --> ")

                # parsed_1st_part = shifter.pars_time(hour[ 0 : hour.find(" --> ") ])
                parsed_1st_part = shifter.pars_time(time_parts[0])
                shifted_parsed_1st_part = shifter.shift(parsed_1st_part, shift_by)
                shifted_1st_part = shifter.print_time(shifted_parsed_1st_part)

                # parsed_2nd_part = shifter.pars_time(hour[ hour.find(" --> ") + len(" --> ") : -1])
                parsed_2nd_part = shifter.pars_time(time_parts[1])
                shifted_parsed_2nd_part = shifter.shift(parsed_2nd_part, shift_by)
                shifted_2nd_part = shifter.print_time(shifted_parsed_2nd_part)

                shifted_time = shifted_time.format(shifted_1st_part, shifted_2nd_part)
                shifter.file.write(f"{text_number}\n")
                shifter.file.write(shifted_time)

                text_number += 1

            else:
                shifter.file.write(line)

            line_number += 1


@timer_decorator
def shift_time_2(file: str, new_file: str, shift: int) -> None:
    brace = ord('}')

    with Timer(file, new_file, binaryMode=True) as new:
        while line := new.source.readline().strip():

            bracePosition = line.find(brace, 1)
            time_1st_part = int(line[1 : bracePosition]) - shift

            lastBracePosition = bracePosition + 2
            bracePosition = line.find(brace, lastBracePosition)

            time_2nd_part = int(line[lastBracePosition : bracePosition]) - shift
            
            new.file.write(b'{%d}{%d}%s\n' % (time_1st_part, time_2nd_part, line[bracePosition + 1:]))
