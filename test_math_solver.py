import unittest
from math_solver_app import solve_math_expression

class TestMathSolver(unittest.TestCase):
    
    def test_basic_operations(self):
        self.assertEqual(str(solve_math_expression("2 + 3")), "5")
        self.assertEqual(str(solve_math_expression("10 - 3")), "7")
        self.assertEqual(str(solve_math_expression("4 × 2")), "8")
        self.assertEqual(str(solve_math_expression("8 ÷ 2")), "4.00000000000000")
    
    def test_exponentiation(self):
        self.assertEqual(str(solve_math_expression("2^3")), "8")
        self.assertEqual(str(solve_math_expression("5^2")), "25")
    
    def test_square_root(self):
        self.assertEqual(str(solve_math_expression("√16")), "4.00000000000000")
        self.assertEqual(str(solve_math_expression("√25")), "5.00000000000000")
    
    def test_complex_expressions(self):
        self.assertEqual(str(solve_math_expression("2 + 3 × 4")), "14")
        self.assertEqual(str(solve_math_expression("10 ÷ 2 + 3")), "8.00000000000000")
        self.assertEqual(str(solve_math_expression("5 + 2^3 - √16")), "9.00000000000000")
    
    def test_invalid_expression(self):
        self.assertIn("SyntaxError", str(solve_math_expression("2 + ")))
        self.assertIn("SympifyError", str(solve_math_expression("abc")))
        
    def test_edge_cases(self):
        self.assertEqual(str(solve_math_expression("0 + 0")), "0")
        self.assertEqual(str(solve_math_expression("0 × 5")), "0")
        self.assertEqual(str(solve_math_expression("100 ÷ 0")), "zoo")  # infinity in sympy
        self.assertIn("SyntaxError", str(solve_math_expression("")))

if __name__ == '__main__':
    unittest.main()
