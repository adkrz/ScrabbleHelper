from PyQt5.QtWidgets import QDialog, QApplication, QLabel, QLineEdit, QTextBrowser, QVBoxLayout, QToolButton, \
    QPlainTextEdit
from PyQt5.QtCore import Qt

from trie import read_pickle, read_dictionary, write_pickle, find_possible_words
import os
import sys


class Helper(QDialog):
    dictionary_txt_file = "../slowa.txt"
    dictionary_txt_encoding = "utf-8"
    dictionary_pickle_file = "../dict.pickle"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._init_gui()
        if os.path.exists(self.dictionary_pickle_file):
            self.trie_root = read_pickle(self.dictionary_pickle_file)
        elif os.path.exists(self.dictionary_txt_file):
            self.trie_root = read_dictionary(self.dictionary_txt_file, self.dictionary_txt_encoding)
            write_pickle(self.trie_root, self.dictionary_pickle_file)
        else:
            raise Exception("Neither dictionary TXT or pickled trie file is present. "
                            "Please download dictionary from https://sjp.pl/sl/growy/ and unzip txt file.")
        print("Starting GUI...")

    def _init_gui(self):
        layout = QVBoxLayout()
        lbl1 = QLabel("Litery do wyłożenia:")
        self.line_edit_letters = QLineEdit()
        self.line_edit_letters.returnPressed.connect(self._search)
        layout.addWidget(lbl1)
        layout.addWidget(self.line_edit_letters)
        lbl2 = QLabel("Wzory do dopasowania:\n. -> litera, * -> ciąg znaków:")
        self.line_edit_pattern = QPlainTextEdit()
        layout.addWidget(lbl2)
        layout.addWidget(self.line_edit_pattern)
        self.setLayout(layout)
        btn_find = QToolButton()
        btn_find.setText("Szukaj")
        btn_find.clicked.connect(self._search)
        layout.addWidget(btn_find)
        self.results = QTextBrowser()
        layout.addWidget(self.results)
        self.setWindowTitle("Scrabble Helper")

    def _search(self):
        self.results.clear()
        patterns = self.line_edit_pattern.toPlainText().lower()
        patterns = patterns.split("\n")
        seen = set()
        seen_add = seen.add
        patterns = [x for x in patterns if not (x in seen or seen_add(x))]

        found_words = {}

        for raw_pattern in patterns:
            raw_pattern = raw_pattern.strip()
            pattern = self._simple_expr_to_regex(raw_pattern)
            letters_from_pattern = [char for char in pattern if char >= 'a' and char <= 'ż']
            letters_from_pattern = "".join(letters_from_pattern)
            possible_letters = self.line_edit_letters.text().lower().strip()
            possible_letters += letters_from_pattern
            result = find_possible_words(self.trie_root, possible_letters, pattern)
            # Exclude pattern itself:
            result = [r for r in result if r != letters_from_pattern]
            found_words[raw_pattern] = result

        if found_words and len(patterns) > 1:
            longest_word = ""
            for_pattern = ""
            for raw_pattern, result in found_words.items():
                for word in result:
                    if len(word) > len(longest_word):
                        longest_word = word
                        for_pattern = raw_pattern
            self.results.append(f"Najdłuższe słowo: z <b>{for_pattern}</b>")
            self.results.setAlignment(Qt.AlignCenter)
            self.results.append(longest_word)
            self.results.setAlignment(Qt.AlignLeft)

        for raw_pattern, result in found_words.items():
            if len(found_words) > 1:
                ptrn = raw_pattern if raw_pattern else "Pusty"
                self.results.append(f"<b>{ptrn}</b>")
                self.results.setAlignment(Qt.AlignCenter)
            self.results.append("<br>".join(result))
            self.results.setAlignment(Qt.AlignLeft)
        cursor = self.results.textCursor()
        cursor.setPosition(0)
        self.results.setTextCursor(cursor)

    @staticmethod
    def _simple_expr_to_regex(expr: str) -> str:
        if not expr.startswith(".") and not expr.startswith("*") and not expr.endswith(".") and not expr.endswith("*"):
            expr = f".*{expr}.*"
            return expr
        expr = expr.replace("*", ".*")
        expr = f"^{expr}$"
        return expr


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Helper()
    win.show()
    sys.exit(app.exec_())
