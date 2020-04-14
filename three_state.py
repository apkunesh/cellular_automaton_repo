#  This script is a lightly "spaghettified" version of code which plots a 100x100 field for a
#  3-state half-lightcone 1-D cellular automata. 
#  This code is noncompliant with PEP-8 (though I don't think it's that far off.) For compliant code,
#  please check out "three_state_functions," which contains the same machinery, but unspaghettified.

from math import floor
import random
from matplotlib import pyplot as plt

rule_number = random.randint(0,6000)
n_timesteps = 100
length = 100

ternary_representation = []
remainder = rule_number
for i in range(8,-1,-1):
    new_digit = str(floor(remainder/3**i))
    ternary_representation.append(new_digit)
    remainder = remainder -int(new_digit)*3**i
ternary_representation = ''.join(ternary_representation)
neighborhoods = [(2,2),(2,1),(2,0),(1,2),(1,1),(1,0),(0,2),(0,1),(0,0)]
lookup_table = {}

for i in range(9):
    key = neighborhoods[i]
    val = ternary_representation[i]
    lookup_table.update({key:val})

initial_condition = []
for i in range(length):
    initial_condition.append(random.randint(0,2))

spacetime_field = [initial_condition]
current_configuration = initial_condition.copy()

for t in range(n_timesteps):
    new_configuration = []
    for i in range(len(current_configuration)):
        neighborhood = (current_configuration[(i-1)], 
                        current_configuration[i])
        new_configuration.append(int(lookup_table[neighborhood]))
    current_configuration = new_configuration
    spacetime_field.append(new_configuration)

plt.figure(figsize=(12,12))
plt.imshow(spacetime_field, cmap=plt.cm.Greys, interpolation='nearest')
plt.show()