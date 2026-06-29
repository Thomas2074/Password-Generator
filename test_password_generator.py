"""Tests for the password generator."""

import importlib
import string
import unittest

# The module name contains a space, so import it via importlib.
pg = importlib.import_module("Password Generator")


class GeneratePasswordTests(unittest.TestCase):
    def test_default_length(self):
        for length in (4, 8, 16, 64):
            self.assertEqual(len(pg.generate_password(length)), length)

    def test_only_uses_selected_character_sets(self):
        password = pg.generate_password(
            20,
            use_lowercase=True,
            use_uppercase=False,
            use_digits=False,
            use_symbols=False,
        )
        self.assertTrue(all(c in string.ascii_lowercase for c in password))

    def test_contains_at_least_one_of_each_selected_set(self):
        # Run several times since selection is random.
        for _ in range(100):
            password = pg.generate_password(8)
            self.assertTrue(any(c in string.ascii_lowercase for c in password))
            self.assertTrue(any(c in string.ascii_uppercase for c in password))
            self.assertTrue(any(c in string.digits for c in password))
            self.assertTrue(any(c in string.punctuation for c in password))

    def test_digits_only(self):
        password = pg.generate_password(
            12,
            use_lowercase=False,
            use_uppercase=False,
            use_digits=True,
            use_symbols=False,
        )
        self.assertTrue(password.isdigit())

    def test_passwords_are_unique(self):
        passwords = {pg.generate_password(16) for _ in range(50)}
        # Collisions are astronomically unlikely with secure randomness.
        self.assertEqual(len(passwords), 50)

    def test_zero_length_raises(self):
        with self.assertRaises(ValueError):
            pg.generate_password(0)

    def test_negative_length_raises(self):
        with self.assertRaises(ValueError):
            pg.generate_password(-5)

    def test_non_integer_length_raises(self):
        with self.assertRaises(ValueError):
            pg.generate_password(8.5)

    def test_boolean_length_raises(self):
        with self.assertRaises(ValueError):
            pg.generate_password(True)

    def test_no_character_set_raises(self):
        with self.assertRaises(ValueError):
            pg.generate_password(
                10,
                use_lowercase=False,
                use_uppercase=False,
                use_digits=False,
                use_symbols=False,
            )

    def test_length_smaller_than_pools_raises(self):
        # All four pools selected but length 3 cannot fit one of each.
        with self.assertRaises(ValueError):
            pg.generate_password(3)


if __name__ == "__main__":
    unittest.main()
