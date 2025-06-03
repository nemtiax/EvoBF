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

    def check_output(self, initial: List[int], final: List[int]) -> bool:
        """Return ``True`` if ``final`` is a correct result for ``initial``."""


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

    def check_output(self, initial: List[int], final: List[int]) -> bool:
        return final[0] == initial[0] + initial[1]


def evaluate(program: str, *, task: Task | None = None, instances: int = 1,
             steps: int = 100, rng: random.Random | None = None) -> int:
    """Evaluate ``program`` on ``instances`` of ``task``.

    Parameters
    ----------
    program:
        BrainFuck program to execute.
    task:
        Task providing inputs and checking results. Defaults to :class:`AdditionTask`.
    instances:
        Number of random inputs to evaluate.
    steps:
        Maximum instructions to execute for each instance.
    rng:
        Optional random generator.

    Returns
    -------
    int
        The number of instances for which the program produced a correct result.
    """

    if task is None:
        task = AdditionTask()

    rng = rng or random.Random()
    score = 0

    for _ in range(instances):
        initial = task.generate_input(rng)
        final = execute(program, steps=steps, size=task.size, initial=initial)
        if task.check_output(initial, final):
            score += 1

    return score

