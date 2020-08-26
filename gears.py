"""
Challenge

As Commander Lambda's personal assistant, you've been assigned the task of configuring the LAMBCHOP doomsday device's axial orientation gears. It should be pretty simple - just add gears to create the appropriate rotation ratio. But the problem is, due to the layout of the LAMBCHOP and the complicated system of beams and pipes supporting it, the pegs that will support the gears are fixed in place.

The LAMBCHOP's engineers have given you lists identifying the placement of groups of pegs along various support beams. You need to place a gear on each peg (otherwise the gears will collide with unoccupied pegs). The engineers have plenty of gears in all different sizes stocked up, so you can choose gears of any size, from a radius of 1 on up. Your goal is to build a system where the last gear rotates at twice the rate (in revolutions per minute, or rpm) of the first gear, no matter the direction. Each gear (except the last) touches and turns the gear on the next peg to the right.

Given a list of distinct positive integers named pegs representing the location of each peg along the support beam, write a function answer(pegs) which, if there is a solution, returns a list of two positive integers a and b representing the numerator and denominator of the first gear's radius in its simplest form in order to achieve the goal above, such that radius = a/b. The ratio a/b should be greater than or equal to 1. Not all support configurations will necessarily be capable of creating the proper rotation ratio, so if the task is impossible, the function answer(pegs) should return the list [-1, -1].

For example, if the pegs are placed at [4, 30, 50], then the first gear could have a radius of 12, the second gear could have a radius of 14, and the last one a radius of 6. Thus, the last gear would rotate twice as fast as the first one. In this case, pegs would be [4, 30, 50] and answer(pegs) should return [12, 1].

The list pegs will be given sorted in ascending order and will contain at least 2 and no more than 20 distinct positive integers, all between 1 and 10000 inclusive.

Test cases

Inputs:
(int list) pegs = [4, 30, 50]
Output:
(int list) [12, 1]

Inputs:
(int list) pegs = [4, 17, 50]
Output:
(int list) [-1, -1]
"""

# only one factor matters: is final gear half the radius of the first gear
# to test this, optimal is starting at cog left of smallest space, going left and right for finding margins.
# if upper margin is larger than maximum required or lower margin is smaller then minimum required than it cant be done
# otherwise assume new margin and work from this gear gap
# value being min or max alternates every move left or right, see line 55


def solution(pegs):
    differences_array = []
    min_difference = 10000
    min_difference_i = 0

    # create list of differences
    for i in range(len(pegs)-1):
        difference = pegs[i+1]-pegs[i]
        if difference < min_difference:
            min_difference = difference
            min_difference_i = i
        differences_array.append(difference)

    test_case = min_difference_i

    def min_option(test_case, differences_array):
        # check for lowest radius at first of 2 pegs with lowest difference:

        # set up initial variables
        current_difference = 1

        test_case_min_or_max = -1
        current_min_or_max = -1  # multiply by -1 to alternate between postive and negative
        i = test_case - 1
        # go down first
        while i >= 0:
            current_difference = differences_array[i] - current_difference
            if current_difference < 1:
                if test_case_min_or_max == current_min_or_max:
                    return [-1, -1]
                else:
                    return min_option(
                        i, differences_array)

            i -= 1
            current_min_or_max *= -1
        possible_beginning_radius = current_difference

        # reset variables
        current_difference = 1

        current_min_or_max = -1  # multiply by -1 to alternate between postive and negative
        i = test_case
        # go up next
        while i < len(differences_array):
            current_difference = differences_array[i] - current_difference
            if current_difference < 1:
                if test_case_min_or_max == current_min_or_max:
                    return [-1, -1]
                else:
                    return min_option(
                        i, differences_array)

            i += 1
            current_min_or_max *= -1
        possible_ending_radius = current_difference

        return [possible_beginning_radius, possible_ending_radius]

    def check_possible_combination(beginning_radius, pegs):
        radius = beginning_radius
        for i in range(len(pegs)-1):
            radius = pegs[i+1] - (pegs[i] + radius)
            if radius < 1:
                return False
        return True

    # verify if answer is valid
    possible_combination = min_option(test_case, differences_array)
    if possible_combination == [-1, -1]:
        return [-1, -1]

    else:
        if len(pegs) % 2 != 0:
            first_radius = (
                possible_combination[0] - possible_combination[1])*2
            if check_possible_combination(first_radius, pegs):
                return [int(first_radius), 1]

        else:
            total = possible_combination[0] + possible_combination[1]
            first_radius = (total/3)*2
            if check_possible_combination(first_radius, pegs):
                if total % 3 == 0:
                    return [int(first_radius), 1]
                else:
                    return [int(2 * total), 3]

    return [-1, -1]


# pegs = [200, 830, 900, 1600, 2230, 2500,
    # 3000, 3600, 4000, 4050, 4150, 5000, 5790]
# pegs = [200, 620, 810, 900, 1400, 1850, 2000]
# pegs = [200, 610, 800, 910, 1400, 2000]
pegs = [4, 30, 50]k

final_verdict = solution(pegs)
print("final verdict")
print(final_verdict)
