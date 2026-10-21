import numpy as np
import pandas as pd

BATTERY_LEVELS = [85, 42, 67, 19, 90, 55]
ROBOT_IDS = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6']
LOW_LIMIT = 50
TOP_UP = 5


def make_battery_array(levels):
    return np.array(levels)


def make_battery_series(levels, robot_ids):
    return pd.Series(levels, index=robot_ids)


def battery_of(series, robot_id):
    return series[robot_id]


def low_battery(series):
    return series[series < LOW_LIMIT]


def top_up(battery_array):
    return battery_array + TOP_UP


def main():
    battery_array = make_battery_array(BATTERY_LEVELS)

    print("Shape:", battery_array.shape)
    print("Dtype:", battery_array.dtype)
    print()

    series = make_battery_series(BATTERY_LEVELS, ROBOT_IDS)

    print("Battery levels:")
    print(series)
    print()

    print("Battery of R4:", battery_of(series, 'R4'))
    print()

    print("Robots below", LOW_LIMIT, "percent:")
    print(low_battery(series))
    print()

    print("After top-up:", top_up(battery_array))


if __name__ == "__main__":
    main()