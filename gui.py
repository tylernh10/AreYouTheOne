import tkinter as tk
from PIL import ImageTk
from tkinter.messagebox import showerror, showinfo
from game import *
from newweek import *
import random
import pygame

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg="#BA55D3")

        self.play_sound()

        self.title("Are You The One?")
        self.geometry('1200x900+50+50')
        self.resizable(False, False)
        self.iconbitmap("heart.ico") # C:\\Users\\tyler\\Desktop\\CSE 2050\\Honors Project\\project files\\heart.ico


        #background image + title
        self.bg = ImageTk.PhotoImage(file="love_bg.gif")
        self.my_canvas = tk.Canvas(self, width=900, height=500)
        self.my_canvas.pack(fill="both", expand=True)
        self.my_canvas.create_image(0, 0, image=self.bg, anchor="nw")
        self.my_canvas.create_text(600, 50, text="♥Are You The One?♥", font=("Cooper Black", 35), fill="white")
        self.my_canvas.create_text(600, 85, text="A game by Tyler Hinrichs", font=("Cooper Black", 15), fill="white")


        # some simple buttons 
        self.exit_btn = tk.Button(self, text='Exit', font=("Cooper Black", 15), width=5, height=1, command=self.destroy)
        self.exit_btn.place(x=600, y=840)

        self.help_btn = tk.Button(self, text='?', font=("Cooper Black", 15), width=5, height=1, command=lambda: showinfo(title='How to play!', 
                        message="In this game, you are trying to find all of the couples as fast as possible. Each round, choose who you think are the pairs. Then, you will be shown how many pairs are correct, and you can send one couple per round to the truth booth to see if they are a match. The goal is to find all matches in as few rounds as possible. On the left sidebar, you can click on a contestant to find out more info about them. Good luck!"))
        self.help_btn.place(x=500, y=840)

        self.music_button = tk.Button(self, text="♫", font=("Cooper Black", 15), width=5, height=0, command=lambda: pygame.mixer.quit() if pygame.mixer.get_init() else self.play_sound())
        self.music_button.place(x=1100, y=840)
        

        self.mode = [4, 6, 8, 10, 12, 14, 16]
        self.mode_mb = tk.Menubutton(self, text="Select Mode", font=("Cooper Black", 20), width=20, height=1, direction="below")
        self.mode_mb.menu = tk.Menu(self.mode_mb, tearoff=0)
        self.mode_mb["menu"] = self.mode_mb.menu
        for i in self.mode:
            self.mode_mb.menu.add_command(label=f"Number of Contestants: {i}", command=lambda i=i: self.play(i))
        self.mode_mb.place(x=430, y=450)

        self.player_buttons = None # dictionary that hold menu buttons for all players
        self.pair_buttons = [] # stores pair buttons for current round

        self.new_button = None
        self.truth_booth_button = None
        
        
        self.selections = []
        self.current_round = 0
        self.indices = []
        self.remaining = []
        self.n = 1
        self.var = 0
        self.found_matches = []
        self.affirmations = ["Well done!", "Good job!", "Way to go!", "Awesome work!"]
        self.e1 = None
        self.e2 = None

    
    def display_round_num(self, playgame):
        self.my_canvas.delete("round")
        self.my_canvas.create_text(600, 170, text=f"Round {self.current_round}", font=("Cooper Black", 25, "underline"), fill="white", tag = "round")




######################## BUTTONS ON LEFT SIDEBAR ########################
    def display_names(self, playgame): # game needs to be a PlayGame object
        contestants = playgame.randomize_and_set_pairs()
        my_string = "Contestant Info"
        x = 20
        y = 200
        buttons = dict()
        for player in contestants:
            mb = tk.Menubutton(self, text=player, font=("Cooper Black", 10), width=20, height=1, activebackground="#FF69B4", cursor="heart", direction="right")
            mb.menu = tk.Menu(mb, tearoff=0)
            mb["menu"] = mb.menu
            buttons[player] = mb
        
        for i in buttons:
            self.create_menu(buttons[i], i)

        for i in buttons:
            buttons[i].place(x=x, y=y)
            y += 30

        self.my_canvas.delete("starting_names")
        self.my_canvas.create_text(107, 175, text=my_string, font=("Cooper Black", 15), fill="white", tag = "starting_names")

        self.player_buttons = buttons
        return self.player_buttons

    def create_menu(self, mb, contestant): # adds a menu to each contestant button
        mb.menu.add_command(label="found match?", command=lambda: showinfo(title='Found Match?', message=f"{self.found_true_love_menu(contestant)}"))
        mb.menu.add_command(label="Who is not a match?", command=lambda: showinfo(title=f"confirmed not matches of {contestant}", message=f'confirmed not matches: {contestant.get_confirmed_not()}')) # showinfo of each contestant's confirmed_not_match function

    def found_true_love_menu(self, contestant):
        if contestant.found_match_yet():
            return f"TRUE. {contestant} has found a match. Their match is {contestant.get_partner()}."
        else:
            return f"FALSE. {contestant} has not found a match yet."




############################# Where main aspect of gameplay is run. this function is modeled after the original 'gameplay' function from game.py #############################
    def play(self, num_players):
        new = PlayGame(num_players)
        self.display_names(new)
        self.var = num_players // 2
        
        self.start_btn = tk.Button(self, text="New Game", font=("Cooper Black", 20), width=18, height=1, command=self.restart)
        self.start_btn.place(x=425, y=775)

        self.my_canvas.delete("all_have_been_chosen")
        self.my_canvas.delete("selections_this_round")
        self.mode_mb.destroy()
        self.current_round = 0
        self.function(new)
        
        
    def function(self, new, button=None):
        self.current_round += 1
        self.display_round_num(new)
        s = "No matches found yet!"
        self.my_canvas.delete("current_found_pairs")
        self.my_canvas.create_text(600, 210, text=f"current found pairs: {s if len(self.found_matches) == 0 else len(self.found_matches)}", font=("Cooper Black", 15), fill="white", tag = "current_found_pairs")

        self.my_canvas.delete("all_have_been_chosen")
        if button is not None: 
            button.destroy()
        self.my_canvas.delete("are_they_a_pair")
        self.my_canvas.delete("num_correct")
        self.my_canvas.delete("selections_this_round")
        

        self.remaining = [i for i in new._contestants if i not in new.found_list()]
        remaining_str = "CONTESTANTS:"
        for idx, person in enumerate(self.remaining):
            remaining_str += f"\n{idx+1}. {person}"
        self.my_canvas.delete("people_wo_matches")
        self.my_canvas.create_text(350, 400, text = remaining_str, font=("Cooper Black", 12), fill="white", tag="people_wo_matches")



        n = len(self.remaining)
        self.indices = list(range(1, n+1))

        self.my_canvas.delete("people_left_making_pairs")
        self.my_canvas.create_text(850, 265, text = f"people you haven't chosen yet this round: \n{self.indices}", font=("Cooper Black", 12), fill="white", tag="people_left_making_pairs")

        self.my_canvas.delete("current_pair_input")
        self.my_canvas.create_text(613, 396, text = f"Pair {self.n}", font=("Cooper Black", 20), fill="white", tag="current_pair_input")

        self.my_canvas.delete("entry")

        entry1 = tk.Entry(self, font=("Cooper Black", 15), justify="center", width=6)
        entry2 = tk.Entry(self, font=("Cooper Black", 15), justify="center", width=6)
        self.e1 = entry1
        self.e2 = entry2
        reg = self.register(self.callback)
        entry1.config(validate = "key", validatecommand = (reg, '%P'))
        entry2.config(validate = "key", validatecommand = (reg, '%P'))

        self.my_canvas.create_window(610, 425, window=entry1, tag="entry")
        self.my_canvas.create_window(700, 425, window=entry2, tag="entry")

        self.get_pair_btn = tk.Button(self, text="submit pair guess", font=("Cooper Black", 15), width=18, height=0, command=lambda: self.get_pair(entry1, entry2, self.indices, new))
        self.get_pair_btn.place(x=573, y=450)


    def get_pair(self, e1, e2, indices, playgame): # gets entry data
        p1 = e1.get()
        p2 = e2.get()
        e1.delete(0, 'end')
        e2.delete(0, 'end')
        print(p1, p2)

        if p1 == "" or p2 == "" or int(p1) not in indices or int(p2) not in indices: # makes sure p is a number that in valid limits and hasn't already been chosen
            showerror(title="invalid", message="there is an invalid entry")
        elif p1 == p2: # makes sure the user doesn't enter the same value
            showerror(title="invalid", message="a person cannot match with themselves")
        else:
            self.n += 1

            self.selections.append((self.remaining[int(p1)-1], self.remaining[int(p2)-1]))
            self.indices.remove(int(p1))
            self.indices.remove(int(p2))
            self.my_canvas.delete("people_left_making_pairs")
            self.my_canvas.create_text(850, 265, text = f"people you haven't chosen yet this round: \n{self.indices}", font=("Cooper Black", 12), fill="white", tag="people_left_making_pairs")


            if self.n > self.var:
                print("all pairs submitted")
                self.get_pair_btn.destroy()
                self.my_canvas.delete("current_pair_input")
                e1.destroy()
                e2.destroy()
                self.my_canvas.create_text(680, 400, text = f"All pairs chosen \nfor this round!", font=("Cooper Black", 15), fill="white", tag="all_have_been_chosen")
                self.my_canvas.delete("selections_this_round")
                self.my_canvas.create_text(1005, 450, text=self.selections_str(), font=("Cooper Black", 12), fill="white", tag="selections_this_round")
                self.n = 1
                new_week = NewWeek(playgame._secret_list_of_pairs, self.selections)
                print(playgame._secret_list_of_pairs)

                num_correct_matches = new_week.get_num_matches()
                self.my_canvas.create_text(880, 575, text = f"Number of Correct Matches: {num_correct_matches}", font=("Cooper Black", 20), fill="white", tag="num_correct")
                if num_correct_matches == 0:
                    self.truthbutton(new_week, playgame, True)
                elif num_correct_matches >= self.var - len(self.found_matches):
                    self.win_condition(playgame) 
                    for pair in self.selections:
                        pair[0].set_found()
                        pair[1].set_found()
                        pair[0].set_partner(pair[1])
                        pair[1].set_partner(pair[0])

                        self.my_canvas.delete("current_found_pairs")
                        self.my_canvas.create_text(600, 210, text=f"current found pairs: {self.var}", font=("Cooper Black", 15), fill="white", tag = "current_found_pairs")


                else:
                    self.truthbutton(new_week, playgame, False)
                return


            self.my_canvas.delete("current_pair_input")
            self.my_canvas.delete("selections_this_round")
            self.my_canvas.create_text(613, 396, text = f"Pair {self.n}", font=("Cooper Black", 20), fill="white", tag="current_pair_input")
            self.my_canvas.create_text(1005, 450, text=self.selections_str(), font=("Cooper Black", 12), fill="white", tag="selections_this_round")



    def truthbutton(self, newweek, playgame, no_matches):
        if no_matches:
            mb = tk.Menubutton(self, text="Truth Booth", font=("Cooper Black", 20), width=20, height=1)
            mb.menu = tk.Menu(mb, tearoff=0)
            mb["menu"] = mb.menu
            mb.menu.add_command(label=f"No matches! Send data.", command=lambda: self.truthbutton_helper(newweek, None, mb, playgame))
            mb.place(x=700, y=600)
            self.truth_booth_button = mb
        else:
            mb = tk.Menubutton(self, text="Truth Booth", font=("Cooper Black", 20), width=20, height=1)
            mb.menu = tk.Menu(mb, tearoff=0)
            mb["menu"] = mb.menu
            for i in range(len(self.selections)):
                mb.menu.add_command(label=f"Pair {i+1}", command=lambda i=i: self.truthbutton_helper(newweek, self.selections[i], mb, playgame))
            mb.place(x=700, y=600)
            self.truth_booth_button = mb

    def truthbutton_helper(self, newweek, selection, button, playgame):
        if selection is None:
            for pair in self.selections:
                pair[0].confirmed_not_match(pair[1])
                pair[1].confirmed_not_match(pair[0])
                button.destroy()
        else:
            x = newweek.truth_booth(selection)
            self.my_canvas.create_text(845, 675, text=f"Is {selection} a pair? {x}.", font=("Cooper Black", 15), fill="white", tag="are_they_a_pair")
            button.destroy()
            if x:
                self.found_matches.append(selection)

                selection[0].set_found()
                selection[1].set_found()
                selection[0].set_partner(selection[1])
                selection[1].set_partner(selection[0])

                self.remaining.remove(selection[0])
                self.remaining.remove(selection[1])

                if len(self.remaining) == 0 and len(self.indices) == 0:
                    self.win_condition(playgame)
            else:
                selection[0].confirmed_not_match(selection[1])
                selection[1].confirmed_not_match(selection[0])
    
        new_button = tk.Button(self, text="next_round", font=("Cooper Black", 15), width=18, height=0, command=lambda: self.function(playgame, new_button), activebackground="#FF69B4", cursor="heart")
        new_button.place(x=700, y=700)
        self.new_button = new_button
        self.selections.clear()

    def callback(self, input):
        if input.isdigit():
            return True
        elif input == "":
            return True
        else:
            return False

    def selections_str(self):
        select_str = "Chosen Pairs This Round:\n"
        for idx, pair in enumerate(self.selections):
            select_str += f"{idx+1}) {pair}\n"

        return select_str

        
    def win_condition(self, playgame):
        if self.current_round == 1:
            showinfo(title="Congratulations, you win!", message=f"You won! This took you {self.current_round} round. {random.choice(self.affirmations)} The matches are {playgame._secret_list_of_pairs}.")
        else:
            showinfo(title="Congratulations, you win!", message=f"You won! This took you {self.current_round} rounds. {random.choice(self.affirmations)} The matches are {playgame._secret_list_of_pairs}.")    

    def play_sound(self):
        pygame.mixer.init()
        pygame.mixer.music.load("fallinlove.mp3") # C:\\Users\\tyler\\Desktop\\CSE 2050\\Honors Project\\project files\\fallinlove.mp3
        pygame.mixer.music.play(loops=-1)
        self.playing = True

    def restart(self):
        if self.player_buttons is not None:
            for button in self.player_buttons.values():
                button.destroy()
        self.my_canvas.delete("starting_names")
        self.my_canvas.delete("round")
        self.my_canvas.delete("people_left_making_pairs")
        self.my_canvas.delete("people_wo_matches")
        self.my_canvas.delete("current_pair_input")
        self.my_canvas.delete("current_found_pairs")
        self.my_canvas.delete("all_have_been_chosen")
        self.my_canvas.delete("num_correct")
        self.my_canvas.delete("selections_this_round")
        self.my_canvas.delete("are_they_a_pair")
        self.get_pair_btn.destroy()
        if self.e1 is not None:
            self.e1.destroy()
        if self.e1 is not None:
            self.e2.destroy()
        if self.new_button is not None:
            self.new_button.destroy()
        if self.truth_booth_button is not None:
            self.truth_booth_button.destroy()

        self.player_buttons = None 
        self.pair_buttons = []

        self.selections = []
        self.current_round = 0
        self.indices = []
        self.remaining = []
        self.n = 1
        self.var = 0
        self.found_matches = []

        self.mode = [4, 6, 8, 10, 12, 14, 16]
        self.mode_mb = tk.Menubutton(self, text="Select Mode", font=("Cooper Black", 20), width=20, height=1, direction="below")
        self.mode_mb.menu = tk.Menu(self.mode_mb, tearoff=0)
        self.mode_mb["menu"] = self.mode_mb.menu
        for i in self.mode:
            self.mode_mb.menu.add_command(label=f"Number of Contestants: {i}", command=lambda i=i: self.play(i))
        self.mode_mb.place(x=430, y=450)

if __name__ == "__main__":
    app = App()
    
    try:
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)
    finally:
        app.mainloop()

