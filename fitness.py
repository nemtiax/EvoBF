"""Program evaluation utilities for evolving BrainFuck programs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Protocol, Sequence
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
        """Return a tape where both inputs are positive."""

        low = max(0, self.min_value)
        high = max(low, self.max_value)
        a = rng.randint(low, high)
        b = rng.randint(low, high)
        tape = [a, b] + [0] * (self.size - 2)
        return tape

    def fitness(self, initial: List[int], final: List[int]) -> float:
        expected = initial[0] + initial[1]
        error = abs(final[0] - expected)
        return -float(error)


@dataclass
class TripleAdditionTask:
    """Task: sum the first three cells without overflow."""

    size: int = 8
    min_value: int = -42
    max_value: int = 42

    def generate_input(self, rng: random.Random) -> List[int]:
        """Return a tape with three positive inputs.

        The range is restricted so that the sum fits into a signed byte.
        """
        low = max(0, self.min_value)
        high = max(low, self.max_value)
        a = rng.randint(low, high)
        b = rng.randint(low, high)
        c = rng.randint(low, high)
        tape = [a, b, c] + [0] * (self.size - 3)
        return tape

    def fitness(self, initial: List[int], final: List[int]) -> float:
        expected = initial[0] + initial[1] + initial[2]
        error = abs(final[0] - expected)
        return -float(error)


def evaluate(program: str, *, task: Task | None = None, instances: int = 1,
             steps: int = 1000, rng: random.Random | None = None,
             inputs: Sequence[List[int]] | None = None) -> float:
    """Evaluate ``program`` on ``instances`` of ``task``.

    Parameters
    ----------
    program:
        BrainFuck program to execute.
    task:
        Task providing inputs and computing fitness. Defaults to :class:`AdditionTask`.
    instances:
        Number of random inputs to evaluate. Ignored when ``inputs`` is
        provided.
    steps:
        Maximum instructions to execute for each instance.
    rng:
        Optional random generator.
    inputs:
        Optional sequence of pre-generated initial tapes. When provided all
        programs are evaluated on these inputs instead of generating new ones.

    Returns
    -------
    float
        The summed fitness over all instances. Higher values are better.
    """

    if task is None:
        task = AdditionTask()

    rng = rng or random.Random()

    if inputs is None:
        inputs = [task.generate_input(rng) for _ in range(instances)]

    score = 0.0
    for initial in inputs:
        final = execute(program, steps=steps, size=task.size, initial=initial)
        score += task.fitness(list(initial), final)

    return score

