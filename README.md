
# chip-8-for-python

An emulator for the original Chip 8 made in Python using the pygame-ce library.

## Requirements

- Python 3.10 or higher

- pygame-ce 2.5.8

To install Python: https://www.python.org/downloads/

Once Python is installed, you can use this command to install pygame-ce:

```bash
pip install pygame-ce
```

Drop any roms onto the same folder where both Python files are located.

To run the emulator, use the command: 

```bash
py main.py "name of the rom file" "emulation speed"
```

If the emulation speed is left blank, it will default to a speed of 2000 
instructions per second.

## Notes
- Audio is currently not implemented.

- Due to the Chip-8 never defining a standard clock speed, many different games run
on different speeds. It's best to try out games at different speeds until one
fits naturally.

## Controls

Chip-8 keypad:

| 1 | 2 | 3 | C |
|---|---|---|---|
| 4 | 5 | 6 | D |
| 7 | 8 | 9 | E |
| A | 0 | B | F |

is mapped to:

| 1 | 2 | 3 | 4 |
|---|---|---|---|
| Q | W | E | R |
| A | S | D | F |
| Z | X | C | V |