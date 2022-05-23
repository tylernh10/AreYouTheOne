class NewWeek:
    def __init__(self, secret_pairs, current_guesses):
        self._secret_pairs = secret_pairs
        self._current_guesses = current_guesses

    def get_num_matches(self): # the running total of correct matches should be kept somewhere --> visually, the pairs that have already been matched should be moved to one side of the screen and those pairs removed from current guesses 
        num_correct = 0
        for pair in self._current_guesses:
            if pair in self._secret_pairs or pair[::-1] in self._secret_pairs:
                num_correct += 1
        return num_correct
        

    def truth_booth(self, pair):
        return pair in self._secret_pairs or pair[::-1] in self._secret_pairs

if __name__ == "__main__":
    pass