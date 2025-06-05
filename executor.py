"""BrainFuck executor.

This module provides a function to execute BrainFuck code on a cyclic tape of
signed bytes.
"""

from typing import Iterable, List, Mapping


def _wrap_byte(value: int) -> int:
    """Wrap integer to signed byte range [-128, 127]."""
    return ((value + 128) % 256) - 128


def _build_bracket_map(program: str) -> Mapping[int, int]:
    """Pre-compute matching bracket positions.

    Unmatched brackets are ignored and simply not present in the resulting map.
    """
    stack: List[int] = []
    pairs: dict[int, int] = {}
    for pos, char in enumerate(program):
        if char == "[":
            stack.append(pos)
        elif char == "]":
            if stack:
                open_pos = stack.pop()
                pairs[open_pos] = pos
                pairs[pos] = open_pos
    # Unmatched '[' are ignored by leaving them out of the map
    return pairs


def execute(program: str, *, steps: int, size: int, initial: Iterable[int] | None = None) -> List[int]:
    """Execute ``program`` for up to ``steps`` instructions.

    Parameters
    ----------
    program:
        BrainFuck program consisting of the characters ``><+-[]``. Any other
        characters are ignored.
    steps:
        Maximum number of instructions to execute.
    size:
        Number of cells on the cyclic tape.
    initial:
        Optional iterable of initial cell values. If fewer than ``size`` values
        are provided, remaining cells start at ``0``.

    Returns
    -------
    list[int]
        The final tape state after execution.
    """

    # Initialize the tape
    tape = list(initial or [])
    if len(tape) < size:
        tape.extend([0] * (size - len(tape)))
    else:
        tape = tape[:size]

    tape = [_wrap_byte(v) for v in tape]

    bracket_map = _build_bracket_map(program)

    data_ptr = 0
    instr_ptr = 0

    executed = 0
    prog_len = len(program)

    while instr_ptr < prog_len and executed < steps:
        command = program[instr_ptr]
        if command == '>':
            data_ptr = (data_ptr + 1) % size
        elif command == '<':
            data_ptr = (data_ptr - 1) % size
        elif command == '+':
            tape[data_ptr] = _wrap_byte(tape[data_ptr] + 1)
        elif command == '-':
            tape[data_ptr] = _wrap_byte(tape[data_ptr] - 1)
        elif command == '[':
            if tape[data_ptr] == 0:
                match = bracket_map.get(instr_ptr)
                if match is not None:
                    instr_ptr = match
        elif command == ']':
            if tape[data_ptr] != 0:
                match = bracket_map.get(instr_ptr)
                if match is not None:
                    instr_ptr = match
        # Ignore unknown characters and unmatched brackets
        instr_ptr += 1
        executed += 1

    return tape

