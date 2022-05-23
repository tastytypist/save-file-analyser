class StringFinder:
    """Represents the string finder used in the save file analyser.

    Class StringFinder implements the Boyer-Moore Algorithm.

    Reference: https://doi.org/10.1145/359842.359859
    """
    def __init__(self, string, target):
        self.index = 0
        self.last = [-1 for _ in range(26)]
        self.string = string
        self.target = target

    def preprocess_string(self):
        for i in range(len(self.string)):
            self.last[ord(self.string[i].upper()) - 65] = i

    def find_string(self):
        self.preprocess_string()
        string_length = len(self.string)
        target_length = len(self.target)
        i = string_length - 1
        j = string_length - 1

        while i <= target_length - 1:
            if self.string[j] == self.target[i]:
                if j == 0:
                    self.index = i
                    return
                else:
                    i -= 1
                    j -= 1
            else:
                if 0 <= ord(self.target[i].upper()) - 65 <= 25:
                    last_occur = self.last[ord(self.target[i].upper()) - 65]
                    i = i + string_length - min(j, last_occur + 1)
                else:
                    i = i + string_length - j
                j = string_length - 1


if __name__ == "__main__":
    finder = StringFinder("hello", "well, hello there!")
    finder.find_string()
    print(finder.index)
