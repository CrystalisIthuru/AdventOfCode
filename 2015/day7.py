import os
import re
import numpy as np
from functools import reduce, cache

INPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), "inputs")
INPUT_FILE = os.path.join(INPUT_DIRECTORY, "7.dat")

def check_token_type(token_type, expected):

    if not isinstance(expected, list): expected = [expected]
    return token_type in expected

def eval_assignment_expression(tokens):

    if len(tokens) < 3: raise Exception("Not enough tokens")

    value_token_type, value = tokens[0]
    op_token_type, op = tokens[1]
    id_token_type, id = tokens[2]

    if op_token_type == "OP": return eval_binary_operator_expression(tokens)

    check_token_type(value_token_type, "INT")
    check_token_type(op_token_type, "ASSIGN")
    check_token_type(id_token_type, "ID")

    return tokens[3:], id, lambda gates: evaluate_gates(gates, value)

def eval_binary_operator_expression(tokens):

    if len(tokens) < 5: raise Exception("Not enough tokens")

    left_token_type, left = tokens[0]
    op_token_type, op = tokens[1]
    right_token_type, right = tokens[2]
    assign_token_type, _ = tokens[3]
    out_token_type, out = tokens[4]

    check_token_type(left_token_type, ["ID", "INT"])
    check_token_type(op_token_type, "OP")
    check_token_type(right_token_type, ["ID", "INT"])
    check_token_type(assign_token_type, "ASSIGN")
    check_token_type(out_token_type, "ID")

    ops = {
        "AND" : lambda x, y: x & y,
        "OR"  : lambda x, y: x | y,
        "LSHIFT" : lambda x, y: x << y,
        "RSHIFT" : lambda x, y: x >> y
    }

    return tokens[5:], out, lambda gates: ops[op](evaluate_gates(gates, left), evaluate_gates(gates, right))

def eval_unary_operator_expression(tokens):

    if len(tokens) < 4: raise Exception("Not enough tokens")

    op_token_type, op = tokens[0]
    id_token_type, id = tokens[1]
    assign_token_type, _ = tokens[2]
    out_token_type, out = tokens[3]

    check_token_type(op_token_type, "OP")
    check_token_type(id_token_type, "ID")
    check_token_type(assign_token_type, "ASSIGN")
    check_token_type(out_token_type, "ID")

    return tokens[4:], out, lambda gates: ~evaluate_gates(gates, id)

def eval_tokens(tokens):

    exprs = {}
    while tokens:
        token_type, value = tokens[0]
        if token_type in ["INT", "ID"]: # Possible binary
            tokens, out, expr = eval_assignment_expression(tokens)
        elif token_type == "OP" and value == "NOT":
            tokens, out, expr = eval_unary_operator_expression(tokens)
        else:
            raise Exception(f"Unexpected token {token_type}, {value}")

        exprs[out] = expr

    return exprs

CACHE = {}
def evaluate_gates(gates, value):

    if isinstance(value, str):
        if value in CACHE:
            return CACHE[value]
        else:
            result = gates[value](gates)
            CACHE[value] = result
            return result
    else:
        return value

def lexer(data):

    scanner = re.Scanner([
        ("\d+", lambda s, t: ("INT", np.ushort(t))),
        ("(NOT|AND|OR|LSHIFT|RSHIFT)", lambda s, t: ("OP", t)),
        ("->", lambda s, t: ("ASSIGN", t)),
        (r"\s+", None), # Ignore whitespace
        ("[a-z]+", lambda s, t: ("ID", t))
    ])
    tokens, remainder = scanner.scan(data)

    if remainder:
        raise Exception(f"Scanner had remainder: {remainder}")

    return tokens

def parse_input(input_file):

    with open(input_file, "r") as f:
        return eval_tokens(lexer(f.read()))

if __name__ == "__main__":

    gates = parse_input(INPUT_FILE)
    P1 = gates["a"](gates)
    print(P1)

    CACHE = {}                    # Reset all memory
    gates["b"] = lambda gates: P1 # Update b to assign the value from P1
    print(gates["a"](gates))
