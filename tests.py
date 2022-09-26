class LispInterpreterTests(unittest.TestCase):
    """
    Test cases for the Lisp interpreter.
    """
    def test_mathematical_operands(self):
        """
        Test that all mathematical operands work as expected.
        """
        self.assertEqual(evaluate_code_string("(* 3 2)"), 6)
        self.assertEqual(evaluate_code_string("(- 3 2)"), 1)
        self.assertEqual(evaluate_code_string("(+ 3 23 3)"), 29)

    def test_boolean_logic(self):
        """
        Test that Boolean logic works as expected.
        """
        self.assertEqual(evaluate_code_string("(and 1 1)"), True)
        self.assertEqual(evaluate_code_string("(or 1 1)"), True)
        self.assertEqual(evaluate_code_string("(not 1)"), False)

    def test_list_functions(self):
        """
        Test that list operations work as expected.
        """
        self.assertEqual(evaluate_code_string("(max 1 9 2)"), 9)
        self.assertEqual(evaluate_code_string("(min 9 1 2)"), 1)
        self.assertEqual(evaluate_code_string("(car (list 1 2 3))"), 1)
        self.assertEqual(evaluate_code_string("(cdr (list 1 2 3))"), [2, 3])
        self.assertEqual(evaluate_code_string("(apply + (1 2 3))"), 6)

    def test_not_implemented(self):
        """
        Test that undefined code returns an exception.
        """
        with self.assertRaises(LispError):
            evaluate_code_string("(test 1 2 3)")


unittest.main()
