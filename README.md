## Are You The One?
#### A Game By Tyler Hinrichs

This was my honors project for CSE 2050, Data Structures and Object-Oriented Design, at the University of Connecticut in the Fall 2021 semester. The focus of the project was Object-Oriented Programming in Python, as well as creating a functional GUI to allow users to easily use the final product.

The premise of this project was very wide open, and largely open to interpretation. The only guideline was that the program was to function similarly to the reality TV show "Are You The One?" while using a GUI to recreate this. This is the wikipedia link to get a more specifc description of the official rules, which are vaguely mimicked here: https://en.wikipedia.org/wiki/Are_You_the_One%3F

Below I will outline some of the key features of gameplay:
1. Random users are selected, and secret pairs are made.
2. Each round, the user tries to guess who the pairs are. They are told how many guesses they have made are correct.
3. They are able to select one pair per round to go to the "truth booth" where they will get a definitive answer on whether this pair is a match or not.
4. Based on the results of the truth booth, each user will have data stored with it that says who is known to be a match or not a match with them. This can be accessed by the user to narrow down later guesses.
5. If the truth booth returns that no matches were made, each person in each pair has data stored that identifies their chosen partner that round is NOT their correct match.
6. The user tries to guess who all the matches are in as few rounds as possible.

The GUI was made using Python's tkinter. It allows the user to select how many total people they want to participate in each game. As the number of contestants increases, the game becomes tougher. A game with 4 contestants is quite easy to win. There is also functionality to toggle the background music, while clicking on the users on the left side of the screen allows more info to be found out about whether a match has been found (and who this match is if they have been found), as well as people who are known not to be matched with a given person. There is functionality to input contestants as numerical values and buttons appear with respect to where one is in the given round. 

This project was completed in December 2021, though at the time, I manually uploaded the project files to GitHub. I have now connected my local directory to the repo and have pushed some new changes. These changes consist of neatening up some of the files, adding a requirements.txt, as well as updating this README.md itself. Since December, no major changes have been made to the functionality of the program. Thanks for reading!