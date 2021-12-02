from avltree import AVLT
import random


def main():
    tree = AVLT()

    for i in range(7, 153, 9):
        tree.insert(i)
        tree.display()


if __name__ == "__main__":
    main()
