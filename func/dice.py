import random
import sys

MAX_DICE_TIME_NUM = 100


def roll_dices(max_num, times):
    if isinstance(max_num, str) and not max_num.isdigit():
        return None

    if isinstance(times, str) and not times.isdigit():
        return None

    if times < 1 or MAX_DICE_TIME_NUM < times  : 
        return None

    if sys.maxsize < 1 or sys.maxsize < max_num :
        return None

    dice = []
    for _ in range(times):
        dice.append(random.randint(1, max_num))

    return dice
    
