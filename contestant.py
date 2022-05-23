class Contestant:
    def __init__(self, name):
        self._name = name
        self._partner_name = None
        self._found_match = False
        self._confirmed_not_matches = []

    def get_name(self):
        return self._name

    def set_partner(self, name):
        self._partner_name = name

    def get_partner(self):
        return self._partner_name

    def found_match_yet(self):
        return self._found_match

    def set_found(self):
        self._found_match = True
    
    def confirmed_not_match(self, c): # adds a contestant to the self._confirmed_not_matches list; this is used only in the case that the number of correct matches is 0
        if c not in self._confirmed_not_matches:
            self._confirmed_not_matches.append(c)
    
    def get_confirmed_not(self):
        if len(self._confirmed_not_matches) == 0:
            return f"No one has been confirmed to not be {self.get_name()}'s match yet."
        else:
            return self._confirmed_not_matches

    def __str__(self):
        return self.get_name()

    def __repr__(self):
        return self.get_name()



if __name__ == "__main__":
    import names
    n = 8
    people = [names.get_full_name() for i in range(n)]
    contestant_list = []
    for i in people:
        contestant_list.append(Contestant(i))

    for i in contestant_list:
        print(i)

    people = [names.get_full_name() for i in range(16)]
    print(people)


