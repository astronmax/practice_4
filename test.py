import unittest
from main import *

class TestSemanticAnalysis(unittest.TestCase):
    def test_positive_text(self):
        result = analyze_file("text_1.txt")
        self.assertIsInstance(result['normalized_score'], float)
        self.assertEqual(result['normalized_score'], 1.0)
    
    def test_negative_text(self):
        result = analyze_file("text_2.txt")
        self.assertIsInstance(result['normalized_score'], float)
        self.assertEqual(result['normalized_score'], -1.0)

if __name__ == '__main__':
    unittest.main()
