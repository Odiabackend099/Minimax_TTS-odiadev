from __future__ import annotations
import unittest
from src.auth import generate_api_key, hash_api_key, verify_api_key

class TestAuth(unittest.TestCase):
    def test_key_uniqueness(self):
        keys = {generate_api_key() for _ in range(100)}
        self.assertEqual(len(keys), 100)
    def test_hash_verify(self):
        k = generate_api_key()
        h = hash_api_key(k)
        self.assertTrue(verify_api_key(k, h))
        self.assertFalse(verify_api_key(k+"x", h))

if __name__ == '__main__':
    unittest.main()
