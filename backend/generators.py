"""Question generators: each one makes a fresh question with random numbers every time.

A generator takes a random number source (rng) and returns a question in the same
shape as the hand-written questions in skill.yaml files.
"""

import random

CONTEXTS = [
    ("shelves", "books"),
    ("boxes", "eggs"),
    ("buses", "people"),
    ("bags", "apples"),
    ("rows", "chairs"),
]


def whole_number_groups(rng):
    groups = rng.randint(3, 12)
    each = rng.randint(3, 25)
    containers, items = rng.choice(CONTEXTS)
    answer = groups * each
    return {
        "type": "numeric",
        "prompt": f"There are {groups} {containers} with {each} {items} in each. How many {items} are there in all?",
        "answer": str(answer),
        "explanation": (
            f"Each of the {groups} {containers} has {each}, so multiply: {groups} x {each} = {answer}. "
            f"If you got {groups + each}, you added instead of multiplying."
        ),
    }


def order_of_operations_basic(rng):
    a = rng.randint(2, 20)
    b = rng.randint(2, 9)
    c = rng.randint(2, 9)
    answer = a + b * c
    return {
        "type": "numeric",
        "prompt": f"What is {a} + {b} x {c}?",
        "answer": str(answer),
        "explanation": (
            f"Multiply before you add: {b} x {c} = {b * c}, then {a} + {b * c} = {answer}. "
            f"If you got {(a + b) * c}, you added first."
        ),
    }


# The names used in skill.yaml files, mapped to the functions above
GENERATORS = {
    "whole_number_groups": whole_number_groups,
    "order_of_operations_basic": order_of_operations_basic,
}


def generate(name, rng=None):
    return GENERATORS[name](rng or random.Random())


if __name__ == "__main__":
    # Preview: print 3 sample questions from every generator
    for name in GENERATORS:
        print(f"--- {name} ---")
        for _ in range(3):
            question = generate(name)
            print(question["prompt"], "->", question["answer"])
