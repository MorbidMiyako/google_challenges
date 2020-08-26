"""
Bomb, Baby!
===========

You're so close to destroying the LAMBCHOP doomsday device you can taste it! But in order to do so, you need to deploy special self-replicating bombs designed for you by the brightest scientists on Bunny Planet. There are two types: Mach bombs (M) and Facula bombs (F). The bombs, once released into the LAMBCHOP's inner workings, will automatically deploy to all the strategic points you've identified and destroy them at the same time. 

But there's a few catches. First, the bombs self-replicate via one of two distinct processes: 
Every Mach bomb retrieves a sync unit from a Facula bomb; for every Mach bomb, a Facula bomb is created;
Every Facula bomb spontaneously creates a Mach bomb.

For example, if you had 3 Mach bombs and 2 Facula bombs, they could either produce 3 Mach bombs and 5 Facula bombs, or 5 Mach bombs and 2 Facula bombs. The replication process can be changed each cycle. 

Second, you need to ensure that you have exactly the right number of Mach and Facula bombs to destroy the LAMBCHOP device. Too few, and the device might survive. Too many, and you might overload the mass capacitors and create a singularity at the heart of the space station - not good! 

And finally, you were only able to smuggle one of each type of bomb - one Mach, one Facula - aboard the ship when you arrived, so that's all you have to start with. (Thus it may be impossible to deploy the bombs to destroy the LAMBCHOP, but that's not going to stop you from trying!) 

You need to know how many replication cycles (generations) it will take to generate the correct amount of bombs to destroy the LAMBCHOP. Write a function solution(M, F) where M and F are the number of Mach and Facula bombs needed. Return the fewest number of generations (as a string) that need to pass before you'll have the exact number of bombs necessary to destroy the LAMBCHOP, or the string "impossible" if this can't be done! M and F will be string representations of positive integers no larger than 10^50. For example, if M = "2" and F = "1", one generation would need to pass, so the solution would be "1". However, if M = "2" and F = "4", it would not be possible.

Test cases
Inputs: (string) M = "2" (string) F = "1"

Output: (string) "1"

Inputs: (string) M = "4" (string) F = "7"

Output: (string) "4"

Inputs: (string) M = "2" (string) F = "4"

Output: (string) "impossible"

"""

# solution is quite simple, just work backwards. 11,5 -> 11-5, 5 = 6,5 -> 6-5,5 = 1,5 -> 1,5-1 = 1,4 -> etc


def solution(x, y):
    # input was a string
    x = int(x)
    y = int(y)

    # keeps coint
    generation = 0

    # once one of the two reaches one, you can just count down in one go, see example line 20
    # if one of the two is below 1, then its an imposible case
    while x > 1 and y > 1:
        # simply determine which should be substracted from which
        if x < y:
            # speeds up the process, first two steps in line 20 in one go
            generation += int(y/x)
            y = y % x
        elif y < x:
            generation += int(x/y)
            x = x % y
            # if x == y then you end up with an imposible case, just saves one move since while loop ends next regardless
        else:
            return "impossible"

    # determining between the option on line 30 and 31
    if x == 1 and y == 1:
        return str(generation)
    elif x == 1:
        # quickly counts down in one go
        generation += y - 1
        return generation
    elif y == 1:
        generation += x - 1
        return generation
    else:
        return "impossible"


print(solution("11", "5"))
print("next answer")
print(solution("793537395893705730750387057302853058235934", "3535098989350344"))
