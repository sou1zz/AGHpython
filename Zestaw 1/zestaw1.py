import os
import re
import random
from typing import Dict, List, Optional


# 1. Katalogi
def count_files(directory: str) -> int:
    
    return sum(len(files) for _, _, files in os.walk(directory))


def list_files_recursive(directory: str) -> None:
    
    for root, _, files in os.walk(directory):
        for file in files:
            print(os.path.join(root, file))


# 2. Teksty
def remove_words(text: str, words_to_remove: List[str]) -> str:
    
    pattern = r'\b(' + '|'.join(map(re.escape, words_to_remove)) + r')\b'
    return re.sub(pattern, '', text)


def replace_words(text: str, replacements: Dict[str, str]) -> str:
    
    pattern = re.compile('|'.join(re.escape(word) for word in replacements))
    return pattern.sub(lambda match: replacements[match.group(0)], text)


# 3. Sortowanie liczb
def bubble_sort(numbers: List[int]) -> List[int]:
    
    n = len(numbers)
    for i in range(n):
        for j in range(0, n-i-1):
            if numbers[j] > numbers[j+1]:
                numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
    return numbers


def quick_sort(numbers: List[int]) -> List[int]:
    
    if len(numbers) <= 1:
        return numbers
    pivot = numbers[0]
    lesser = [x for x in numbers[1:] if x <= pivot]
    greater = [x for x in numbers[1:] if x > pivot]
    return quick_sort(lesser) + [pivot] + quick_sort(greater)


# 4. Klasa drzewa
class TreeNode:
    
    def __init__(self, value: Optional[int] = None):
        self.value = value
        self.children = {}

    def add_child(self, child, edge_label: Optional[str] = None):
        self.children[child] = edge_label

    def __str__(self):
        return f"Node({self.value})"


class Tree:
    
    def __init__(self):
        self.root = None

    def set_root(self, value: int):
        self.root = TreeNode(value)

    def traverse(self, node: Optional[TreeNode] = None):
        if node is None:
            node = self.root
        if node is not None:
            print(node)
            for child, label in node.children.items():
                print(f"Edge to {child} with label {label}")
                self.traverse(child)

    def __str__(self):
        return f"Tree(root={self.root})"


# Testy jednostkowe
import unittest

class TestTree(unittest.TestCase):
    def test_tree(self):
        tree = Tree()
        tree.set_root(1)
        root = tree.root
        node2 = TreeNode(2)
        node3 = TreeNode(3)
        root.add_child(node2, "to 2")
        root.add_child(node3, "to 3")

        tree.traverse()
        self.assertEqual(root.value, 1)
        self.assertIn(node2, root.children)

if __name__ == "__main__":
    print("Pliki w katalogu:", count_files("/dev"))
    list_files_recursive("/dev")
    
    text = "Ala ma kota, a kot ma Ale."
    words_to_remove = ["Ala", "kota"]
    replacements = {"Ala": "Ola", "kot": "gnom"}
    print("Po usunięciu:", remove_words(text, words_to_remove))
    print("Po zamianie:", replace_words(text, replacements))
    
    numbers = [random.randint(0, 100) for _ in range(10)]
    print("Liczby:", numbers)
    print("Sortowanie bąbelkowe:", bubble_sort(numbers[:]))
    print("Sortowanie szybkie:", quick_sort(numbers[:]))

    unittest.main()
