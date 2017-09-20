#!/usr/bin/env python

import sys
import os.path
import re
import math


def validate():

    # Check activation function parameter
    if sys.argv[1] not in ['threshold', 'tanh', 'relu']:
        print >> sys.stderr, "Incorrect activation function!"
        print >> sys.stderr, "Use either threshold, tanh or relu"
        exit(1)

    # Check training_algo parameter
    if sys.argv[2] not in ['perceptron', 'winnow']:
        print >> sys.stderr, "Incorrect training algo!"
        print >> sys.stderr, "Use either perceptron or winnow"
        exit(1)

    # Check ground function parameter
    if not os.path.isfile(sys.argv[3]):
        print >> sys.stderr, sys.argv[3] + " :file does not exist!"
        exit(1)

    # Check distribution parameter
    if sys.argv[4] not in ['bool', 'sphere']:
        print >> sys.stderr, "Incorrect distribution parameter!"
        print >> sys.stderr, "Use either bool or sphere"
        exit(1)

    # Check num_train, num_test and epsilon parameters
    if not (sys.argv[5].replace('.', '', 1).isdigit() and
            sys.argv[6].replace('.', '', 1).isdigit() and
            sys.argv[7].replace('.', '', 1).isdigit()):
        print >> sys.stderr, "Incorrect num_train, num_test or epsilon!"
        print >> sys.stderr, "Use integers or floats"
        exit(1)


def main():
    # Check if all arguments are present
    if len(sys.argv) < 8:
        print >> sys.stderr, "Some arguments are missing!",
        print >> sys.stderr, "Please make sure the command is in format:"
        print >> sys.stderr, "\"python perceptron activation training_alg",
        print >> sys.stderr, "ground_file dist num_train num_test epsilon\""
        exit(1)

    validate()
    #parse()


if __name__ == '__main__':
    main()
