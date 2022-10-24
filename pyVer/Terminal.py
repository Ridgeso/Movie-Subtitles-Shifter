import Timer

if __name__ == '__main__':
    print("Type of the file: ")
    print("With text line number - 1")
    print("Without               - 2")

    text_file_type = input("Choice: ")

    file_name = input("File name: ")
    new_file = input("To what file write the output: ")
    shift_by = float(input("Shift by what amount: "))

    if text_file_type == '1':
        Timer.shift_time_1(file_name, new_file, shift_by)
    elif text_file_type == '2':
        Timer.shift_time_2(file_name, new_file, shift_by)
    else:
        print("I am not supporting other types of coding subtitles files!")
    input("Press enter to finish the program... ")
