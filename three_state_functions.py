#  This module is a set of tools for visualizing and generating fields from a 3-state cellular automaton
#  as part of the PHY250 SQ 2020 course at UC Davis.

from math import floor
import random
from matplotlib import pyplot as plt


def base_ten_to_ternary(int_in):
    #  This produces a (string) ternary representation for integers smaller than 19682.
    ternary_representation = []
    remainder = int_in
    for i in range(8, -1, -1):
        new_digit = str(floor(remainder / 3 ** i))
        ternary_representation.append(new_digit)
        remainder = remainder - int(new_digit) * 3 ** i
    return "".join(ternary_representation)


def get_stilted_ternary_lookup(ternary_rule):
    #  This produces a dictionary of neighborhoods and their appropriate outputs.
    lookup_table = {}
    neighborhoods = [
        (2, 2),
        (2, 1),
        (2, 0),
        (1, 2),
        (1, 1),
        (1, 0),
        (0, 2),
        (0, 1),
        (0, 0),
    ]
    for i in range(9):
        key = neighborhoods[i]
        val = ternary_rule[i]
        lookup_table.update({key: val})
    return lookup_table


def random_ternary_initial_condition(length):
    #  This generates a list, whose elements are in 0,1,2, for evolution by an CA.
    initial_condition = []
    for i in range(length):
        initial_condition.append(random.randint(0, 2))
    return initial_condition


"""
def plot_spacetime_field(field_in):
    plt.figure(figsize=(12,12))
    plt.imshow(field_in, cmap=plt.cm.Greys, interpolation='nearest')
    plt.show()
"""


def show_random_field(rule_number_in):
    # This Quickly plots a random-initial-condition spacetime field given only a rule number.
    local_length = 100
    local_n_timesteps = 100
    local_ternary_ca = CA3StateStilted(rule_number_in)
    local_initial_condition = random_ternary_initial_condition(local_length)
    local_spacetime_field = SpacetimeField(
        local_ternary_ca.evolve(
            local_n_timesteps, local_length, local_initial_condition
        )
    )
    local_spacetime_field.plot_spacetime_field()
    # print(local_ternary_ca.lookup_table)


class CA3StateStilted:
    def __init__(self, rule_number):
        self.rule_number = rule_number
        # print('inside')
        self.ternary_rule = base_ten_to_ternary(self.rule_number)
        # print('ternary inside:' + str(self.ternary_rule))
        self.lookup_table = get_stilted_ternary_lookup(self.ternary_rule)

    def evolve(self, time_steps, length, initial_condition):
        #  The CA evolves an initial condition and returns a spacetime field.
        if time_steps < 0:
            raise ValueError("time_steps must be a non-negative integer")
        # try converting time_steps to int and raise a custom error if this can't be done
        try:
            time_steps = int(time_steps)
        except ValueError:
            raise ValueError("time_steps must be a non-negative integer")
        spacetime = []
        current_configuration = initial_condition
        for _ in range(time_steps):  # use underscore if the index will not be used
            new_configuration = []
            for i in range(length):
                neighborhood = (
                    int(current_configuration[(i - 1)]),
                    int(current_configuration[i]),
                )
                new_configuration.append(int(self.lookup_table[neighborhood]))

            current_configuration = new_configuration
            spacetime.append(new_configuration)
        return spacetime


class SpacetimeField:
    def __init__(self, field_in):
        self.field = field_in

    def plot_spacetime_field(self):
        plt.figure(figsize=(12, 12))
        plt.imshow(self.field, cmap=plt.cm.Greys, interpolation="nearest")
        plt.show()


''' Example: Here's how one might use the previous classes/functions.
rule_number = 15897
length = 10
n_timesteps = 10

# initializing the 3-state stilted automaton
ternary_ca = CA3StateStilted(rule_number)
initial_condition = random_ternary_initial_condition(length)
my_field = SpacetimeField(ternary_ca.evolve(n_timesteps, length, initial_condition))
my_field.plot_spacetime_field()

for i in range(100):
    show_random_field(i)

'''
