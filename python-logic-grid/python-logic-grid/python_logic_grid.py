import pickle

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
                    print("Invalid properties:",p1,r,p2)
            else:
                if search(p1, self.properties) and search(p2, self.properties) and search(r, self.RELATIONS):
                    self.rules.append(Rule(p1, r, p2, self, text))
                else:
                    print("Invalid properties:",p1,r,p2)
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

class Main():
    def __init__(self):
        self.puzzle = Grid()
    def __str__(self):
        return str(self.puzzle)
    def save_puzzle(self, filename):
        output = open(filename, "wb")
        pickle.dump(self.puzzle, output, pickle.HIGHEST_PROTOCOL)
        output.close()
    def load_puzzle(self, filename):
        input = open(filename, "rb")
        self.puzzle = pickle.load(input)
        input.close()
    def solve(self):
        self.puzzle.solve()
    def test_run(self):
        self.puzzle = Grid()
        self.puzzle.change_intro("There are five houses in five different colours.\nIn each house lives a person with a different nationality.\nThe five owners drink a different beverage, smoke different brands of cigar, and keep different pets.")
        self.puzzle.change_output_text("The {4} lives in house number {0}, which is painted {1}. He keep {2}. drinks {3}, and smokes {5} cigars.")
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
        self.save_puzzle("puzzle_1.pk1")

a = Main()
#a.test_run()
a.load_puzzle("puzzle_1.pk1")
a.solve()
print(a)