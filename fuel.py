"""
Doomsday Fuel
=============

Making fuel for the LAMBCHOP's reactor core is a tricky process because of the exotic matter involved. It starts as raw ore, then during processing, begins randomly changing between forms, eventually reaching a stable form. There may be multiple stable forms that a sample could ultimately reach, not all of which are useful as fuel.

Commander Lambda has tasked you to help the scientists increase fuel creation efficiency by predicting the end state of a given ore sample. You have carefully studied the different structures that the ore can take and which transitions it undergoes. It appears that, while random, the probability of each structure transforming is fixed. That is, each time the ore is in 1 state, it has the same probabilities of entering the next state (which might be the same state).  You have recorded the observed transitions in a matrix. The others in the lab have hypothesized more exotic forms that the ore can become, but you haven't seen all of them.

Write a function solution(m) that takes an array of array of nonnegative ints representing how many times that state has gone to the next state and return an array of ints for each terminal state giving the exact probabilities of each terminal state, represented as the numerator for each state, then the denominator for all of them at the end and in simplest form. The matrix is at most 10 by 10. It is guaranteed that no matter which state the ore is in, there is a path from that state to a terminal state. That is, the processing will always eventually end in a stable state. The ore starts in state 0. The denominator will fit within a signed 32-bit integer during the calculation, as long as the fraction is simplified regularly.

For example, consider the matrix m:
[
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]
So, we can consider different paths to terminal states, such as:
s0 -> s1 -> s3
s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
s0 -> s1 -> s0 -> s5
Tracing the probabilities of each, we find that
s2 has probability 0
s3 has probability 3/14
s4 has probability 1/7
s5 has probability 9/14
So, putting that together, and making a common denominator, gives an answer in the form of
[s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is
[0, 3, 2, 9, 14].

Languages
=========

To provide a Java solution, edit Solution.java
To provide a Python solution, edit solution.py

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Java cases --
Input:
Solution.solution({{0, 2, 1, 0, 0}, {0, 0, 0, 3, 4}, {
                  0, 0, 0, 0, 0}, {0, 0, 0, 0,0}, {0, 0, 0, 0, 0}})
Output:
    [7, 6, 8, 21]

Input:
Solution.solution({{0, 1, 0, 0, 0, 1}, {4, 0, 0, 3, 2, 0}, {0, 0, 0, 0, 0, 0}, {
                  0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}})
Output:
    [0, 3, 2, 9, 14]

-- Python cases --
Input:
solution.solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [
                  0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]])
Output:
    [7, 6, 8, 21]

Input:
solution.solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [
                  0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
Output:
    [0, 3, 2, 9, 14]

"""

# simply implementing an absorbing markov chain

from fractions import Fraction
import numpy as np


def solution(matrix):

    # simple edge case
    if len(matrix) == 1:
        return [1, 1]

    # since this is done often
    def matrix_maker(d, r):
        made_matrix = []
        for i in range(d):
            made_array = []
            for j in range(r):
                made_array.append(0)
            made_matrix.append(made_array)
        return made_matrix

    # stores index of terminal and nonterminal/denom arrays in matrix, aids to rearange matrix
    order_array = []
    denoms_order = []
    terminals_order = []

    # stores which denom belongs to which matrix array
    denoms_dict = {}

    # fills the above arrays
    for i in range(len(matrix)):
        total = 0
        for number in matrix[i]:
            total += number
        if total > 0:
            denoms_order.append(i)
        else:
            terminals_order.append(i)
        denoms_dict[i] = total

    # edge case of all arrays being terminal states
    if len(denoms_order) == 0:
        return [1]*len(terminals_order) + [len(terminals_order)]

    # just cosmetic, to have the matrix in standard form, although top left is never used
    for i in terminals_order:
        matrix[i][i] = 1

    # this will be the order in which the matrix will be rearanged
    order_array = terminals_order + denoms_order

    # rearanges the matrix
    new_matrix = matrix_maker(len(order_array), len(order_array))
    i = 0

    # essentially gets the right keys in the order of the order_array and uses that to access the right values in the right order
    for array_n in order_array:
        j = 0
        for value_n in order_array:
            if denoms_dict[array_n] != 0:
                new_matrix[i][j] = float(
                    matrix[array_n][value_n]) / float(denoms_dict[array_n])
            else:
                new_matrix[i][j] = float(matrix[array_n][value_n]) / 1.0
            j += 1
        i += 1

    # just overwrites the matrix
    matrix = new_matrix

    # creates the empty matrices used for the mathematics
    R_matrix = matrix_maker(len(denoms_order), len(terminals_order))
    Q_matrix = matrix_maker(len(denoms_order), len(denoms_order))

    # next section calculates F*R "((I - Q)**-1)R"

    # preparation
    starting_point = len(order_array) - len(denoms_order)
    for i in range(len(R_matrix)):
        R_matrix[i] = matrix[starting_point + i][:len(terminals_order)]

    for i in range(len(Q_matrix)):
        Q_matrix[i] = matrix[starting_point +
                             i][starting_point:len(order_array)]

    # F*R
    F_R_matrix = np.matmul(np.linalg.inv(
        np.array(np.subtract(np.identity(len(Q_matrix)), Q_matrix))), R_matrix)

    # creates the probability array, turns floats into their Fractions
    prob_array = [1]*len(terminals_order)
    lcm_array = []
    for i in range(len(F_R_matrix[0])):
        prob_array[i] = Fraction(F_R_matrix[0][i]).limit_denominator()
        if prob_array[i] != 0:
            lcm_array.append(
                Fraction(F_R_matrix[0][i]).limit_denominator().denominator)

    # calculates the lowest common multiple, or lowest common denominator
    prob_array.append(np.lcm.reduce(np.array(lcm_array)))

    # transforms prob_array into the right values to return the answer
    return_array = []
    for i in range(len(prob_array)-1):
        if prob_array[-1]/prob_array[i].denominator > 1:
            prob_array[i] = prob_array[i].numerator * \
                Fraction(prob_array[-1]/prob_array[i].denominator)
        return_array.append(int(prob_array[i].numerator))
    return_array.append(int(prob_array[-1]))

    # returns answer
    return return_array


print(solution([[0, 0], [0, 0]]))
print(solution([[0, 7, 0, 17, 0, 1, 0, 5, 0, 2],
                [0, 0, 29, 0, 28, 0, 3, 0, 16, 0],
                [0, 3, 0, 0, 0, 1, 0, 0, 0, 0],
                [48, 0, 3, 0, 0, 0, 17, 0, 0, 0],
                [0, 6, 0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]))
print(solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [
    0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]))
print(solution([
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [1, 0, 8, 1],
    [1, 1, 4, 4]

]))
print(solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [
      0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]))
print(solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [
      0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]))
