# -----------------------------
# BLOKS Interactive Adventure
# -----------------------------
blocks = {}
variables = {}

program = """
BLOK main
  say "Welcome to the BLOKS Adventure!"
  set health to 3
  call start
END

BLOK start
  say "You are in a dark forest. Paths go LEFT and RIGHT."
  set choice to ""  # placeholder for user input
  call get_choice
END

BLOK left_path
  say "You encounter a friendly elf!"
  say "The elf heals you by 1 point."
  set health to health + 1
  call continue_journey
END

BLOK right_path
  say "You fall into a trap!"
  say "You lose 1 health."
  set health to health - 1
  call continue_journey
END

BLOK continue_journey
  say "You continue deeper into the forest..."
  if health is 0
    say "You have no health left. Game over!"
  end
  if health is not 0
    say "You survive for now. Adventure continues..."
  end
END

BLOK get_choice
  say "Type LEFT or RIGHT:"
  set choice to input()
  if choice.lower() is "left"
    call left_path
  end
  if choice.lower() is "right"
    call right_path
  end
END
"""

# -----------------------------
# Parser
# -----------------------------
lines = [line.strip() for line in program.splitlines() if line.strip()]
stack = []
current_block = None

for line in lines:
    l = line.lower()
    if l.startswith("blok "):
        name = line[5:].strip()
        block = {"name": name, "commands": []}
        if stack:
            stack[-1]["commands"].append(block)
        stack.append(block)
        current_block = block
    elif l == "end":
        if current_block is not None:
            finished = stack.pop()
            if not stack:
                blocks[finished["name"]] = finished
            current_block = stack[-1] if stack else None
    else:
        if current_block is not None:
            current_block["commands"].append(line)

# -----------------------------
# Executor
# -----------------------------
def exec_line(cmd):
    parts = cmd.split()
    if not parts:
        return
    verb = parts[0]

    if verb == "say":
        text = cmd[4:].strip()
        if text.startswith('"') and text.endswith('"'):
            text = text[1:-1]
        elif text in variables:
            text = str(variables[text])
        print(text)

    elif verb == "set":
        var_name = parts[1]
        value_str = cmd.split("to", 1)[1].strip()

        # Handle arithmetic
        if "+" in value_str:
            var, add = value_str.split("+")
            var = var.strip()
            add = int(add.strip())
            value = variables.get(var, 0) + add
        elif "-" in value_str:
            var, sub = value_str.split("-")
            var = var.strip()
            sub = int(sub.strip())
            value = variables.get(var, 0) - sub
        # Handle numeric
        elif value_str.isdigit():
            value = int(value_str)
        # Handle input
        elif value_str.lower() == "input()":
            value = input()
        # Other variable
        elif value_str in variables:
            value = variables[value_str]
        # Text default
        else:
            value = value_str.strip('"')

        variables[var_name] = value

# -----------------------------
# Run block
# -----------------------------
def run_block(name):
    if name not in blocks:
        print(f"Unknown block {name}")
        return

    def run_commands(commands):
        i = 0
        while i < len(commands):
            cmd = commands[i]

            if isinstance(cmd, dict):
                i += 1
                continue

            parts = cmd.split()
            if not parts:
                i += 1
                continue

            if parts[0] == "repeat":
                count = parts[1]
                if count.isdigit():
                    times = int(count)
                elif count in variables:
                    times = variables[count]
                else:
                    times = 0

                repeat_cmds = []
                i += 1
                nested = 1
                while i < len(commands) and nested > 0:
                    line = commands[i]
                    if line.lower().startswith("repeat"):
                        nested += 1
                    elif line.lower() == "end":
                        nested -= 1
                        if nested == 0:
                            i += 1
                            break
                    if nested > 0:
                        repeat_cmds.append(line)
                    i += 1

                for _ in range(times):
                    run_commands(repeat_cmds)
                continue

            elif parts[0] == "call":
                run_block(parts[1])

            elif parts[0] == "wait":
                import time
                time.sleep(int(parts[1]))

            elif parts[0] in ("say", "set"):
                exec_line(cmd)

            elif parts[0] == "input":
                variables[parts[1]] = input()

            elif parts[0] == "if":
                # simple if condition: 'if health is 0'
                var = parts[1]
                op = parts[2]
                val = parts[3]
                if val.isdigit():
                    val = int(val)
                var_val = variables.get(var, 0)
                cond_met = (op == "is" and var_val == val) or (op == "is not" and var_val != val)
                if cond_met:
                    i += 1
                    continue
                else:
                    # Skip to the corresponding end
                    i += 1
                    nested_if = 1
                    while i < len(commands) and nested_if > 0:
                        line = commands[i].lower()
                        if line.startswith("if"):
                            nested_if += 1
                        elif line == "end":
                            nested_if -= 1
                        i += 1
                    continue

            i += 1

    run_commands(blocks[name]["commands"])

# -----------------------------
# Run the adventure
# -----------------------------
run_block("main")
