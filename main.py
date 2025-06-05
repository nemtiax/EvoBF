import argparse
import random

from evolver import evolve
from fitness import AdditionTask, TripleAdditionTask


def main() -> None:
    parser = argparse.ArgumentParser(description="Evolve BrainFuck programs")
    parser.add_argument("--population-size", type=int, default=100,
                        help="number of individuals in the population")
    parser.add_argument("--elite-count", type=int, default=5,
                        help="number of elite programs kept each generation")
    parser.add_argument("--generations", type=int, default=50,
                        help="number of generations to evolve")
    parser.add_argument("--mutation-rate", type=float, default=0.1,
                        help="probability of mutation at each position")
    parser.add_argument("--crossover-rate", type=float, default=0.5,
                        help="probability of creating offspring via crossover")
    parser.add_argument("--instances", type=int, default=10,
                        help="number of evaluation instances per program")
    parser.add_argument("--init-length", type=int, default=10,
                        help="initial random program length")
    parser.add_argument("--task", choices=["addition", "triple"], default="addition",
                        help="evaluation task to use")
    parser.add_argument("--size", type=int, default=8,
                        help="tape size for the addition task")
    parser.add_argument("--min-value", type=int, default=-64,
                        help="minimum random input value for the addition task")
    parser.add_argument("--max-value", type=int, default=63,
                        help="maximum random input value for the addition task")
    parser.add_argument("--seed", type=int, default=None,
                        help="random seed")
    parser.add_argument("--steps", type=int, default=1000,
                        help="maximum instructions executed per evaluation")
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="increase verbosity; can be specified multiple times")

    args = parser.parse_args()

    rng = random.Random(args.seed)

    if args.task == "addition":
        task = AdditionTask(size=args.size,
                            min_value=args.min_value,
                            max_value=args.max_value)
    else:
        task = TripleAdditionTask(size=args.size,
                                  min_value=args.min_value,
                                  max_value=args.max_value)

    program, score = evolve(
        args.population_size,
        args.elite_count,
        args.generations,
        mutation_rate=args.mutation_rate,
        crossover_rate=args.crossover_rate,
        task=task,
        instances=args.instances,
        steps=args.steps,
        init_length=args.init_length,
        rng=rng,
        verbose=args.verbose,
    )

    print(program)
    print(f"Score: {score:.2f}")


if __name__ == "__main__":
    main()
