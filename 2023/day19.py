from functools import reduce
import os
import re

INPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), "inputs")
INPUT_FILE = os.path.join(INPUT_DIRECTORY, "19.dat")

def build_rule_function(expr):
        
    match = re.match(r"([amsx])([<>])(\d+):(.*)", expr)
    category = match.group(1)
    operator = (lambda x, y: x < y) if match.group(2) == "<" else (lambda x, y: x > y)
    value = int(match.group(3))
    workflow = match.group(4)

    return RuleFunction(workflow, operator, category, value)

class RuleFunction:

    def __init__(self, workflow, operator = None, category = None, value = None):

        self.workflow = workflow
        self.operator = operator
        self.category = category
        self.value = value

    def __call__(self, part):

        if self.category is None: # Default workflow
            return self.workflow
        elif self.operator(part[self.category], self.value):
            return self.workflow
        else:
            return None

def parse_input(input_file):

    with open(input_file, "r") as f:
        rules = parse_rules(f)
        parts = parse_parts(f)

    return rules, parts

def parse_rules(f):

    rules = {}

    for line in f:

        line = line.strip()
        if line == "": return rules

        match = re.match(r"(.*){(.*)}", line)
        workflow_name = match.group(1)

        workflow_rules_strings = match.group(2).split(",")
        workflow_rules = []
        for rule in workflow_rules_strings[:-1]:
            workflow_rules += [build_rule_function(rule)]
        workflow_rules += [RuleFunction (workflow_rules_strings[-1])]

        rules[workflow_name] = workflow_rules

    raise Exception("Unexpected end of file.")

def parse_parts(f):

    parts = []
    for line in f:
        line = line.strip()
        line = line[1:-1]

        part = {}
        for element in line.split(","):
            split = element.split("=")
            part[split[0]] = int(split[1])
        
        parts += [part]

    return parts

def evaluate_parts(rules, parts):

    accepted = []
    for part in parts:

        workflow = "in"
        while workflow not in ["A", "R"]:
            workflow = evaluate_workflow(part, rules[workflow])
        
        if workflow == "A":
            accepted += [part]
    
    return accepted

def evaluate_workflow(part, rules):

    for rule in rules:
        workflow = rule(part)
        if workflow is not None:
            return workflow

    raise Exception("Could not evaluate workflow rules.")

if __name__ == "__main__":

    rules, parts = parse_input(INPUT_FILE)
    print(reduce(lambda acc, part: acc + sum(part.values()), evaluate_parts(rules, parts), 0))