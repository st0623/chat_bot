from func.dice import roll_dices
import re

def judge_work(message):
    dice_pattern = r"^\d+d\d+$"

    if is_complete_match(dice_pattern, message):
        split_str = message.split("d")
        return roll_dices(int(split_str[0]), int(split_str[1]))

    return message

def is_complete_match(pattern, message):
    if re.match(pattern, message):
        return True
    else:
        return False


