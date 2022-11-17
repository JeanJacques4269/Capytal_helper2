import glob
import multiprocessing
import os
import sys
import time
from importlib.machinery import SourceFileLoader
from inspect import getmembers, isfunction
import signal

import xlsxwriter
import subprocess

debug = True

scrabble = {"A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1, "J": 8, "K": 10, "L": 1, "M": 2,
            "N": 1, "O": 1, "P": 3, "Q": 8, "R": 1, "S": 1, "T": 1, "U": 1, "V": 4, "W": 10, "X": 10, "Y": 10, "Z": 10}


def tests(copies_dir, correction_dir):
    print(f"**  STARTING TESTS  **")

    name = os.path.basename(correction_dir)
    correction = SourceFileLoader(name, correction_dir).load_module()
    fonctions = getmembers(correction, isfunction)
    fonctions_str_everyone_should_have = [e[0] for e in fonctions]

    args_for_tests = None
    try:
        args_for_tests = correction.tests_prof
    except AttributeError:
        print("!!! Missing 'tests_prof' in correction file !!!")

    # Getting all data required from the correction in order to correct fast

    tests_data = compute_tests_correction(correction, args_for_tests)
    if debug:
        print(f"{tests_data=}")

    # Starting correcting students
    all_data_for_excel = test_students_functions(copies_dir, fonctions_str_everyone_should_have, tests_data, debug=True)
    print("**  TESTS EXECUTED SUCCESSFULLY  **")

    print("Starting excel doc creation")
    return all_data_for_excel, fonctions_str_everyone_should_have


def compute_tests_correction(correction, args_for_tests, debug=False) -> dict:
    if debug:
        print("Creating correction data")
    fonctions = getmembers(correction, isfunction)
    fonctions_reelle = [e[1] for e in fonctions]
    fonctions_str = [e[0] for e in fonctions]

    if debug:
        print(f"Testing all these : {fonctions_str}")
    tests_data = dict()
    for j, fonction in enumerate(fonctions_reelle):
        if debug:
            print(f"Creating data for fonction : {fonction}")
        test_values = args_for_tests[fonctions_str[j]]
        answers = []
        if test_values:
            for args in test_values:
                if isinstance(args, tuple):
                    answers.append(fonction(*args))
                else:
                    answers.append(fonction(args))
            one_fonction_test_data = [test_values, answers]
        else:
            one_fonction_test_data = [[], [fonction()]]
        tests_data[fonctions_str[j]] = one_fonction_test_data
    return tests_data


def test_students_functions(copies_dir, fonctions_str, tests_data, debug=False) -> dict:
    all_data_for_excel = dict()

    for file in glob.glob(fr"{copies_dir}\*.py"):
        name_f = os.path.basename(file)
        name = name_f[:-3]
        if debug:
            print(f"Correcting {name_f}")
        all_data_for_excel[name_f[:-3]] = list()

        try:
            # student_file = SourceFileLoader(name_f, file).load_module()
            pass
        except Exception as e:
            print("Exceptionnally trash student, skipped.")
            continue

        for fonction_str in fonctions_str:
            arg_expected_out = tests_data[fonction_str]
            if debug:
                print(f"Testing {fonction_str}")

            nb_wrong = 0
            nb_error = 0

            try:
                # student_fonction = getattr(student_file, fonction_str)
                pass
            except AttributeError:  # la fonction n'est pas définie dans le fichier de l'élève
                all_data_for_excel[name].append("Missing fonction")
                continue

            for i, arg in enumerate(arg_expected_out[0]):
                if debug:
                    a = "[Truncated]"
                    print(f"{f'Test {i} : {arg if len(str(arg)) < 15 else a}':<24}", end="")
                error = False
                timeout = False
                got = None
                try:
                    basebasename = "copies." + name_f.replace(".py", "")
                    if isinstance(arg, tuple):
                        arg_list = [str(e) for e in arg]
                        real_arg = ",".join(arg_list)
                    else:
                        real_arg = arg
                    if type(arg) == str:
                        real_arg = f"'{real_arg}'"
                    magic_s = f'python -c "from {basebasename} import {fonction_str};import sys; print({fonction_str}' \
                              f'({real_arg}))"'
                    r = subprocess.run(magic_s, timeout=1, capture_output=True, )
                    print(r)
                    got = str(r.stdout.rstrip())[2:-1]

                except subprocess.TimeoutExpired as e:
                    timeout = True
                    print("Timeout", end=" | ")
                except Exception as e:
                    print(e)
                    error = True

                if error or timeout:
                    if debug:
                        print(f"Error")
                    nb_error += 1
                else:
                    if got == str(arg_expected_out[1][i]):
                        if debug:
                            print("OK")
                    else:
                        if debug:
                            print("WRONG RESULT")
                            # print(f"expected {arg_expected_out[1][i]}, got {got}")
                        nb_wrong += 1
            if debug:
                print()
            score = 100 - (nb_wrong + nb_error) / len(arg_expected_out[1]) * 100
            cute_score = int(f'{score:.0f}')
            all_data_for_excel[name].append(cute_score)

        if debug:
            print("____________________________________________________________________")
    return all_data_for_excel


def create_excel(data, fonctions_str, output_path) -> None:
    names = data.keys()

    workbook = xlsxwriter.Workbook(output_path)
    worksheet = workbook.add_worksheet('Output')

    row, column = 0, 1

    for fonction in fonctions_str:
        worksheet.write(row, column, fonction)
        column += 1

    row, column = 1, 0
    for name in names:
        worksheet.write(row, column, name)
        column += 1
        for score in data[name]:
            worksheet.write(row, column, score)
            column += 1
        row += 1
        column = 0

    worksheet.conditional_format(0, 0, 1000, 1000, {'type': '3_color_scale',
                                                    'min_value': 0,
                                                    "max_value": 100})

    workbook.close()
    print("Output wrote successfully")
