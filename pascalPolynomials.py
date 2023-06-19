import sys
from sympy import *
from sympy.abc import x
from math import factorial
import colorama
from colorama import Fore, Style


def pascal(n, p):
    triangle = []
    for i in range(n):
        row = []
        for j in range(i + 1):
            coefficient = factorial(i) // (factorial(j) * factorial(i - j))
            row.append(int(coefficient % p))
        triangle.append(row)
    return triangle


def draw_pascal(triangle, border=0, module=1):
    colorama.init(autoreset=True)
    max_num_length = len(str(max(max(triangle))))
    for i, row in enumerate(triangle):
        if module == 2 and i < border:
            continue
        print(Fore.LIGHTYELLOW_EX + str(i) + ". ", end=" ")
        formatted_row = []
        for num in row:
            if num == 0:
                formatted_row.append(Fore.RED + str(num).center(max_num_length))
            else:
                formatted_row.append(Fore.LIGHTCYAN_EX + str(num))
        triangle_padding = " " * (len(triangle) - i - 1) * 2
        print(triangle_padding + "   ".join(formatted_row))


def draw_pascal_line(triangle, index):
    row = triangle[index]
    for j in range(len(row)):
        if (row[j] == 0):
            print(Fore.MAGENTA + str(row[j]), end=" ")
        else:
            print(Fore.LIGHTCYAN_EX + str(row[j]), end=" ")
    print()


def generate_polynomials(triangle, p):
    print()
    polynomials = []
    for i in range(len(triangle)):
        polynomial = []
        for j in range(len(triangle[i])):
            if triangle[i][j] == 0:
                continue
            if j == 0:
                polynomial.append(str(triangle[i][j]))
            else:
                polynomial.append(f"{triangle[i][j]}*x^{j}")
        polynomials.append(" + ".join(polynomial))
    return polynomials


def generate_polynomials_first3(triangle, p):
    print()
    polynomials = []
    for i in range(len(triangle)):
        polynomial = []
        for j in range(min(3, len(triangle[i]))):
            if triangle[i][j] == 0:
                continue
            if j == 0:
                polynomial.append(str(triangle[i][j]))
            else:
                polynomial.append(f"{triangle[i][j]}*x^{j}")
        polynomials.append(" + ".join(polynomial))
    return polynomials


def generate_polynomials_F2E(triangle, p):
    print()
    polynomials = []
    for i in range(len(triangle)):
        polynomial = []
        for j in range(len(triangle[i])):
            if j == 0 or j == 1 or j == len(triangle[i]) - 1:
                coefficient = triangle[i][j] % p
                if coefficient != 0:
                    if j == 0:
                        polynomial.append(str(coefficient))
                    else:
                        polynomial.append(f"{coefficient}*x^{j}")
        polynomials.append(" + ".join(polynomial))
    return polynomials


def generate_polynomials_FME(triangle, p):
    print()
    polynomials = []
    coeffs = []
    for i in range(len(triangle)):
        polynomial = []
        polynomial_coeffs = []
        num_coeffs = len(triangle[i])

        if num_coeffs % 2 == 0:
            polynomial_coeffs.append(triangle[i][0] % p)
            polynomial_coeffs.append(triangle[i][num_coeffs - 1] % p)
            if polynomial_coeffs[0] != 0:
                polynomial.append(str(triangle[i][0]))
            if polynomial_coeffs[1] != 0:
                polynomial.append(f"{triangle[i][num_coeffs - 1]}*x^{num_coeffs - 1}")
        else:
            middle_index = num_coeffs // 2
            for j in range(num_coeffs):
                if j == 0 or j == middle_index or j == num_coeffs - 1:
                    coeff = triangle[i][j] % p
                    if coeff != 0:
                        polynomial_coeffs.append(coeff)
                        if j == 0:
                            polynomial.append(str(triangle[i][j]))
                        else:
                            polynomial.append(f"{triangle[i][j]}*x^{j}")

        polynomials.append(" + ".join(polynomial))
        coeffs.append(polynomial_coeffs)
    return polynomials


def find_roots(polynomial, p):
    roots = []
    f = Poly(polynomial, x, modulus=p)
    for i in range(p):
        if f.eval(i) % p == 0:
            roots.append(i)
    return roots


def check_irreducibility(polynomial, p):
    f = Poly(polynomial, x, modulus=p)
    return f.is_irreducible


def factorize_polynomial(polynomial, p):
    f = Poly(polynomial, x, modulus=p)
    if f.is_irreducible:
        return ""
    factors = factor_list(f)
    factorization = []
    for factor, exponent in factors[1]:
        my_factor = str(factor.as_expr()).replace("**", "^")
        factorization.append(f"({my_factor})^{exponent}")
    return " * ".join(factorization)


def get_longest_polynome(polynomials):
    longest = 0
    for poly in polynomials:
        if len(poly) > longest:
            longest = len(poly)
    return longest+2


def print_properties(polynomials, p, module, n=0, additional_rows=0):
    if module == 2:
        beginning = n
        to = n + additional_rows
    else:
        beginning = 0
        to = len(polynomials)

    for i in range(beginning, to):
        roots = find_roots(polynomials[i], p)
        irreducibility = check_irreducibility(polynomials[i], p)
        factorization = factorize_polynomial(polynomials[i], p)

        longest_poly = get_longest_polynome(polynomials)
        formatting = longest_poly - len(polynomials[i])
        line_formatting = len(str(to)) - len(str(i))
        roots_formatting = 5 - len(roots)

        print(
            Fore.YELLOW + f"RIADOK {i} --->" + " " * line_formatting + Fore.LIGHTCYAN_EX + f" F{p} :  P{i}(x)" + " "
            * line_formatting + " = " + Fore.BLUE + f"{polynomials[i]}" + " " * formatting + Fore.LIGHTCYAN_EX +
            f"KORENE:" + Fore.LIGHTBLUE_EX + f"{roots}" + " " * roots_formatting, end="")

        if irreducibility:
            print(Fore.LIGHTMAGENTA_EX + f" IREDUCIBILNÝ")
        else:
            print(Fore.MAGENTA + f" REDUCIBILNÝ   " +
                  Fore.LIGHTCYAN_EX + f"ROZKLAD: " + Fore.LIGHTBLUE_EX + f"{factorization}")
    print()


def print_single_line_properties(polynomials, index, p):
    polynomial = polynomials[index]
    roots = find_roots(polynomial, p)
    irreducibility = check_irreducibility(polynomial, p)
    factorization = factorize_polynomial(polynomial, p)
    print(Fore.YELLOW + f"RIADOK {index} --->" + " " + Fore.LIGHTCYAN_EX + f" F{p} :  P{index}(x)" +
          " = " + Fore.BLUE + f"{polynomial}" + Fore.LIGHTCYAN_EX +
          f" KORENE:" + Fore.LIGHTBLUE_EX + f"{roots}", end="")
    if irreducibility:
        print(Fore.LIGHTMAGENTA_EX + f" IREDUCIBILNÝ")
    else:
        print(Fore.MAGENTA + f" REDUCIBILNÝ   " +
              Fore.LIGHTCYAN_EX + f"ROZKLAD: " + Fore.LIGHTBLUE_EX + f"{factorization}")
    print()


def select_polynom(question_1, triangle, p, index=0):
    print()
    print(Fore.BLACK +     "1 - polynóm vygenerovaný z celého riadku\n"
                           "2 - trinóm zložený z prvých 3 prvkov riadku\n"
                           "3 - trinóm zložený z 2 prvých a posledného prvku\n"
                           "4 - trinóm zložený z prvého, stredného a posledného riadku" )
    question_2 = custom_input(Fore.BLACK + "Vyberte typ polynómu: ", "Úspešne zadané!", "Zadajte číslo od 1 do 4",
                              bottom=0, upper=5)

    if question_2 == 1:
        polynomials = generate_polynomials(triangle, p)
    elif question_2 == 2:
        polynomials = generate_polynomials_first3(triangle, p)
    elif question_2 == 3:
        polynomials = generate_polynomials_F2E(triangle, p)
    elif question_2 == 4:
        polynomials = generate_polynomials_FME(triangle, p)
    else:
        return question_2

    if question_1 == 2:
        print_single_line_properties(polynomials, index, p)
    else:
        print_properties(polynomials, p, 1)

    return question_2


def next_lines(n, p, question):
    while True:
        print()
        additional_rows = custom_input("Zadajte počet ďalších riadkov na výpis alebo 0 pre ukončenie programu: ",
                                       "Úspešne zadané!", "Zadajte kladné číslo. ", bottom=-1)
        if additional_rows == 0:
            break
        additional_rows = int(additional_rows)
        triangle = pascal(n + additional_rows, p)
        draw_pascal(triangle, n, 2)

        if question == 1:
            polynomials = generate_polynomials(triangle, p)
        elif question == 2:
            polynomials = generate_polynomials_first3(triangle, p)
        elif question == 3:
            polynomials = generate_polynomials_F2E(triangle, p)
        elif question == 4:
            polynomials = generate_polynomials_FME(triangle, p)

        print_properties(polynomials, p, 2, n, additional_rows)
        n += additional_rows


def custom_input(input_prompt, valid_input, wrong_input, exception_message="Chybný vstup!", bottom=-sys.maxsize + 1,
                 upper=sys.maxsize):
    user_input = -sys.maxsize
    while (bottom >= user_input) or (user_input >= upper):
        print(Fore.BLACK + Style.BRIGHT + input_prompt + Style.RESET_ALL, end="")
        try:
            user_input = int(input())
        except ValueError:
            print(Fore.RED + exception_message)
            continue

        if (bottom >= user_input) or (user_input >= upper):
            print(Fore.RED + wrong_input)
            continue
    print(Fore.LIGHTGREEN_EX + valid_input)
    print(Style.RESET_ALL)
    return user_input


def start():
    n = custom_input("Zadajte počet riadkov n: ", "Úspešne zadané!", "Zadajte číslo väčšie ako 0. ", bottom=0)
    p = custom_input("Zadajte prvočíslo (modulo) p: ", "Úspešne zadané!", "Zadajte číslo väčšie ako 0. ", bottom=0)
    triangle = pascal(n, p)

    question_1 = custom_input("Chcete vypísať všetky riadky (1) alebo iba jeden konkrétny (2)? ", "Úspešne zadané!", "Zadajte číslo 1 alebo 2. ", bottom=0, upper=3)

    if (question_1 == 1):
        draw_pascal(triangle)
        question_2 = select_polynom(question_1, triangle, p)

        print()
        question_3 = custom_input(Fore.BLACK + "Želáte si vypísať ďalšie riadky? Zadajte číslo 1 pre ÁNO alebo číslo 2 pre NIE. ", "Úspešne zadané!",
                                  "Zadajte číslo 1 alebo 2. ", bottom=0, upper=3)
        if question_3 == 1:
            next_lines(n, p, question_2)

    elif question_1 == 2:
        index = custom_input("Zadajte index riadku na výpis alebo -1 pre ukončenie programu. ", "Úspešne zadané!",
                             f"Zadajte číslo 0 alebo {n - 1}", bottom=-2, upper=n)
        while index != -1:
            draw_pascal_line(triangle, index)
            select_polynom(question_1, triangle, p, index)
            index = custom_input("Zadajte index riadku na výpis alebo -1 pre ukončenie programu. ", "Úspešne zadané!",
                                 f"Zadajte číslo 0 alebo {n - 1}", bottom=-2, upper=n)


start()
print(Fore.GREEN + Style.BRIGHT + "Úspešné ukončenie programu.")