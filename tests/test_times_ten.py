import inspect
import unittest
from unittest.mock import patch

import src.times_ten as times_ten_module
from src.times_ten import times_ten


def get_correct(a: int, b: int) -> dict:
    return {x: x * 10 for x in range(a, b + 1)}


def check_no_code_outside_functions(module):
    """Check that the module has no top-level statements besides imports,
    def/class headers, comments, and the `if __name__ == "__main__":`
    guard. Returns (True, "") if clean, otherwise (False, offending_line).
    """
    allowed_prefixes = (
        "import ", "from ", "def ", "class ", " ", "\t", "#", "if __name__",
    )
    source = inspect.getsourcefile(module)
    with open(source) as file:
        for line in file.readlines():
            if line.strip() == "":
                continue
            if not line.startswith(allowed_prefixes):
                return False, line
    return True, ""


class TestTimesTen(unittest.TestCase):

    def test_0_main_program_ok(self):
        ok, line = check_no_code_outside_functions(times_ten_module)
        message = (
            "The code for testing the functions should be placed inside\n"
            "if __name__ == \"__main__\":\n"
            "block. The following row should be moved:\n"
        )
        self.assertTrue(ok, msg=message + line)

    def test_1_function_exists(self):
        with patch('builtins.input',
                    side_effect=[AssertionError("Asking input from the "
                                                 "user was not expected")]):
            try:
                times_ten(1, 2)
            except Exception:
                self.fail(
                    "Make sure that function can be called as follows\n"
                    "times_ten(1, 2)")

    def test_2_type_of_return_value(self):
        val = times_ten(1, 2)
        taip = str(type(val)).replace("<class '", '').replace("'>", "")
        self.assertTrue(
            type(val) == dict,
            msg=f"Function times_ten should return value which is "
                f"dict-type, now it returns value {val} which is "
                f"{taip}-type.")

    def test_3_numbers(self):
        test_cases = ((1, 3), (0, 6), (2, 8), (20, 23), (100, 110))
        for test_case in test_cases:
            with patch('builtins.input',
                        side_effect=[AssertionError("Asking input from "
                                                     "the user was not "
                                                     "expected")]):
                value = times_ten(test_case[0], test_case[1])
                correct = get_correct(test_case[0], test_case[1])

                self.assertEqual(
                    len(correct), len(value),
                    msg=f"The returned dictionary should contain "
                        f"{len(correct)} items, but it contains "
                        f"{len(value)} items: \n{value} when the "
                        f"parameters are {test_case}")
                self.assertEqual(
                    value, correct,
                    msg=f"The result \n{value}\ndoes not match with the "
                        f"model solution \n{correct}\nwhen the parameters "
                        f"are\n{test_case}")


if __name__ == '__main__':
    unittest.main()
