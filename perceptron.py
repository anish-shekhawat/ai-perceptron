#!/usr/bin/env python

import sys
import os.path
import re
import random
import math

ground_function = ""

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


def calculate_input_len():

    with open(sys.argv[3], 'r') as file:
            lines = file.readlines()

    if ground_function == "NBF":
        lines[1] = lines[1].strip().split()
        length = max([int(item) for item in lines[1][::2]])

    else:
        lines[2] = lines[2].strip().split()
        length = len([int(item) for item in lines[2]])

    return length


def bool_dist_samples(num_samples, n):

    sample_matrix = list()
    for i in range(num_samples):
        vector = []
        for j in range(n):
            vector.append(random.randint(0, 1))
        sample_matrix.append(vector)

    return sample_matrix


def sphere_dist_samples(num_samples, n):

    sample_matrix = list()
    for i in range(num_samples):
        vector = []
        for j in range(n):
            vector.append(random.random())
        sample_matrix.append(vector)

    return sample_matrix


def get_samples(num_samples, n):

    if ground_function == "NBF" or sys.argv[4] == "bool":
        sample_vector = bool_dist_samples(num_samples, n)
    else:
        sample_vector = sphere_dist_samples(num_samples, n)

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
    with open(sys.argv[3], 'r') as file:
        lines = file.readlines()

    coefficient_list = lines[2].strip().split()
    coefficient_list = [int(item) for item in coefficient_list]

    value = 0
    for i in range(len(vector)):
        value = value + (coefficient_list[i] * vector[i])

    if value < int(lines[1]):
        return 0
    else:
        return 1


def threshold_activation(dot_product, theta):
    if dot_product < theta:
        return 0
    else:
        return 1


def tanh_activation(dot_product, theta):
    return (0.5 + (0.5 * math.tanh((dot_product - theta) / 2)))


def relu_activation(dot_product, theta):
    return max(0, dot_product - theta)


def perceptron_update_func(vector, weights, theta_alpha, test):
    if test == 1:
        weights = [x1 - x2 for (x1, x2) in zip(weights, vector)]
        # Update theta
        theta_alpha[0] += 1
    else:
        weights = [x1 + x2 for (x1, x2) in zip(weights, vector)]
        theta_alpha[0] -= 1

    return weights


def winnow_update_func(vector, weights, theta_alpha, test):
    if test == 1:
        for i in range(vector):
            weights[i] *= (1 / (theta_alpha[1] ** vector[i]))
    else:
        for i in range(vector):
            weights[i] *= (theta_alpha[1] ** vector[i])

    return weights


activation_func_map = {
    'threshold': threshold_activation,
    'tanh': tanh_activation,
    'relu': relu_activation
}
ground_function_map = {
    'NBF': nested_bool_func,
    'TF': threshold_func
}


def train(vectors):
    global ground_function
    global activation_func_map
    global ground_function_map

    weights = random.sample(range(1, 101), len(vectors[0]))
    theta = 10
    alpha = 1

    theta_alpha = [theta, alpha]
    print "Reference: " + str(theta_alpha)

    update_function_map = {
        'perceptron': perceptron_update_func,
        'winnow': winnow_update_func
    }

    for i in range(len(vectors)):
        dot_product = 0
        for j in range(len(vectors[i])):
            dot_product += weights[j] * vectors[i][j]

        prediction = activation_func_map[sys.argv[1]](dot_product, theta)
        actual = ground_function_map[ground_function](vectors[i])

        output = ",".join(map(str, vectors[i])) + ":"
        output += str(prediction) + ":" + str(actual)

        if prediction == actual:
            output += " no update"

        elif prediction > actual:
            weights = update_function_map[sys.argv[2]](
                vectors[i], weights, theta_alpha, 1)
            theta = theta_alpha[0]
            output += " update : " + str(theta) + " : " + str(alpha)

        else:
            weights = update_function_map[sys.argv[2]](
                vectors[i], weights, theta_alpha, 0)
            theta = theta_alpha[0]
            output += " update : " + str(theta) + " : " + str(alpha)

        print output

    return weights, theta


def test(vectors, weights, theta):
    global ground_function
    global activation_func_map
    global ground_function_map

    sum_error = 0
    epsilon = 0.2

    for i in range(len(vectors)):
        dot_product = 0
        for j in range(len(vectors[i])):
            dot_product += weights[j] * vectors[i][j]

        prediction = activation_func_map[sys.argv[1]](dot_product, theta)
        actual = ground_function_map[ground_function](vectors[i])

        output = ",".join(map(str, vectors[i])) + ":"
        output += str(prediction) + ":" + str(actual) + ":"
        output += str(abs(prediction - actual))

        print output

        if abs(prediction - actual) > 0:
            sum_error += 1

    average_error = sum_error / float(len(vectors))
    print "Average Error: " + str(average_error)
    print "Epsilon: " + str(epsilon)

    if average_error > epsilon:
        print "TRAINING FAILED"
    else:
        print "TRAINING SUCCEEDED"


def main():
    # Check if all arguments are present
    if len(sys.argv) < 8:
        print >> sys.stderr, "Some arguments are missing!",
        print >> sys.stderr, "Please make sure the command is in format:"
        print >> sys.stderr, "\"python perceptron activation training_alg",
        print >> sys.stderr, "ground_file dist num_train num_test epsilon\""
        exit(1)

    validate()
    n = calculate_input_len()
    training_vectors = get_samples(int(sys.argv[5]), n)
    weights, theta = train(training_vectors)

    testing_vectors = get_samples(int(sys.argv[6]), n)
    test(testing_vectors, weights, theta)


if __name__ == '__main__':
    main()
