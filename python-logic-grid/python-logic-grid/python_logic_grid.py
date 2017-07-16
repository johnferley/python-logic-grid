import pickle
import textwrap
import pathlib
import os

def search(p, ps):
    return any(p in search for search in ps)

class Node():
    def __init__(self, action):
        children = []
    def up(self):
        pass
    def down(self, target):
        pass

class Rule():
    def __init__(self, p1, r, p2, grid, text):
        self.p1 = p1
        self.p2 = p2
        self.r = r
        self.grid = grid
        self.text = text
    def __str__(self):
        output = self.text.format(self.p1, self.r, self.p2)
        return output
    def validate(self):
        if self.r != "At":
            p1_cells = self.grid.find_property(self.p1)
            p2_cells = self.grid.find_property(self.p2)
            if self.r == "Left":
                for p1_cell in p1_cells:
                    ok = False
                    for p2_cell in p2_cells:
                        if p1_cell[1] == p2_cell[1] - 1:
                            ok = True
                            break
                    if not ok:
                        self.grid.values[p1_cell[0]][p1_cell[1]] = ""
                for p2_cell in p2_cells:
                    ok = False
                    for p1_cell in p1_cells:
                        if p2_cell[1] == p1_cell[1] + 1:
                            ok = True
                            break
                    if not ok:
                        self.grid.values[p2_cell[0]][p2_cell[1]] = ""
            elif self.r == "Right":
                for p1_cell in p1_cells:
                    ok = False
                    for p2_cell in p2_cells:
                        if p1_cell[1] == p2_cell[1] + 1:
                            ok = True
                            break
                    if not ok:
                        self.grid.values[p1_cell[0]][p1_cell[1]] = ""
                for p2_cell in p2_cells:
                    ok = False
                    for p1_cell in p1_cells:
                        if p2_cell[1] == p1_cell[1] - 1:
                            ok = True
                            break
                    if not ok:
                        self.grid.values[p2_cell[0]][p2_cell[1]] = ""
            elif self.r == "Has":
                for p1_cell in p1_cells:
                    ok = False
                    for p2_cell in p2_cells:
                        if p2_cell[1] == p1_cell[1]:
                            ok = True
                            break
                    if not ok:
                        self.grid.values[p1_cell[0]][p1_cell[1]] = ""
                for p2_cell in p2_cells:
                    ok = False
                    for p1_cell in p1_cells:
                        if p1_cell[1] == p2_cell[1]:
                            ok = True
                            break
                    if not ok:
                        self.grid.values[p2_cell[0]][p2_cell[1]] = ""
            elif self.r == "Neighbor":
                for p1_cell in p1_cells:
                    ok = False
                    for p2_cell in p2_cells:
                        if p1_cell[1] == p2_cell[1] - 1 or p1_cell[1] == p2_cell[1] + 1:
                            ok = True
                            break
                    if not ok:
                        self.grid.values[p1_cell[0]][p1_cell[1]] = ""
                for p2_cell in p2_cells:
                    ok = False
                    for p1_cell in p1_cells:
                        if p2_cell[1] == p1_cell[1] - 1 or p2_cell[1] == p1_cell[1] + 1:
                            ok = True
                            break
                    if not ok:
                        self.grid.values[p2_cell[0]][p2_cell[1]] = ""
        else:
            for row in range(0, len(self.grid.values)):
                for col in range(0, self.grid.no_of_properties):
                    test = self.grid.values[row][col]
                    ok = False
                    for property in self.grid.properties:
                        if test in property and self.p1 in property:
                            ok = True
                    if ok:
                        if self.grid.values[row][col] != self.p1 and str(col + 1) == self.p2:
                            self.grid.values[row][col] = ""
                        elif self.grid.values[row][col] == self.p1 and str(col + 1) != self.p2:
                            self.grid.values[row][col] = ""

class Grid():
    def __init__(self):
        self.intro = ""
        self.initialised = False
        self.values = []
        self.rules = []
        self.properties = []
        self.RELATIONS = ["Left", "Right", "Has", "Neighbor", "At"]
        self.locations = []
        self.no_of_properties = 0
        self.no_of_combinations = 0
        self.output_text = ""
    def build_grid(self):
        if self.initialised:
            self.values = []
            for property in self.properties:
                for each in property:
                    temp = [each for x in range(0, self.no_of_properties)]
                    self.values.append(temp)
    def __str__(self):
        l = 0
        output = self.intro
        output += "\n"
        output += "\n"
        for rule in self.rules:
            output += str(rule)
            output += "\n"
        output += "\n"
        for row in self.values:
            for col in row:
                if len(col) > l:
                    l = len(col)
        for i in range(0, self.no_of_properties):
            output += "+"
            output += "-" * l
        output += "+"
        output += "\n"
        for loc in self.locations:
            output += "|"
            output += "{message: <{fill}}".format(message=str(loc), fill=str(l))
        output += "|"
        output += "\n"
        for i in range(0, self.no_of_properties):
            output += "+"
            output += "-" * l
        output += "+"
        output += "\n"
        for row in range(0, len(self.values)):
            for col in self.values[row]:
                output += "|"
                output += "{message: <{fill}}".format(message=col, fill=str(l))
            output += "|"
            output += "\n"
            if row % self.no_of_properties == 4:
                for i in range(0, self.no_of_properties):
                    output += "+"
                    output += "-" * l
                output += "+"
                output += "\n"
        output += "\n"
        for house in range(0, len(self.locations)):
            temp = [None for x in range(0, self.no_of_properties)]
            for i in range(0, self.no_of_properties):
                s = ""
                for row in range(0 + (i * self.no_of_combinations), self.no_of_combinations + (i * self.no_of_combinations)):
                    s += self.values[row][house]
                temp[i] = s
            output += self.output_text.format(self.locations[house], temp[0], temp[1], temp[2], temp[3], temp[4])
            output += "\n"
        return output.rstrip()
    def add_rule(self, p1, r, p2, text):
        if self.initialised:
            if r == "At":
                if search(p1, self.properties) and search(p2, self.locations) and search(r, self.RELATIONS):
                    self.rules.append(Rule(p1, r, p2, self, text))
                else:
                    print("Invalid parameters:",p1,r,p2)
            else:
                if search(p1, self.properties) and search(p2, self.properties) and search(r, self.RELATIONS):
                    self.rules.append(Rule(p1, r, p2, self, text))
                else:
                    print("Invalid parameters:",p1,r,p2)
    def add_properties(self, p, i = None):
        if self.initialised:
            if i == None:
                if isinstance(p, list):
                    while len(p) < self.no_of_combinations:
                        p.append(None)
                    while len(p) > self.no_of_combinations:
                        for each in self.properties:
                            while len(each) < len(p):
                                each.append(None)
                    self.properties.append(p)
            else:
                if isinstance(p, list):
                    self.properties[i] += p1
                    l = len(properties[i])
                    for each in properties:
                        while len(each) < len(l):
                            each.append(None)
                else:
                    self.properties[i].append(str(p))
                    l = len(self.properties[i])
                    for each in self.properties:
                        while len(each) < len(l):
                            each.append(None)
        else:
            if isinstance(p, list) and i == None:
                self.properties.append(p)
                self.initialised = True
        self.no_of_properties = len(self.properties)
        self.no_of_combinations = len(self.properties[0])
    def change_properties(self, p1, p2):
        if self.initialised:
            self.no_of_properties = len(self.properties)
            self.no_of_combinations = len(self.properties[0])
    def remove_properties(self, p):
        if self.initialised:
            self.no_of_properties = len(self.properties)
            self.no_of_combinations = len(self.properties[0])
    def add_locations(self, l):
        if isinstance(l, list):
            self.locations += l
        else:
            self.locations.append(str(l))
    def change_locations(self, p1, p2):
        pass
    def remove_locations(self, p):
        pass
    def change_intro(self, s):
        self.intro = s
    def change_output_text(self, s):
        self.output_text = s
    def find_property(self, p):
        if self.initialised:
            results = []
            if not search(p, self.properties):
                print("Invalid property:", p)
            else:
                for row in range(0, len(self.values)):
                    for col in range(0, self.no_of_properties):
                        if self.values[row][col] == p:
                            results.append([row,col])
            return results
    def solve(self):
        if self.initialised:
            for rule in self.rules:
                rule.validate()
            counter = 0
            for prop in range(0, self.no_of_properties):
                for row in range(0 + (prop * self.no_of_combinations), self.no_of_combinations + (prop * self.no_of_combinations)):
                    if self.values[row].count("") == len(self.values[row]) - 1:
                        for property in self.values[row]:
                            if property != "":
                                i = row
                                j = self.values[row].index(property)
                                break
                        for row2 in range(0 + (prop * self.no_of_combinations), self.no_of_combinations + (prop * self.no_of_combinations)):
                            if self.values[row2][j] != "" and row2 != i:
                                counter += 1
                                self.values[row2][j] = ""
                for col in range(0, self.no_of_properties):
                    n = 0
                    for row in range(0 + (prop * self.no_of_combinations), self.no_of_combinations + (prop * self.no_of_combinations)):
                        if self.values[row][col] != "":
                            n += 1
                            i = row
                            j = col
                    if n == 1:
                        for col2 in range(0, self.no_of_properties):
                            if col2 != j and self.values[i][col2] != "":
                                counter += 1
                                self.values[i][col2] = ""

            if counter > 0:
                self.solve()
    def solution(self):
        output = []
        for house in range(0, len(self.locations)):
            temp = [None for x in range(0, self.no_of_properties)]
            for i in range(0, self.no_of_properties):
                s = ""
                for row in range(0 + (i * self.no_of_combinations), self.no_of_combinations + (i * self.no_of_combinations)):
                    s += self.values[row][house]
                temp[i] = s
            output.append(self.output_text.format(self.locations[house], temp[0], temp[1], temp[2], temp[3], temp[4]))
        return output
    def status(self):
        if self.initialised:
            output = []
            output.append("Intro:")
            output.append(self.intro)
            output.append("")
            output.append("Solution Format:")
            output.append(self.output_text.format("{0}", "{1}", "{2}", "{3}", "{4}", "{5}"))
            output.append("")
            output.append("Locations:")
            temp = "{0} "
            for each in self.locations:
                temp += each
                temp += ", "
            temp = temp [:-2]
            output.append(temp)
            output.append("")
            output.append("Parameters:")
            first = True
            counter = 1
            for each in self.properties:
                temp = "{"+str(counter)+"} "
                counter += 1
                for item in each:
                   temp += item
                   temp += ", "
                temp = temp [:-2]
                output.append(temp)
            output.append("")
            output.append("Rules:")
            for each in self.rules:
                output.append("- " + str(each))
            return output
        else:
            return ["Puzzle uninitialised, add some parameters and rules."]

class UI_Text():
    def __init__(self, parent, max_width):
        self.level = 0
        self.max_width = max_width
        self.width = max_width
        self.set_width()
        self.parent = parent
        self.divided = False
        self.numbering = 0
        self.no_options = 0
        self.display_divider()
        self.display_text("Welcome to the Logic Grid Solver")
        self.display_divider()
        self.display_text("Select options by typing the number and pressing enter.")
        self.display_divider()
        self.main_loop()
    def set_width(self):
        hw = os.get_terminal_size()
        if hw[0] - 3 > self.max_width:
            self.width = self.max_width
        else:
            self.width = hw[0] - 3
    def main_loop(self):
        while self.level != -1:
            self.set_width()
            self.display_menu()
        self.display_divider()
        self.display_text("Closing...")
        self.display_divider()
    def display_divider(self):
        self.set_width()
        if self.divided == False:
            self.divided = True
            print("+",end="")
            print("-" * self.width,end="")
            print("+",end="\n")
    def display_text(self, text, indent = 0, margin = 1):
        self.set_width()
        self.divided = False
        self.numbering = 0
        if len(text) + len(" " * indent) + 2 * len(" " * margin) <= self.width:
            text = (" " * indent) + (" " * margin) + text + (" " * margin)
            print("|",end="")
            print("{message: <{fill}}".format(message=text, fill=str(self.width)),end="")
            print("|",end="\n")
        else:
            text = textwrap.wrap(text, width = self.width - (len(" " * indent) + 2 * len(" " * margin)))
            for line in text:
                print("|",end="")
                print(" " * margin,end="")
                print(" " * indent,end="")
                print("{message: <{fill}}".format(message=line, fill=str(self.width - (len(" " * indent) + 2 * len(" " * margin)))),end="")
                print(" " * margin,end="")
                print("|",end="\n")
    def display_input(self, text, indent = 0, margin = 1):
        self.set_width()
        self.divided = False
        self.numbering = 0
        if len(text) + len(" " * indent) + 2 * len(" " * margin) <= self.width:
            text = (" " * indent) + (" " * margin) + text + (" " * margin)
            string = "|"
            string += "{message: <{fill}}".format(message=text, fill=str(self.width))
            string += "|\n"
        else:
            text = textwrap.wrap(text, width = self.width - (len(" " * indent) + 2 * len(" " * margin)))
            string = ""
            for line in text:
                string += "|"
                string += " " * margin
                string += " " * indent
                string += "{message: <{fill}}".format(message=line, fill=str(self.width - (len(" " * indent) + 2 * len(" " * margin))))
                string += " " * margin
                string += "|\n"
        string += "+"
        string += "-" * self.width
        string += "+\n>>> "
        output = input(string)
        return output
    def display_numbered(self, text, style = ":", indent = 0, margin = 1):
        if "0" in style:
            style = style.split("0")
        self.set_width()
        self.divided = False
        self.numbering += 1
        self.no_options = self.numbering
        if isinstance(style, list):
            number = (" " * indent) + style[0] + str(self.numbering) + style[1] + " "
        else:
            number = (" " * indent) + str(self.numbering) + style + " "
        if len(text) + len(number) + 2 * len(" " * margin) <= self.width:
            print("|" + (" " * margin) + str(number),end="")
            print("{message: <{fill}}".format(message=text, fill=str(self.width - (2 * len(" " * margin) + len(number)))),end="")
            print(" " * margin,end="")
            print("|",end="\n")
        else:
            text = textwrap.wrap(text, width = self.width - (len(number) + 2 * len(" " * margin)))
            first = True
            for line in text:
                if first:
                    print("|" + (" " * margin) + str(number),end="")
                    first = False
                else:
                    print("|",end="")
                    print(" "*(len(number) + margin),end="")
                print("{message: <{fill}}".format(message=line, fill=str(self.width - (2 * len(" " * margin) + len(number)))),end="")
                print(" " * margin, end="")
                print("|",end="\n")
    def display_bullet(self, text, style = "-", indent = 0, margin = 1):
        self.set_width()
        self.divided = False
        self.numbering = 0
        style = (" " * indent) + style + " "
        if len(text) + len(style) + 2 * len(" " * margin) <= self.width:
            print("|" + (" " * margin) + str(style),end="")
            print("{message: <{fill}}".format(message=text, fill=str(self.width - (2 * len(" " * margin) + len(style)))),end="")
            print(" " * margin, end="")
            print("|",end="\n")
        else:
            text = textwrap.wrap(text, width = self.width - (len(style) + 2 * len(" " * margin)))
            first = True
            for line in text:
                if first:
                    print("|" + (" " * margin) + str(style),end="")
                    first = False
                else:
                    print("|",end="")
                    print(" "*(len(style) + margin),end="")
                print("{message: <{fill}}".format(message=line, fill=str(self.width - (2 * len(" " * margin) +len(style)))),end="")
                print(" " * margin, end="")
                print("|",end="\n")
    def display_menu(self):
        self.set_width()
        self.display_divider()
        self.display_status()
        self.display_divider()
        if self.level == 0:
            self.display_divider()
            self.display_text("MAIN MENU")
            self.display_divider()
            self.display_numbered("New Puzzle")
            self.display_numbered("Load puzzle")
            self.display_numbered("Save puzzle")
            self.display_numbered("Edit puzzle")
            self.display_numbered("Solve puzzle")
            self.display_numbered("Help")
            self.display_text("0: Exit")
            self.display_divider()
            input_ok = False
            while not input_ok:
                self.display_divider()
                selection = self.display_input("Make a selection: ")
                self.display_divider()
                try:
                    selection = int(selection)
                    if selection in range(0, self.no_options + 1):
                        input_ok = True
                    else:
                        self.display_divider()
                        self.display_text("Error: Please enter a number between 0 and "+str(self.no_options)+".")
                        self.display_divider()
                except:
                    self.display_divider()
                    self.display_text("Error: Please enter a number.")
                    self.display_divider()
            self.no_options = 0
            if selection == 0:
                self.level = -1
            elif selection == 1:
                self.level = 1
            elif selection == 2:
                self.level = 2
            elif selection == 3:
                self.level = 3
            elif selection == 4:
                self.level = 4
            elif selection == 5:
                self.level = 5
            elif selection == 6:
                self.level = 6
        elif self.level == 1:
            self.display_divider()
            self.display_text("NEW PUZZLE")
            self.display_divider()
            check = self.display_input("This will clear the current puzzle, continue?").upper()
            self.display_divider()
            if check in ["Y", "YES", ""]:
                ok = True
            if ok:
                self.parent.puzzle = Grid()
            self.level = 0
        elif self.level == 2:
            self.display_divider()
            self.display_text("LOAD PUZZLE")
            self.display_divider()
            found = False
            while not found:
                self.display_divider()
                filename = self.display_input("Enter the filename of the puzzle to load (0 to cancel):")
                self.display_divider()
                if filename == "0":
                    found = True
                else:
                    if not filename.endswith(".pkl"):
                        filename += ".pkl"
                    filename = pathlib.Path(filename)
                    if filename.is_file():
                        found = True
                    else:
                        self.display_divider()
                        self.display_text("File not found")
                        self.display_divider()
            if isinstance(filename, pathlib.Path):
                self.display_divider()
                self.display_text("Loading puzzle...")
                self.display_divider()
                self.parent.load_puzzle(filename)
            self.level = 0
        elif self.level == 3:
            self.display_divider()
            self.display_text("SAVE PUZZLE")
            self.display_divider()
            file_ok = False
            while not file_ok:
                self.display_divider()
                filename = self.display_input("Enter the filename to save th puzzle to (0 to cancel):")
                self.display_divider()
                if filename == "0":
                    file_ok = True
                else:
                    if not filename.endswith(".pkl"):
                        filename += ".pkl"
                    filename = pathlib.Path(filename)
                    if filename.is_file():
                        self.display_divider()
                        check = self.display_input("The file already exists, overwrite?").upper()
                        self.display_divider()
                        if check in ["Y", "YES", ""]:
                            file_ok = True
                    else:
                        file_ok = True
            if isinstance(filename, pathlib.Path):
                self.display_divider()
                self.display_text("Saving puzzle...")
                self.display_divider()
                self.parent.save_puzzle(filename)
            self.level = 0
        elif self.level == 4:
            self.display_divider()
            self.display_text("EDIT PUZZLE")
            self.display_divider()
            self.display_numbered("Show Puzzle")
            self.display_numbered("Puzzle Settings")
            self.display_numbered("Edit Parameters")
            self.display_numbered("Edit Locations")
            self.display_numbered("Edit Rules")
            self.display_text("0: Main Menu")
            self.display_divider()
            input_ok = False
            while not input_ok:
                self.display_divider()
                selection = self.display_input("Make a selection: ")
                self.display_divider()
                try:
                    selection = int(selection)
                    if selection in range(0, self.no_options + 1):
                        input_ok = True
                    else:
                        self.display_divider()
                        self.display_text("Error: Please enter a number between 0 and "+str(self.no_options)+".")
                        self.display_divider()
                except:
                    self.display_divider()
                    self.display_text("Error: Please enter a number.")
                    self.display_divider()
            self.no_options = 0
            if selection == 0:
                self.level = 0
            elif selection == 1:
                self.level = 7
            elif selection == 2:
                self.level = 8
            elif selection == 3:
                self.level = 9
            elif selection == 4:
                self.level = 10
            elif selection == 5:
                self.level = 11
        elif self.level == 5:
            self.display_divider()
            self.display_text("SOLUTION")
            self.display_divider()
            if self.parent.puzzle.initialised:
                self.display_divider()
                solutions = self.parent.puzzle.solution()
                for each in solutions:
                    self.display_bullet(each)
                self.display_divider()
                self.display_input("Press any key to return to the main menu.")
                self.display_divider()
            else:
                self.display_divider()
                self.display_text("Puzzle not initialised, please enter some parameters.")
                self.display_input("Press any key to return to the main menu.")
                self.display_divider()
            self.level = 0
        elif self.level == 6:
            self.display_divider()
            self.display_text("HELP")
            self.display_divider()
            self.display_bullet("Navigate the menus by entering the corresponding key and pressing enter.")
            self.display_bullet("Puzzles can be saved or loaded from *.pkl files.")
            self.display_bullet("Make sure all the parameters and rules/clues have been set up before selecting solve.")
            self.display_bullet("The text above each menu shows a summary of the current puzzle.")
            self.display_bullet("The puzzle has not had any parameters set","Puzzle Uninitialised:",2)
            self.display_bullet("The number of locations","Loc:",2)
            self.display_bullet("The number of parameters","Para:",2)
            self.display_bullet("The number of combinations for each parameter","Comb:",2)
            self.display_bullet("The number of rules","Rules:",2)
            self.display_divider()
            self.display_input("Press any key to return to the main menu.")
            self.display_divider()
            self.level = 0
        elif self.level == 7:
            self.display_divider()
            self.display_text("CURRENT PUZZLE")
            self.display_divider()
            for each in self.parent.puzzle.status():
                self.display_text(each)
            self.display_divider()
            self.display_input("Press any key to return to the edit puzzle menu.")
            self.display_divider()
            self.level = 4
        elif self.level == 8:
            self.display_divider()
            self.display_text("SETTINGS")
            self.display_divider()
            self.display_numbered("Edit Information")
            self.display_numbered("Edit Solution Format")
            self.display_text("0: Edit Menu")
            self.display_divider()
            input_ok = False
            while not input_ok:
                self.display_divider()
                selection = self.display_input("Make a selection: ")
                self.display_divider()
                try:
                    selection = int(selection)
                    if selection in range(0, self.no_options + 1):
                        input_ok = True
                    else:
                        self.display_divider()
                        self.display_text("Error: Please enter a number between 0 and "+str(self.no_options)+".")
                        self.display_divider()
                except:
                    self.display_divider()
                    self.display_text("Error: Please enter a number.")
                    self.display_divider()
            self.no_options = 0
            if selection == 0:
                self.level = 4
            elif selection == 1:
                self.level = 12
            elif selection == 2:
                self.level = 13
        elif self.level == 9:
            self.display_divider()
            self.display_text("PARAMETERS")
            self.display_divider()
            self.display_numbered("Show Parameters")
            self.display_numbered("Add Parameters")
            self.display_numbered("Edit Parameters")
            self.display_numbered("Remove Parameters")
            self.display_text("0: Edit Menu")
            self.display_divider()
            input_ok = False
            while not input_ok:
                self.display_divider()
                selection = self.display_input("Make a selection: ")
                self.display_divider()
                try:
                    selection = int(selection)
                    if selection in range(0, self.no_options + 1):
                        input_ok = True
                    else:
                        self.display_divider()
                        self.display_text("Error: Please enter a number between 0 and "+str(self.no_options)+".")
                        self.display_divider()
                except:
                    self.display_divider()
                    self.display_text("Error: Please enter a number.")
                    self.display_divider()
            self.no_options = 0
            if selection == 0:
                self.level = 4
            elif selection == 1:
                self.level = 14
            elif selection == 2:
                self.level = 15
            elif selection == 3:
                self.level = 16
            elif selection == 4:
                self.level = 17
        elif self.level == 10:
            self.display_divider()
            self.display_text("LOCATIONS")
            self.display_divider()
            self.display_numbered("Show Locations")
            self.display_numbered("Add Locations")
            self.display_numbered("Edit Locations")
            self.display_numbered("Remove Locations")
            self.display_text("0: Edit Menu")
            self.display_divider()
            input_ok = False
            while not input_ok:
                self.display_divider()
                selection = self.display_input("Make a selection: ")
                self.display_divider()
                try:
                    selection = int(selection)
                    if selection in range(0, self.no_options + 1):
                        input_ok = True
                    else:
                        self.display_divider()
                        self.display_text("Error: Please enter a number between 0 and "+str(self.no_options)+".")
                        self.display_divider()
                except:
                    self.display_divider()
                    self.display_text("Error: Please enter a number.")
                    self.display_divider()
            self.no_options = 0
            if selection == 0:
                self.level = 4
            elif selection == 1:
                self.level = 18
            elif selection == 2:
                self.level = 19
            elif selection == 3:
                self.level = 20
            elif selection == 4:
                self.level = 21
        elif self.level == 11:
            self.display_divider()
            self.display_text("RULES")
            self.display_divider()
            self.display_numbered("Show Rules")
            self.display_numbered("Add Rules")
            self.display_numbered("Edit Rules")
            self.display_numbered("Remove Rules")
            self.display_text("0: Edit Menu")
            self.display_divider()
            input_ok = False
            while not input_ok:
                self.display_divider()
                selection = self.display_input("Make a selection: ")
                self.display_divider()
                try:
                    selection = int(selection)
                    if selection in range(0, self.no_options + 1):
                        input_ok = True
                    else:
                        self.display_divider()
                        self.display_text("Error: Please enter a number between 0 and "+str(self.no_options)+".")
                        self.display_divider()
                except:
                    self.display_divider()
                    self.display_text("Error: Please enter a number.")
                    self.display_divider()
            self.no_options = 0
            if selection == 0:
                self.level = 4
            elif selection == 1:
                self.level = 22
            elif selection == 2:
                self.level = 23
            elif selection == 3:
                self.level = 24
            elif selection == 4:
                self.level = 25
        elif self.level == 12:
            self.display_divider()
            self.display_text("EDIT INFORMATION")
            self.display_divider()
            self.display_text("Under Construction")
            self.display_divider()
            self.display_input("Press any key to return to the puzzle settings menu.")
            self.display_divider()
            self.level = 8
        elif self.level == 13:
            self.display_divider()
            self.display_text("EDIT SOLUTION FORMAT")
            self.display_divider()
            self.display_text("Under Construction")
            self.display_divider()
            self.display_input("Press any key to return to the puzzle settings menu.")
            self.display_divider()
            self.level = 8
        elif self.level == 14:
            self.display_divider()
            self.display_text("CURRENT PARAMETERS")
            self.display_divider()
            self.display_text("Under Construction")
            self.display_divider()
            self.display_input("Press any key to return to the puzzle settings menu.")
            self.display_divider()
            self.level = 9
        elif self.level == 15:
            self.display_divider()
            self.display_text("ADD PARAMETERS")
            self.display_divider()
            self.display_text("Under Construction")
            self.display_divider()
            self.display_input("Press any key to return to the puzzle settings menu.")
            self.display_divider()
            self.level = 9
        elif self.level == 16:
            self.display_divider()
            self.display_text("EDIT PARAMETERS")
            self.display_divider()
            self.display_text("Under Construction")
            self.display_divider()
            self.display_input("Press any key to return to the puzzle settings menu.")
            self.display_divider()
            self.level = 9
        elif self.level == 17:
            self.display_divider()
            self.display_text("REMOVE PARAMETERS")
            self.display_divider()
            self.display_text("Under Construction")
            self.display_divider()
            self.display_input("Press any key to return to the puzzle settings menu.")
            self.display_divider()
            self.level = 9
        elif self.level == 18:
            self.display_divider()
            self.display_text("CURRENT LOCATIONS")
            self.display_divider()
            self.display_text("Under Construction")
            self.display_divider()
            self.display_input("Press any key to return to the puzzle settings menu.")
            self.display_divider()
            self.level = 10
        elif self.level == 19:
            self.display_divider()
            self.display_text("ADD LOCATIONS")
            self.display_divider()
            self.display_text("Under Construction")
            self.display_divider()
            self.display_input("Press any key to return to the puzzle settings menu.")
            self.display_divider()
            self.level = 10
        elif self.level == 20:
            self.display_divider()
            self.display_text("EDIT LOCATIONS")
            self.display_divider()
            self.display_text("Under Construction")
            self.display_divider()
            self.display_input("Press any key to return to the puzzle settings menu.")
            self.display_divider()
            self.level = 10
        elif self.level == 21:
            self.display_divider()
            self.display_text("REMOVE LOCATIONS")
            self.display_divider()
            self.display_text("Under Construction")
            self.display_divider()
            self.display_input("Press any key to return to the puzzle settings menu.")
            self.display_divider()
            self.level = 10
        elif self.level == 22:
            self.display_divider()
            self.display_text("CURRENT RULES")
            self.display_divider()
            self.display_text("Under Construction")
            self.display_divider()
            self.display_input("Press any key to return to the puzzle settings menu.")
            self.display_divider()
            self.level = 11
        elif self.level == 23:
            self.display_divider()
            self.display_text("ADD RULES")
            self.display_divider()
            self.display_text("Under Construction")
            self.display_divider()
            self.display_input("Press any key to return to the puzzle settings menu.")
            self.display_divider()
            self.level = 11
        elif self.level == 24:
            self.display_divider()
            self.display_text("EDIT RULES")
            self.display_divider()
            self.display_text("Under Construction")
            self.display_divider()
            self.display_input("Press any key to return to the puzzle settings menu.")
            self.display_divider()
            self.level = 11
        elif self.level == 25:
            self.display_divider()
            self.display_text("REMOVE RULES")
            self.display_divider()
            self.display_text("Under Construction")
            self.display_divider()
            self.display_input("Press any key to return to the puzzle settings menu.")
            self.display_divider()
            self.level = 11
    def display_status(self):
        if self.parent.puzzle.initialised:
            output = "Loc: " + str(len(self.parent.puzzle.locations)) + " Para: " + str(self.parent.puzzle.no_of_properties) + " Comb: " + str(self.parent.puzzle.no_of_combinations) + " Rules: " + str(len(self.parent.puzzle.rules))
            self.display_text(output)
        else:
            self.display_text("Puzzle Uninitialised")
class UI_GUI():
    def __init__(self, parent):
        pass

class Main():
    def __init__(self, ui=None):
        self.puzzle = Grid()
        self.ui = ui
        self.width = 75
        if self.ui != None:
            self.display_ui()
    def display_ui(self):
        if self.ui == "text":
            run = UI_Text(self, self.width)
        elif self.ui == "gui":
            run = UI_GUI(self)
        elif self.ui == "test":
            self.test_run()
        elif self.ui == None:
            print("No UI set, using text.")
            run = UI_Text(self, self.width)
        else:
            print("Invalid UI, using text.")
            run = UI_Text(self, self.width)
    def save_puzzle(self, filename):
        try:
            with open(filename, "wb") as output:
                pickle.dump(self.puzzle, output, pickle.HIGHEST_PROTOCOL)
        except:
            print("Unable to save file")
    def load_puzzle(self, filename):
        try:
            with open(filename, "rb") as input:
                self.puzzle = pickle.load(input)
        except OSError:
            print("Unable to open file")
    def solve(self):
        self.puzzle.solve()
    def test_run(self):
        self.puzzle = Grid()
        self.puzzle.change_intro("There are five houses in five different colours.\nIn each house lives a person with a different nationality.\nThe five owners drink a different beverage, smoke different brands of cigar, and keep different pets.")
        self.puzzle.change_output_text("The {4} lives in house number {0}, which is painted {1}. He keeps {2}, drinks {3}, and smokes {5} cigars.")
        self.puzzle.add_locations(["1", "2", "3", "4", "5"])
        self.puzzle.add_properties(["Red", "Green", "Yellow", "Blue", "White"])
        self.puzzle.add_properties(["Dogs", "Cats", "Fish", "Birds", "Horses"])
        self.puzzle.add_properties(["Tea", "Water", "Beer", "Milk", "Coffee"])
        self.puzzle.add_properties(["Brit", "Swede", "Dane", "Norwegian", "German"])
        self.puzzle.add_properties(["Pall Mall", "Dunhill", "Blend", "Bluemaster", "Prince"])
        self.puzzle.build_grid()
        self.puzzle.add_rule("Brit", "Has", "Red","The {0} lives in the {2} house")
        self.puzzle.add_rule("Swede", "Has", "Dogs","The {0} keeps {2} as pets")
        self.puzzle.add_rule("Dane", "Has", "Tea", "The {0} drinks {2}")
        self.puzzle.add_rule("Green", "Left", "White", "The {0} house is on the {1} of the {2} house")
        self.puzzle.add_rule("Green", "Has", "Coffee", "The {0} homeowner drinks {2}")
        self.puzzle.add_rule("Pall Mall", "Has", "Birds", "The person who smokes {0} rears {2}")
        self.puzzle.add_rule("Yellow", "Has", "Dunhill", "The owner of the {0} house smokes {2}")
        self.puzzle.add_rule("Milk", "At", "3", "The man living in the center house drinks {0}")
        self.puzzle.add_rule("Norwegian", "At", "1", "The {0} lives in the first house")
        self.puzzle.add_rule("Blend", "Neighbor", "Cats", "The man who smokes {0} lives next to the one who keeps {2}")
        self.puzzle.add_rule("Dunhill", "Neighbor", "Horses", "The man who keeps the {2} lives next to the man who smokes {0}")
        self.puzzle.add_rule("Bluemaster", "Has", "Beer", "The owner who smokes {0} drinks {2}")
        self.puzzle.add_rule("German", "Has", "Prince", "The {0} smokes {2}")
        self.puzzle.add_rule("Norwegian", "Neighbor", "Blue", "The {0} lives next to the {2} house")
        self.puzzle.add_rule("Blend", "Neighbor", "Water", "The man who smokes {0} has a neighbor who drinks {2}")
        self.puzzle.solve()
        print(self.puzzle)
        self.save_puzzle("puzzle_1.pkl")
        
a = Main("text")