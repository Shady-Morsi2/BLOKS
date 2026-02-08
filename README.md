
BLOKS is a simple, text-based programming language inspired by the Algol family, designed to be readable, intuitive, and easy to learn. Everything in BLOKS is structured as blocks and commands, making programs resemble a set of instructions or “building blocks” that can be stacked, nested, and reused
Core Concepts:

Blocks (BLOK … END)

Blocks are the main structural unit.

They group commands together and can be nested.

Example:

BLOK main
  say "Hello World"
END


Commands (text-based verbs)

Each line is a command with optional arguments.

Commands describe actions in plain words.

Examples:

say "Hello" → prints text or variable values

set counter to 5 → stores a value

wait 2 → pauses execution for 2 seconds

call greet → runs another block

Variables

Variables store text or numbers.

No explicit types are required; BLOKS infers them.

Example:

set name to "Shady"
say name


Control Flow

Repeat loops:

repeat 3 times
  say "Again"
end


Conditional execution:

if counter is greater than 3
  say "Big"
end


Human-friendly Errors

Errors are descriptive and readable:

Unknown command "sya"
Did you mean "say"?


Execution

Execution starts at the top-level block.

Nested blocks are run via call.

Commands are executed sequentially in the order written.

Design Philosophy:

Readable: Programs look like plain English instructions.

Minimal syntax: Only BLOK and END are reserved keywords; everything else is a verb.

Extensible: New commands can be added easily without changing syntax.

Structured: Blocks provide hierarchy and scope, preventing messy code.

Fun and approachable: You can write a Hello World, a clock, or simple automation scripts without learning complicated syntax.
