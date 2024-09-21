# Итоговое задание № 1 - задача № 2  "функция-конвертер для римских чисел"
def roman_to_integer(roman):
    roman_numerals = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }

    integer_value = 0

    for i in range(len(roman)):
        if i + 1 < len(roman) and roman_numerals[roman[i]] < roman_numerals[roman[i + 1]]:
            integer_value -= roman_numerals[roman[i]]
        else:
            integer_value += roman_numerals[roman[i]]

    return integer_value

roman_input = input("Введите римское число: ").upper()

try:
    result = roman_to_integer(roman_input)
    print(f"Десятичное значение римского числа {roman_input} равно {result}")
except KeyError:
    print("Ошибка: введено неверное римское число. Пожалуйста, используйте только римские цифры (I, V, X, L, C, D, M).")
