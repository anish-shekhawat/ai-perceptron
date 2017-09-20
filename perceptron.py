#!/usr/bin/env python

import sys
import os.path
import re
import random
import math

ground_function = ""
n = 5


def validate_ground_func_file():

    global ground_function

    with open(sys.argv[3], 'r') as file:
        line = file.readline()
        line = line.strip()

        if line == 'NBF':
            line = file.readline()
            pattern = re.compile("([+|-]\d+\s)([AND|OR]+\s[+|-]\d+\s)+")

            if not pattern.match(line):
                print >> sys.stderr, "NOT PARSEABLE"
                exit(1)

            ground_function = "NBF"

        elif line == 'TF':
            line = file.readline()
            pattern = re.compile("[+|-]\d+")

            if not pattern.match(line):
                print >> sys.stderr, "NOT PARSEABLE"
                exit(1)

            line = file.readline()
            pattern = re.compile("([+|-]\d+([ \t]+[+|-]\d+)*)")

            if not pattern.match(line):
                print >> sys.stderr, "NOT PARSEABLE"
                exit(1)

            ground_function = "TF"

        else:
            print >> sys.stderr, "NOT PARSEABLE"


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

    validate_ground_func_file()

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


def bool_dist_samples(num_samples):

    sample_matrix = list()
    vector = list()
    for i in range(num_samples):
        del vector[:]
        for j in range(n):
            vector.append(random.randint(0, 1))
        sample_matrix.append(vector)

    return sample_matrix


def sphere_dist_samples(num_samples):

    sample_matrix = list()
    vector = list()
    for i in range(num_samples):
        del vector[:]
        for j in range(n):
            vector.append(random.random())
        sample_matrix.append(vector)

    return sample_matrix


def get_samples(num_samples):

    if ground_function == "NBF" or sys.argv[4] == "bool":
        sample_vector = bool_dist_samples(num_samples)
    else:
        sample_vector = sphere_dist_samples(num_samples)

    return sample_vector


def nested_bool_func(vector):
    with open(sys.argv[3], 'r') as file:
        lines = file.readlines()

    func_list = lines[1].strip().split()

    value = (vector[int(func_list[0]) - 1]
             if int(func_list[0]) > 0
             else abs(vector[abs(int(func_list[0]))-1] - 1))

    for i in range(1, len(func_list), 2):

        if func_list[i] == 'OR':
            value = value or (vector[int(func_list[i + 1]) - 1] if
                              int(func_list[i + 1]) > 0 else
                              abs(vector[abs(int(func_list[i + 1])) - 1] - 1))
        else:
            value = value and (vector[int(func_list[i+1]) - 1] if
                               int(func_list[i+1]) > 0 else
                               abs(vector[abs(int(func_list[i+1])) - 1] - 1))
    return value


def threshold_func(vector):
    print vector
    with open(sys.argv[3], 'r') as file:
        lines = file.readlines()

    coefficient_list = lines[2].strip().split()
    coefficient_list = [int(item) for item in coefficient_list]
    print coefficient_list

    value = 0
    for i in range(len(vector)):
        value = value + (coefficient_list[i] * vector[i])

    if value < int(lines[1]):
        return 0
    else:
        return 1


def main():
    # Check if all arguments are present
    if len(sys.argv) < 8:
        print >> sys.stderr, "Some arguments are missing!",
        print >> sys.stderr, "Please make sure the command is in format:"
        print >> sys.stderr, "\"python perceptron activation training_alg",
        print >> sys.stderr, "ground_file dist num_train num_test epsilon\""
        exit(1)

    validate()

    x_vector = get_samples(int(sys.argv[5]))

    threshold_func(x_vector[0])


if __name__ == '__main__':
    main()
