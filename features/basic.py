
import pandas as pd
from pandas import DataFrame
import math
from tinkoff.invest import *
from tinkoff.invest.utils import now

import sys
import os
from typing import List, Union

from pprint import pprint

from datetime import timedelta 
import time

TOKEN = os.environ["INVEST_TOKEN"]

import toml
with open('config.toml') as f:
    cnf = toml.load(f)


def calculate_percent_change(lst: List[Union[float, int]]) -> List[float]:

    result = []
    for i in range(1, len(lst)):
        change = (lst[i] - lst[i-1]) / lst[i-1] * 100
        result.append(change)
    return result



if __name__ == "__main__":
    print(figi_ticker(["BBG000B9XRY4", "BBG000B9XRY4"]))