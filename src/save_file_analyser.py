import argparse

import save_analyser

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="your game save file", type=str)

    save_file = parser.parse_args()
    analyser = save_analyser.SaveAnalyser(save_file.source)
    analyser.analyse()
