# Password Generator

A secure, configurable command-line password generator written in Python.

## Features

- **Cryptographically secure** — uses Python's [`secrets`](https://docs.python.org/3/library/secrets.html) module rather than `random`, making generated passwords suitable for real-world use.
- **Configurable character sets** — choose any combination of lowercase letters, uppercase letters, digits, and symbols.
- **Guaranteed coverage** — every generated password contains at least one character from each selected set, then shuffles them so the guaranteed characters aren't predictably positioned.
- **Input validation** — rejects non-numeric, zero, and negative lengths, and re-prompts instead of crashing.

## Requirements

- Python 3.6 or newer (no third-party dependencies).

## Usage

Run the generator and follow the interactive prompts:

```bash
py "Password Generator.py"
```

Example session:

```
Enter the desired password length: 16
Include lowercase letters? [Y/n]: y
Include uppercase letters? [Y/n]: y
Include digits? [Y/n]: y
Include symbols? [Y/n]: y
Generated Password: qZ#<uBr$Ae1nn#G\
```

Press Enter at any yes/no prompt to accept the default (shown in capitals).

## Use as a library

The `generate_password` function can be imported and used directly:

```python
from importlib import import_module

pg = import_module("Password Generator")  # filename contains a space

password = pg.generate_password(
    length=20,
    use_lowercase=True,
    use_uppercase=True,
    use_digits=True,
    use_symbols=False,
)
print(password)
```

`generate_password` raises `ValueError` if:

- the length is not a positive integer,
- no character sets are selected, or
- the length is smaller than the number of selected character sets (so it can't include one of each).

## Running the tests

```bash
py -m unittest test_password_generator -v
```

## Files

| File | Description |
| --- | --- |
| `Password Generator.py` | The generator and interactive CLI. |
| `test_password_generator.py` | Unit tests covering generation and validation. |
