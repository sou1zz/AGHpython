from collections import defaultdict, deque

class AhoCorasick:
    def __init__(self):
        self.trie = defaultdict(dict)
        self.output = defaultdict(list)
        self.fail = {}

    def add_word(self, word):
        node = 0
        for char in word:
            node = self.trie[node].setdefault(char, len(self.trie))
        self.output[node].append(word)

    def build(self):
        self.fail = {}
        queue = deque()
        
        for node in self.trie[0].values():
            self.fail[node] = 0
            queue.append(node)

        while queue:
            current = queue.popleft()
            for char, child in self.trie[current].items():
                queue.append(child)
                fallback = self.fail[current]
                while fallback and char not in self.trie[fallback]:
                    fallback = self.fail[fallback]
                self.fail[child] = self.trie[fallback].get(char, 0)
                self.output[child].extend(self.output[self.fail[child]])

    def search(self, text):
        node = 0
        results = []
        for i, char in enumerate(text):
            while node and char not in self.trie[node]:
                node = self.fail[node]
            node = self.trie[node].get(char, 0)
            if self.output[node]:
                for match in self.output[node]:
                    results.append((i - len(match) + 1, match))
        return results

ac = AhoCorasick()
ac.add_word("he")
ac.add_word("she")
ac.add_word("his")
ac.add_word("hers")
ac.build()
print(ac.search("ushers"))
