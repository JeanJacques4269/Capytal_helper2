import glob
import os
from importlib.machinery import SourceFileLoader
from inspect import getmembers, isfunction
import signal

import xlsxwriter

debug = False

i_test = [["a", "b", "c"], []]


class Timeout:

    def __init__(self, seconds=1, error_message='TimeoutError'):
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, type, value, traceback):
        signal.alarm(0)


def tests(copies_dir, correction_dir, inputs_test):
    print(f"**  STARTING TESTS  **")

    name = os.path.basename(correction_dir)
    correction = SourceFileLoader(name, correction_dir).load_module()
    fonctions = getmembers(correction, isfunction)
    fonctions_str_everyone_should_have = [e[0] for e in fonctions]

    # Getting all data required from the correction in order to correct fast

    tests_data = compute_tests_correction(correction, inputs_test)
    if debug:
        print(f"{tests_data=}")

    # Starting correcting students
    all_data_for_excel = test_students_fucntions(copies_dir, fonctions_str_everyone_should_have, tests_data, debug=True)
    print("**  TESTS EXECUTED SUCCESSFULLY  **")

    print("Starting excel doc creation")
    # create_excel(all_data_for_excel, fonctions_str_everyone_should_have)


def compute_tests_correction(correction, inputs_test, debug=True) -> dict:
    if debug:
        print("Starting tests computation")
    fonctions = getmembers(correction, isfunction)
    fonctions_reelle = [e[1] for e in fonctions]
    fonctions_str = [e[0] for e in fonctions]

    if debug:
        print(f"Testing all these : {fonctions_str}")
    tests_data = dict()
    for j, fonction in enumerate(fonctions_reelle):
        if debug:
            print(f"Creating data for fonction : {fonction}")
        test_values = inputs_test[j]
        answers = []
        if test_values:
            for i in test_values:
                answers.append(fonction(i))
            one_fonction_test_data = [test_values, answers]
        else:
            one_fonction_test_data = [[], [fonction()]]
        tests_data[fonctions_str[j]] = one_fonction_test_data
    return tests_data


def test_students_fucntions(copies_dir, fonction_str, tests_data, debug=False) -> dict:
    all_data_for_excel = dict()

    for file in glob.glob(fr"{copies_dir}\*.py"):
        name = os.path.basename(file)
        student_file = SourceFileLoader(name, file).load_module()
        if debug:
            print(f"Loaded {name}")
        all_data_for_excel[name] = list()
        for fonction in fonction_str:
            arg_expected_out = tests_data[fonction]
            if debug:
                print(f"\nTesting {fonction} with {arg_expected_out}")

            nb_wrong = 0
            nb_error = 0

            try:
                student_fonction = getattr(student_file, fonction)
            except AttributeError:  # la fonction n'est pas définie dans le fichier de l'élève
                all_data_for_excel[name].append("na")
                continue

            for i, arg in enumerate(arg_expected_out[0]):
                if debug:
                    print(f"{f'testing with {arg}':<24}", end="")
                error = False

                with Timeout(seconds=3, error_message='Job took too much time'):
                    try:
                        if isinstance(arg, tuple):
                            got = student_fonction(*arg)
                        else:
                            got = student_fonction(arg)
                    except TimeoutError as e:
                        print(e)
                        error = True
                        got = None
                    except Exception:
                        error = True
                        got = None
                if error:
                    if debug:
                        print(f"Error")
                    nb_error += 1
                else:
                    if got == arg_expected_out[1][i]:
                        if debug:
                            print("Passed")
                    else:
                        # print("Wrong")
                        if debug:
                            print(f"expected {arg_expected_out[1][i]}, got {got}")
                        nb_wrong += 1
            score = 100 - (nb_wrong + nb_error) / len(arg_expected_out[1]) * 100
            cute_score = int(f'{score:.0f}')
            all_data_for_excel[name].append(cute_score)
            if debug:
                print(f"Finished testing, score = {cute_score}%")
        if debug:
            print("\n\n__________________________________________________________________________________________\n\n")
    return all_data_for_excel


def create_excel(data, fonctions_str) -> None:
    names = data.keys()

    workbook = xlsxwriter.Workbook('output.xlsx')
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
