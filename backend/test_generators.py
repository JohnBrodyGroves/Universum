import random

from generators import GENERATORS, generate


def test_every_generator_makes_complete_questions():
    for name in GENERATORS:
        for seed in range(200):
            question = generate(name, random.Random(seed))
            for field in ["type", "prompt", "answer", "explanation"]:
                assert question[field], f"{name} left '{field}' empty"
            assert question["answer"] in question["explanation"]


def test_order_of_operations_answers_are_correct():
    for seed in range(200):
        question = generate("order_of_operations_basic", random.Random(seed))
        expression = question["prompt"].removeprefix("What is ").removesuffix("?").replace("x", "*")
        assert int(question["answer"]) == eval(expression)


def test_same_seed_gives_same_question():
    first = generate("whole_number_groups", random.Random(42))
    second = generate("whole_number_groups", random.Random(42))
    assert first == second
