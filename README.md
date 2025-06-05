The goal of this project is to evolve programs in BrainFuck. The first thing we need to do is implement a simple executor that takes as input a string (representing a program in BrainFuck) and executes it. The language consists of 6 characters, which operate as follows:

Character	Instruction Performed
>	Increment the data pointer by one (to point to the next cell to the right).
<	Decrement the data pointer by one (to point to the next cell to the left).
+	Increment the byte at the data pointer by one.
-	Decrement the byte at the data pointer by one.
[	If the byte at the data pointer is zero, then instead of moving the instruction pointer forward to the next command, jump it forward to the command after the matching ] command.
]	If the byte at the data pointer is nonzero, then instead of moving the instruction pointer forward to the next command, jump it back to the command after the matching [ command.

We add one additional twist on the standard language - a [ or ] which is unmatched will be ignored. This allows all strings of these characters to correspond to a valid program.

A program operates on a cyclic tape (moving off one end moves back to the other end) of signed bytes. Our executor should take as input a size indicating how many cells are on the tape, and optionally a list of initial values. If the list is shorter than the specified size, the remaining cells start as zero.

Fitness Evaluation
------------------
The ``evaluate`` function in ``fitness.py`` executes a BrainFuck program on a
number of randomly generated task instances. By default it uses
``AdditionTask`` which places two inputs on the tape and expects their sum in
the first cell when the program halts. The inputs are sampled from
non-negative values only. The returned score sums the negative absolute
difference between the expected and produced value for each instance, so
perfect solutions achieve the highest (least negative) score.

``TripleAdditionTask`` extends this idea by placing three inputs on the tape
and expecting their sum in the first cell. The default bounds ensure that the
sum never exceeds the signed byte range.

The ``--steps`` command line option controls how many instructions a program
may execute when being evaluated. It defaults to ``1000``.

Verbosity
---------
Use the ``-v``/``--verbose`` flag to display progress during evolution.
Passing ``-v`` prints the best and average score for each generation. Using
``-vv`` additionally prints the current best program.
