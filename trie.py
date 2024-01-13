import pickle
from typing import List, Optional
import re


class TrieNode:
    def __init__(self) -> None:
        self.children = None
        self.is_valid_word = False

    def register(self, word: str):
        first_letter = word[0]
        remainder = word[1:]
        if self.children is None:
            self.children = dict()
        if first_letter not in self.children:
            child = TrieNode()
            self.children[first_letter] = child
        else:
            child = self.children[first_letter]

        if not remainder:
            child.is_valid_word = True
        else:
            child.register(remainder)


def find_possible_words(trie: TrieNode, letters: str, filter_regex=None, _result: List[str] = None, _root_word="") -> \
List[str]:
    if _result is None:
        _result = []
    if trie.children is None:
        return _result

    for i in range(len(letters)):
        current_letter = letters[i]
        other_letters = [letters[j] for j in range(len(letters)) if j != i]

        for child_letter, child in trie.children.items():
            if current_letter == child_letter or current_letter == "?":
                new_word = f"{_root_word}{child_letter}"
                if child.is_valid_word:
                    if not filter_regex or re.match(filter_regex, new_word):
                        _result.append(new_word)
                if other_letters:
                    find_possible_words(child, other_letters, filter_regex, _result, new_word)
    if _root_word == "":
        _result = list(sorted(sorted(set(_result)), key=len, reverse=True))
    return _result


def has_word(trie: TrieNode, word: str) -> Optional[TrieNode]:
    """ Returns trie child that represents last letter of the word (None if not found) """
    current_level = trie
    for letter in word:
        if current_level.children is None:
            return None
        if letter in current_level.children:
            current_level = current_level.children[letter]
        else:
            return None
    return current_level


def read_pickle(pickle_file: str) -> TrieNode:
    print("Reading dictionary pickle")
    with open(pickle_file, "rb") as p:
        trie_root = pickle.load(p)
        return trie_root


def read_dictionary(dict_file, encoding="cp1250") -> TrieNode:
    trie_root = TrieNode()
    print("Reading dictionary file")
    with open(dict_file, "rt", encoding=encoding) as f:
        for i, line in enumerate(f):
            trie_root.register(line.strip())
    print("Done")
    return trie_root


def write_pickle(root: TrieNode, pickle_file: str):
    print("Writing pickle")
    with open(pickle_file, "wb") as p:
        pickle.dump(root, p)
