import unittest
from modules.utils import calculate_distance_km

class TestUtils(unittest.TestCase):
    def test_calculate_distance(self):
        paris = (48.8566, 2.3522)
        lyon = (45.7640, 4.8357)

        dist = calculate_distance_km(paris, lyon)

        self.assertIsInstance(dist, float)
        self.assertGreater(dist, 300)
        self.assertLess(dist, 500)

if __name__ == '__main__':
    unittest.main()
