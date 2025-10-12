from __future__ import annotations
import os, unittest

class TestProjectStructure(unittest.TestCase):
    def test_src_exists(self):
        self.assertTrue(os.path.isdir('src'))
    def test_tests_exists(self):
        self.assertTrue(os.path.isdir('tests'))
    def test_main_exists(self):
        self.assertTrue(os.path.isfile('src/main.py'))
    def test_env_example_exists(self):
        self.assertTrue(os.path.isfile('.env.example'))

if __name__ == '__main__':
    unittest.main()
