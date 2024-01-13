## Scrabble Helper
This program searches the language dictionary (by default Polish) and shows all possible words, that can be made from user provided characters.

Program can also search for simple patterns. Use "." for indicating missing letter and "*" to any length pattern. For example:

- pattern "cz.p.a", available letters "KLA", finds "czapka", "czapla"
- pattern "cza*", available letters "OKL", finds "czako", "czak"

## First Run
Before first run, please download the Scrabble dictionary.
Polish one is available for free at https://sjp.pl/sl/growy/.
Please unzip the file "slowa.txt" to the working directory and run the program.

During first run, dictionary will be parsed into trie data structure and saved as pickle, for faster subsequent startups.