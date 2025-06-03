"""Program evaluation utilities for evolving BrainFuck programs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Protocol
import random

from executor import execute


class Task(Protocol):
    """Interface for evaluation tasks."""

    size: int

    def generate_input(self, rng: random.Random) -> List[int]:
        """Return a list of initial cell values for one instance."""

    def fitness(self, initial: List[int], final: List[int]) -> float:
        """Return a fitness value for ``final`` given ``initial``."""


@dataclass
class AdditionTask:
    """Simple task: sum the first two cells."""

    size: int = 8
    min_value: int = -64
    max_value: int = 63

    def generate_input(self, rng: random.Random) -> List[int]:
        a = rng.randint(self.min_value, self.max_value)
        b = rng.randint(self.min_value, self.max_value)
        tape = [a, b] + [0] * (self.size - 2)
        return tape

    def fitness(self, initial: List[int], final: List[int]) -> float:
        expected = initial[0] + initial[1]
        error = abs(final[0] - expected)
        return -float(error)


def evaluate(program: str, *, task: Task | None = None, instances: int = 1,
             steps: int = 1000, rng: random.Random | None = None) -> float:
    """Evaluate ``program`` on ``instances`` of ``task``.

    Parameters
    ----------
    program:
        BrainFuck program to execute.
    task:
        Task providing inputs and computing fitness. Defaults to :class:`AdditionTask`.
    instances:
        Number of random inputs to evaluate.
    steps:
        Maximum instructions to execute for each instance.
    rng:
        Optional random generator.

    Returns
    -------
    float
        The summed fitness over all instances. Higher values are better.
    """

    if task is None:
        task = AdditionTask()

    rng = rng or random.Random()
    score = 0.0

    for _ in range(instances):
        initial = task.generate_input(rng)
        final = execute(program, steps=steps, size=task.size, initial=initial)
        score += task.fitness(initial, final)

    return score

