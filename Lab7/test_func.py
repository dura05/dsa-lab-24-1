import unittest
from triangle_func import get_triangle_type, IncorrectTriangleSides

class TestTriangleFunc(unittest.TestCase):
    def test_equilateral(self):
        self.assertEqual(get_triangle_type(5, 5, 5), "equilateral")
    
    def test_isosceles(self):
        self.assertEqual(get_triangle_type(5, 5, 8), "isosceles")
        self.assertEqual(get_triangle_type(5, 8, 5), "isosceles")
        self.assertEqual(get_triangle_type(8, 5, 5), "isosceles")
    
    def test_nonequilateral(self):
        self.assertEqual(get_triangle_type(3, 4, 5), "nonequilateral")
    
    def test_negative_side(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(-1, 2, 2)
    
    def test_zero_side(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(0, 1, 1)
    
    def test_invalid_sides(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(1, 1, 3)

if __name__ == "__main__":
    unittest.main()