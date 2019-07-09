import random
import unittest

from structures.char_set import CharSet


class CharSetTests(unittest.TestCase):

    def validate_tree(self, tree, expected_str):
        if tree.map.root is None:
            return
        self.assertIsNone(tree.map.root.parent)
        data = []

        def __validate(node):
            left_height, right_height = 0, 0
            left_size, right_size = 0, 0
            if node.left:
                self.assertEqual(node.left.parent, node)
                left_height = node.left.height
                left_size = node.left.size
                __validate(node.left)
            data.append(node.value)
            if node.right:
                self.assertEqual(node.right.parent, node)
                right_height = node.right.height
                right_size = node.right.size
                __validate(node.right)
            self.assertTrue(abs(left_height - right_height) <= 1)
            self.assertEqual(node.height, max(left_height, right_height) + 1)
            self.assertEqual(node.size, left_size + right_size + 1)
        __validate(tree.map.root)
        self.assertEqual(''.join(data), expected_str)

    def launch(self, s):
        self.s = s
        self.cs = CharSet(s)

    def test_create_empty(self):
        self.launch('')
        self.validate_tree(self.cs, self.s)

    def test_create_not_empty(self):
        self.launch('abcda')
        self.validate_tree(self.cs, self.s)

    def test_get_index(self):
        self.launch('abcd')
        for i in range(len(self.s)):
            self.assertEqual(self.s[i], self.cs[i])

    def test_get_negative_index(self):
        self.launch('abcd')
        with self.assertRaises(IndexError):
            self.cs[-1]

    def test_get_too_big_index(self):
        self.launch('abcd')
        with self.assertRaises(IndexError):
            self.cs[4]

    def test_swap(self):
        s = 'abcdefghjklmnoprstuxwz'
        for i in range(len(s)):
            self.launch(s)
            self.cs.swap(i)
            expected = self.s[i+1:] + self.s[:i+1]
            self.validate_tree(self.cs, expected)

    def test_swap_empty(self):
        self.launch('')
        with self.assertRaises(IndexError):
            self.cs.swap(0)

    def test_swap_negative_index(self):
        self.launch('abcd')
        with self.assertRaises(IndexError):
            self.cs.swap(-1)

    def test_swap_too_big_index(self):
        self.launch('abcd')
        with self.assertRaises(IndexError):
            self.cs.swap(4)

    def test_dynamic(self):
        for _ in range(150):
            s = ''.join([chr(random.randint(97, 122))
                         for _ in range(random.randint(1, 100))])
            cs = CharSet(s)
            self.validate_tree(cs, s)
            i = random.randint(0, len(s) - 1)
            cs.swap(i)
            expected = s[i+1:] + s[:i+1]
            self.validate_tree(cs, expected)


if __name__ == '__main__':
    unittest.main()
