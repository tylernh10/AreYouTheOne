from contestant import Contestant
from newweek import NewWeek
import names
import random

class PlayGame:
    def __init__(self, num_players):
        self._contestants = []
        self._secret_list_of_pairs = []
        self._game_has_started = False

        self.found_pairs = []
        self.num_found = len(self.found_pairs)

        self.rounds_played = 0
        self.total_pairs = None
        self.num_players = num_players
    
    def randomize_and_set_pairs(self):
        if not self._game_has_started:
            self._game_has_started = True
            people = [names.get_full_name() for i in range(self.num_players)]
            random.shuffle(people)
            
            for i in people:
                self._contestants.append(Contestant(i))
            
            self.total_pairs = len(self._contestants) // 2

            for i in range(0, self.num_players, 2):
                self._secret_list_of_pairs.append((self._contestants[i], self._contestants[i+1]))
            random.shuffle(self._contestants)
            return self._contestants

        else:
            raise Exception("game has already started!")

    def found_list(self):
        found = []
        for pair in self.found_pairs:
            found.append(pair[0])
            found.append(pair[1])
        return found


    def gameplay(self):
        while self.num_found < self.total_pairs:
            s = "No matches found yet!"
            print(f"current found pairs: {s if self.num_found == 0 else [(str(i[0]), str(i[1])) for i in self.found_pairs]}")
            
            remaining = [i for i in self._contestants if i not in self.found_list()]
            print("People without matches:")
            for idx, person in enumerate(remaining):
                print(f"\t{idx+1}. {person}")

            print()
            print(f"Time to pick your matches for round {self.rounds_played+1}.")
            print()

            n = len(remaining)
            indices = list(range(n))
            selections = []
            for i in range(n // 2):
                print(f"people you haven't chosen yet: {indices}")
                print(f"Pair {i + 1}:")
                x = int(input("person 1: "))
                y = int(input("person 2: "))
                selections.append((remaining[x], remaining[y]))
                indices.remove(x)
                indices.remove(y)

            new_week = NewWeek(self._secret_list_of_pairs, selections)
            self.rounds_played += 1
            num_matches = new_week.get_num_matches()

            if num_matches == self.total_pairs or num_matches == self.total_pairs - len(self.found_pairs):
                break

            print()
            print(f"You have created {num_matches} correct matches.")
            print()
            print("Next, select a couple to go to the truth booth:")
            for i, pair in enumerate(selections):
                print(f"pair {i+1}: {pair[0]} and {pair[1]}")
            print()
            truth_booth_pair = int(input("select a pair: "))
            truth_check = new_week.truth_booth(selections[truth_booth_pair - 1])
            if truth_check:
                x = selections[truth_booth_pair - 1]
                self.found_pairs.append(x)
                selections.remove(x)
                x[0].set_found()
                x[1].set_found()
                self.num_found += 1
                print("this pair is a couple!")
            else:
                print("this pair is not a couple")

        
        affirmations = ["Well done!", "Good job!", "You're a winner!", "Awesome work!"]
        print(f"All matches have been found! This took you {self.rounds_played} rounds. {random.choice(affirmations)}")    

if __name__ == "__main__":
    test = PlayGame(4)
    test.randomize_and_set_pairs()

    test.gameplay()

    # This file will simulate gameplay in terminal. Run the file to play the game without a GUI.