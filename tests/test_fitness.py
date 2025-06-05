import os
import sys
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fitness import TripleAdditionTask

def test_triple_addition_bounds():
    task = TripleAdditionTask()
    rng = random.Random(0)
    for _ in range(100):
        tape = task.generate_input(rng)
        a, b, c = tape[:3]
        assert a >= 0 and b >= 0 and c >= 0
        assert a + b + c <= 127

def test_triple_addition_fitness():
    task = TripleAdditionTask()
    initial = [5, 6, 7] + [0] * (task.size - 3)
    final = [18] + [0] * (task.size - 1)
    assert task.fitness(initial, final) == 0
    final_bad = [17] + [0] * (task.size - 1)
    assert task.fitness(initial, final_bad) == -1.0
