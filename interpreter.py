# lisp.py
# A simple Lisp evaluator written in Python.
# capjamesg 2022

import sys
import unittest
from functools import reduce

arguments = sys.argv

# functions supported by the interpreter
# functions can also be defined in lisp and will be saved to this
# dictionary in the runtime
functions = {
    "first": lambda x: x[0],
    "+": lambda x: sum(x),
    "last": lambda x: x[-1],
    "car": lambda x: x[0][0],
    "cdr": lambda x: x[0][1:],
    "print": lambda x: print(x),
    "-": lambda numbers: reduce(lambda x, y: x - y, numbers),
    "*": lambda numbers: reduce(lambda x, y: x * y, numbers),
    ">": lambda x: x[0] > x[1],
    "max": lambda x: max(x),
    "min": lambda x: min(x),
    "and": lambda x: all(x),
    "not": lambda x: not x,
    "or": lambda x: x[0] or x[1],
    "quote": lambda x: x,
    "list": lambda x: list(x),
    "concatenate": lambda strings: reduce(lambda x, y: x + y, strings),
}

# values considered nil
NIL_VALUES = ("()", "nil")
# value for truth
TRUTH_BOOLEAN_VALUE = "t"

code = """
(if (and (> 2 1) (> 1 3)) (last (- 2 3) 99) (last 1 33))
"""
# (car (+ 1 2) 2 9)
# (cdr 1 2 4)


class LispError(Exception):
    """
    A general exception raised by the Lisp interpreter.
    """

    def __init__(self, message):
        print(message)


def create_tokens(code: str) -> list:
    """
    Transforms a string of Lisp code into a list of tokens.

    :param code: A string of Lisp code.
    :type code: str
    :returns: A list of tokens.
    :rtype: list
    """
    return code.strip().replace(")", " ) ").replace("(", " ( ").split()


def parse(tokens: list) -> list:
    """
    Transforms a list of tokens into a nested list of all function calls.

    :param tokens: A list of tokens to transform.
    :type tokens: str
    :returns: A nested list of function calls to make.
    :rtype: list
    """
    buffer = []

    while tokens:
        token = tokens.pop(0)

        if token == "(":
            buffer.append(parse(tokens))
        elif token == ")":
            return buffer
        else:
            if token.isdigit():
                token = int(token)
            buffer.append(token)

    return buffer


def evaluate(parsed_tokens: list) -> str:
    """
    Accepts a list of parsed tokens and evaluates their contents.

    :param tokens: A list of parsed tokens returned by the parse() function.
    :type tokens: str
    :returns: A string output from the Lisp function evaluation.
    :rtype: str
    """
    if (
        isinstance(parsed_tokens, int)
        or len(parsed_tokens) == 1
        and isinstance(parsed_tokens[0], int)
    ):
        return parsed_tokens

    if parsed_tokens in NIL_VALUES:
        return False

    if parsed_tokens == TRUTH_BOOLEAN_VALUE:
        return True

    car, cdr = parsed_tokens[0], parsed_tokens[1:]

    results = []

    if car == "apply":
        function_car, function_cdr = cdr[0], cdr[1:]

        return [functions[function_car](item) for item in function_cdr][0]

    if car in ("defun", "defparameter", "defvar"):
        function_car, function_cdr = cdr[0], cdr[1:]
        functions[function_car] = function_cdr
        return ""

    if car == "if":
        function_car, function_cdr = cdr[0], cdr[1:]

        if evaluate(function_car):
            return evaluate(function_cdr[0])
        else:
            return evaluate(function_cdr[1])

    for item in cdr:
        if isinstance(item, list):
            results.append(evaluate(item))
        else:
            results.append(item)

    try:
        function_results = functions[car]
    except:
        raise LispError("Function not defined.")

    if isinstance(function_results, list):
        function_to_execute = functions[car][1][0]

        return functions[function_to_execute](results)

    return functions[car](results)


def evaluate_code_string(code, verbose=False):
    """
    Parses a provided string of Lisp code.
    """
    for i in code.split("\n"):
        if i.strip() == "":
            continue

        tokens = create_tokens(i)
        parsed_tokens = parse(tokens)[0]

        if verbose:
            print(evaluate(parsed_tokens))

    return evaluate(parsed_tokens)


def main():
    """
    Accept a string of Lisp, interpret the code, then evaluate it.
    """
    # create interactive repl if --repl argument provided, else evaluate value of "code"
    if len(arguments) > 1 and arguments[1] == "--repl":
        try:
            while True:
                prompt = input("* ")

                tokens = create_tokens(prompt)
                parsed_tokens = parse(tokens)[0]

                print(evaluate(parsed_tokens))
        except KeyboardInterrupt:
            print("goodbye!")
    else:
        evaluate_code_string(code)


if __name__ == "__main__":
    main()
