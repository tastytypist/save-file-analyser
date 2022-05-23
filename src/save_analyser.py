import str_find


class SaveAnalyser:
    def __init__(self, file):
        self.farm_types = ["Standard", "Riverland", "Forest", "Hill-top",
                           "Wilderness", "Four Corners", "Beach"]
        self.stardrop_id = ["CF_Fair", "CF_Fish", "CF_Mines", "CF_Sewer",
                            "CF_Spouse", "CF_Statue", "museumComplete"]

        self.file = file
        self.data = ""
        self.finder = None
        self.name = ""      # tag: name
        self.farm = ""      # tag: farmName
        self.farm_type = 0  # tag: whichFarm
        self.time = 0       # tag: millisecondsPlayed
        self.version = ""   # tag: gameVersion
        self.money = 0      # tag: totalMoneyEarned
        self.spouse = ""    # tag: spouse
        self.stardrops = 0  # string: CF_Fair, CF_Fish, CF_Mines, CF_Sewer, CF_Spouse, CF_Statue, museumComplete
        self.kids = []      # type: "Child"

    def analyse(self):
        self.import_save_file()

        self.name = self.find("name")
        self.farm = self.find("farmName")
        self.farm_type = int(self.find("whichFarm"))
        self.time = int(self.find("millisecondsPlayed"))
        self.version = self.find("gameVersion")
        self.money = int(self.find("totalMoneyEarned"))
        self.spouse = self.find("spouse")

        for ids in self.stardrop_id:
            if self.find(ids):
                self.stardrops += 1

        child = self.find('type="Child"', child=True)
        last_found = 0
        while child and len(self.kids) < 2:
            self.kids.append(child)
            last_found += self.finder.index
            child = self.find('type="Child"', child=True, data=self.data[last_found + 12:])

        self.show()

    def import_save_file(self):
        save_file = open(f"../test/{self.file}", "r")
        self.data = save_file.readlines()
        self.data = self.data[0]
        save_file.close()

    def find(self, attr, child=False, data=None):
        if not data:
            data = self.data
        self.finder = str_find.StringFinder(attr, data)
        self.finder.find_string()

        if self.finder.index == -1:
            return None

        character = data[self.finder.index]
        start_index = self.finder.index
        stop_index = self.finder.index

        if not child:
            while character != "<":
                if character == ">":
                    start_index = stop_index + 1
                stop_index += 1
                character = data[stop_index]
        else:
            while character != "/":
                if character == ">":
                    start_index = stop_index + 1
                stop_index += 1
                character = data[stop_index]
            stop_index -= 1

        return data[start_index:stop_index]

    def show(self):
        print(f"Farmer's name: {self.name}")
        print(f"Farm's name: {self.farm} Farm")
        print(f"Farm Type: {self.farm_types[self.farm_type]}")
        print(f"Time Played: {int(self.time // 36e5)} hours {int((self.time % 36e5) // 6e4)} minutes")
        print(f"Game Version: {self.version}")
        print(f"{self.name} has earned {self.money}g.")
        print(f"{self.name} is married to {self.spouse}.")

        print(f"{self.name} has {len(self.kids)} kid(s)", end="")
        if len(self.kids) > 0:
            print(f" named ", end="")
            for i in range(len(self.kids)):
                print(f"{self.kids[i]}", end="")
                if len(self.kids) == 2 and i == 0:
                    print(f" and ", end="")
                    continue
        print(".")

        print(f"{self.name} has collected {self.stardrops} Stardrop(s).")


if __name__ == "__main__":
    analyser = SaveAnalyser("Clancy_241495642")
    analyser.analyse()
