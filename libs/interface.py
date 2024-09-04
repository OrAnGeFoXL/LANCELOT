import os
import math
from typing import List, Union

from libs.broker import *
from features.basic import calculate_percent_change


import toml
with open('config.toml') as f:
    cnf = toml.load(f)

def cn(num: Union[float, int]) -> str:
    """
    Colorize a number, positive -> green, negative -> red, 0 -> no color.
    Args:
        num: The number to colorize.
    Returns:
        The colorized number as a string.
    """
    if isinstance(num, (float, int)):

        if True:
            pass

        if num > 0:
            return f"\033[92m{num:.2f}\033[0m"  # зеленый цвет
        elif num < 0:
            return f"\033[91m{num:.2f}\033[0m"  # красный цвет
        else:
            return str(num)
    else:
        raise TypeError("Argument must be either int or float")


def draw_sparkline(values):
    """
    Выводит sparkline из значений в List.
    """
    if not values:
        return None  

    abs_values = [abs(v) for v in values]
    symbols = ' ▁▂▃▄▅▆▇█'

    max_value = max(abs_values)
    scale = len(symbols) / max_value

    sparkline = ''
    for value in values:
        index = int(abs(value) * scale)

        if index >= len(symbols):
            index = len(symbols) - 1
        
        symbol = symbols[index]

        if value > 0:
            sparkline += f"\033[92m{symbol}\033[0m"
        elif value < 0:
            sparkline += f"\033[91m{symbol}\033[0m"
        else:
            sparkline += symbol
        
    return sparkline, min(values), max(values)

def bar_chart(num, limit, label=True):

    blocks = ' ▏▎▍▌▋▊▉█'
    if label:
        label=' '+str(round(num,2))
    else:
        label = ''
    
    term_width = os.get_terminal_size()[0]-len(label)-1 #FIXME: число для поправки 

    if num < 0:
        color = '\033[91m'
    else:
        color = '\033[92m'

    num  = abs(num)
    bigger = max(num, limit)
    scale = term_width/bigger

    bar_ln = scale*num

    body_ln = math.modf(bar_ln)[1] #целая часть
    tail_ln = math.modf(bar_ln)[0] #остаток

    tail_scale = len(blocks)/10
    tail_index = int(10*round(tail_ln,1)*tail_scale)

    if tail_index >= len(blocks):
        tail_index = len(blocks)-1

    body = int(body_ln)*blocks[-1]
    tail = blocks[tail_index]
    bar = body + tail
    print(f"{color}{bar}{label}\033[0m")
    if num > limit:
        print(f"\033[91mЛимит превышен на {round((num-limit),2)}%!!!\033[0m")

    return 


def sparkline(figi: str, days: int = 10) -> str:

    history = get_history(figi, days)
    candles = CandlesSerial(history)
    pct_chg = calculate_percent_change(candles.close)
    sparkline = draw_sparkline(pct_chg)

    if not sparkline:
        return "NoData"

    if cnf["interface"]["sparkline"]["show_labels"]:
        label =f"{sparkline[1]:.2f} {sparkline[2]:.2f}"

    return sparkline[0]+label