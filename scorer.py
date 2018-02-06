"""
SCORER
Module to calculate and score fantasy points

"""

"""
Standard ESPN points for offensive players. Legend for points keys:
    - yd: yard gained
    - pass_yd: passing yard gained
    - td: touchdown
    - pass_td: passing touchdown
    - 2pt_conv: successful 2 point conversion
    - int: interception
    - fum: fumble
"""
STANDARD = {
    "yd": 0.1,
    "pass_yd": 0.04,
    "td": 6.0,
    "pass_td": 4.0,
    "2pt_conv": 2.0,
    "fum": -2.0,
    "int": -2.0
}


class Scorer():
    """
    Class to score fantasy points.

    :param point_system: dict of scorable metrics and their points

    """

    def __init__(self, point_system=STANDARD):
        self.point_system = point_system

    def calculate(self, metrics):
        pass

if __name__ == "__main__":
    pass
