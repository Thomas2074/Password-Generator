"""A secure, configurable command-line password generator."""

import secrets
import string

# Minimum length that still allows reasonable security.
MIN_LENGTH = 4


def generate_password(
    length,
    use_lowercase=True,
    use_uppercase=True,
    use_digits=True,
    use_symbols=True,
):
    """Generate a cryptographically secure random password.

    Args:
        length: Desired password length (must be a positive integer).
        use_lowercase: Include lowercase letters (a-z).
        use_uppercase: Include uppercase letters (A-Z).
        use_digits: Include digits (0-9).
        use_symbols: Include punctuation symbols.

    Returns:
        A randomly generated password string of the requested length that is
        guaranteed to contain at least one character from each selected pool.

    Raises:
        ValueError: If length is not a positive integer, no character pools are
            selected, or length is smaller than the number of selected pools.
    """
    if not isinstance(length, int) or isinstance(length, bool):
        raise ValueError("Length must be an integer.")
    if length < 1:
        raise ValueError("Length must be a positive integer.")

    pools = []
    if use_lowercase:
        pools.append(string.ascii_lowercase)
    if use_uppercase:
        pools.append(string.ascii_uppercase)
    if use_digits:
        pools.append(string.digits)
    if use_symbols:
        pools.append(string.punctuation)

    if not pools:
        raise ValueError("At least one character set must be selected.")
    if length < len(pools):
        raise ValueError(
            f"Length must be at least {len(pools)} to include every "
            "selected character set."
        )

    # Guarantee at least one character from each selected pool, then fill the
    # rest from the combined pool.
    all_characters = "".join(pools)
    password_chars = [secrets.choice(pool) for pool in pools]
    password_chars += [
        secrets.choice(all_characters) for _ in range(length - len(pools))
    ]

    # Shuffle so the guaranteed characters are not always at the front.
    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)


def _prompt_yes_no(prompt, default=True):
    """Prompt the user for a yes/no answer, returning a boolean."""
    suffix = " [Y/n]: " if default else " [y/N]: "
    while True:
        answer = input(prompt + suffix).strip().lower()
        if not answer:
            return default
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please answer 'y' or 'n'.")


def _prompt_length():
    """Prompt the user for a valid password length."""
    while True:
        raw = input("Enter the desired password length: ").strip()
        try:
            length = int(raw)
        except ValueError:
            print("Please enter a whole number.")
            continue
        if length < MIN_LENGTH:
            print(f"Please enter a length of at least {MIN_LENGTH}.")
            continue
        return length


def main():
    """Interactive entry point."""
    length = _prompt_length()
    use_lowercase = _prompt_yes_no("Include lowercase letters?")
    use_uppercase = _prompt_yes_no("Include uppercase letters?")
    use_digits = _prompt_yes_no("Include digits?")
    use_symbols = _prompt_yes_no("Include symbols?")

    try:
        password = generate_password(
            length,
            use_lowercase=use_lowercase,
            use_uppercase=use_uppercase,
            use_digits=use_digits,
            use_symbols=use_symbols,
        )
    except ValueError as error:
        print(f"Error: {error}")
        return

    print("Generated Password:", password)


if __name__ == "__main__":
    main()
