import time
from datetime import datetime
# -----------------------------
# BLOKS Interpreter
# -----------------------------

blocks = {}
variables = {}
# Sample BLOKS program
program = """
BLOK main
  say "Hello world"
  set counter to 3
  repeat counter times
    say "Again"
    repeat 2 times
      say "Nested"
    end
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
        if current_block is not None:  # only pop BLOK
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
        elif text == "now":
            text = datetime.now().strftime("%H:%M:%S")
        elif text in variables:
            text = str(variables[text])
        print(text)

    elif verb == "set":
        var_name = parts[1]
        value = parts[3]
        if value.isdigit():
            value = int(value)
        variables[var_name] = value

# Run commands inside a block
def run_block(name):
    if name not in blocks:
        print(f"Unknown block {name}")
        return

    def run_commands(commands):
        i = 0
        while i < len(commands):
            cmd = commands[i]

            # Skip nested BLOK definitions
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

                # collect inner commands inside repeat
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
                seconds = int(parts[1])
                time.sleep(seconds)

            elif parts[0] in ("say", "set"):
                exec_line(cmd)

            i += 1
