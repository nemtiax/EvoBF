"""Simple evolutionary system for BrainFuck programs."""

from __future__ import annotations

import random
from typing import Sequence

from fitness import Task, evaluate, AdditionTask


INSTRUCTIONS = "><+-.,[]"


def _mutate(program: str, rng: random.Random, rate: float) -> str:
    """Return a mutated copy of ``program``."""
    chars = list(program)
    i = 0
    while i < len(chars):
        if rng.random() < rate:
            choice = rng.choice(["sub", "del", "ins"])
            if choice == "sub":
                chars[i] = rng.choice(INSTRUCTIONS)
            elif choice == "del":
                chars.pop(i)
                continue
            else:  # ins
                chars.insert(i, rng.choice(INSTRUCTIONS))
                i += 1
        i += 1
    if rng.random() < rate:
        chars.append(rng.choice(INSTRUCTIONS))
    return "".join(chars)


def _crossover(a: str, b: str, rng: random.Random) -> str:
    """Create a program by crossing ``a`` and ``b``."""
    if not a and not b:
        return ""
    cut_a = rng.randint(0, len(a))
    cut_b = rng.randint(0, len(b))
    return a[:cut_a] + b[cut_b:]


def _select(population: Sequence[str], fitnesses: Sequence[float], rng: random.Random) -> str:
    """Fitness-proportional random selection.

    ``fitnesses`` may contain negative values. They are shifted so that the
    lowest fitness corresponds to weight ``0``.
    """
    if not fitnesses:
        return rng.choice(population)
    min_fit = min(fitnesses)
    if min_fit < 0:
        weights = [f - min_fit for f in fitnesses]
    else:
        weights = list(fitnesses)
    if sum(weights) == 0:
        return rng.choice(population)
    return rng.choices(population, weights=weights, k=1)[0]


def evolve(population_size: int, elite_count: int, generations: int, *,
           mutation_rate: float = 0.1, crossover_rate: float = 0.5,
           task: Task | None = None, instances: int = 10, steps: int = 1000,
           rng: random.Random | None = None, verbose: int = 0) -> tuple[str, float]:
    """Evolve a BrainFuck program.

    Parameters
    ----------
    population_size:
        Number of individuals in the population.
    elite_count:
        Number of top scoring programs preserved unchanged each generation.
    generations:
        How many generations to evolve.
    mutation_rate:
        Probability of applying a mutation at each position.
    crossover_rate:
        Probability of creating an offspring via crossover of two parents.
    task:
        Evaluation task used for fitness calculation.
    instances:
        Number of task instances used per evaluation.
    steps:
        Maximum instructions to execute per evaluation.
    rng:
        Optional random generator.
    verbose:
        Verbosity level. ``0`` disables progress output. Higher values print
        additional statistics during evolution.

    Returns
    -------
    tuple[str, float]
        The best program found and its score on the final generation.
    """

    rng = rng or random.Random()
    task = task or AdditionTask()
    population = ["" for _ in range(population_size)]

    best_prog = ""
    best_score = float("-inf")

    for gen in range(generations):
        eval_inputs = [task.generate_input(rng) for _ in range(instances)]
        scores = [evaluate(prog, task=task, steps=steps, rng=rng,
                          inputs=eval_inputs)
                  for prog in population]
        pairs = list(zip(population, scores))
        pairs.sort(key=lambda p: p[1], reverse=True)
        population = [p[0] for p in pairs]
        scores = [p[1] for p in pairs]

        if scores[0] > best_score:
            best_prog = population[0]
            best_score = scores[0]

        if verbose:
            avg = sum(scores) / len(scores)
            msg = f"Gen {gen + 1}/{generations}: best={scores[0]} avg={avg:.2f}"
            print(msg)
            if verbose > 1:
                print(f"  Best program: {population[0]!r}")

        elites = population[:elite_count]
        fitnesses = scores

        new_population = elites.copy()
        while len(new_population) < population_size:
            if rng.random() < crossover_rate:
                parent1 = _select(population, fitnesses, rng)
                parent2 = _select(population, fitnesses, rng)
                child = _crossover(parent1, parent2, rng)
            else:
                parent = _select(population, fitnesses, rng)
                child = parent
            child = _mutate(child, rng, mutation_rate)
            new_population.append(child)

        population = new_population

    # Final evaluation to return accurate best score
    final_inputs = [task.generate_input(rng) for _ in range(instances)]
    final_scores = [evaluate(prog, task=task, steps=steps, rng=rng,
                            inputs=final_inputs)
                    for prog in population]
    best_idx = max(range(len(population)), key=lambda i: final_scores[i])
    return population[best_idx], final_scores[best_idx]
