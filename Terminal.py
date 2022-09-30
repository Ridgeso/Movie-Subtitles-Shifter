import Timer

if __name__ == '__main__':
    # print("Ktory typ pliku napisow")
    # print("Z numerami linji dialogowych - 1")
    # print("Bez numeru linji dialogowych - 2")

    # dezycja = input("Wybor: ")

    file_name = input("File name: ")
    new_file = input("To what file write the output: ")
    shift_by = float(input("Shift by what amount: "))

    # try:
    Timer.shift_time_1(file_name, new_file, shift_by)
        # if ord(dezycja) == 49:
        #     Timer.zmiana_czasu_1(nazwa, zmiana, cofka*1000)
        # else:
        #     Timer_2.zmiana_czasu_2(nazwa, zmiana, cofka)
    # except Exception as e:
    #     print("Something goes wrong\n"+str(e))
    # finally:
    #     input("Press enter to finish the program... ")
