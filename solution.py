import pytest
from datetime import datetime
import statistics as s

# Your task is to write the group adjustment method below. There are some
# unimplemented unit_tests at the bottom which also need implementation.
# Your solution can be pure python, pure NumPy, pure Pandas
# or any combination of the three.  There are multiple ways of solving this
# problem, be creative, use comments to explain your code.

# Group Adjust Method
# The algorithm needs to do the following:
# 1.) For each group-list provided, calculate the means of the values for each
# unique group.
#
#   For example:
#   vals       = [  1  ,   2  ,   3  ]
#   ctry_grp   = ['USA', 'USA', 'USA']
#   state_grp  = ['MA' , 'MA' ,  'CT' ]
#
#   There is only 1 country in the ctry_grp list.  So to get the means:
#     USA_mean == mean(vals) == 2
#     ctry_means = [2, 2, 2]
#   There are 2 states, so to get the means for each state:
#     MA_mean == mean(vals[0], vals[1]) == 1.5
#     CT_mean == mean(vals[2]) == 3
#     state_means = [1.5, 1.5, 3]
#
# 2.) Using the weights, calculate a weighted average of those group means
#   Continuing from our example:
#   weights = [.35, .65]
#   35% weighted on country, 65% weighted on state
#   ctry_means  = [2  , 2  , 2]
#   state_means = [1.5, 1.5, 3]
#   weighted_means = [2*.35 + .65*1.5, 2*.35 + .65*1.5, 2*.35 + .65*3]
#
# 3.) Subtract the weighted average group means from each original value
#   Continuing from our example:
#   val[0] = 1
#   ctry[0] = 'USA' --> 'USA' mean == 2, ctry weight = .35
#   state[0] = 'MA' --> 'MA'  mean == 1.5, state weight = .65
#   weighted_mean = 2*.35 + .65*1.5 = 1.675
#   demeaned = 1 - 1.675 = -0.675
#   Do this for all values in the original list.
#
# 4.) Return the demeaned values

# Hint: See the test cases below for how the calculation should work.


def group_adjust(vals, groups, weights):
    """
    Calculate a group adjustment (demean).

    Parameters
    ----------

    vals    : List of floats/ints

        The original values to adjust

    groups  : List of Lists

        A list of groups. Each group will be a list of ints

    weights : List of floats

        A list of weights for the groupings.

    Returns
    -------

    A list-like demeaned version of the input values
    """
    if len(groups) != len(weights):
        raise ValueError("Number of groups must equal number of weights")
    for group in groups:
        if len(group) != len(vals):
            raise ValueError(
                "Number of items in each group must equal number of vals")

    weighted_means = [0 for num in vals]

    # Iterate through the groups and create a list of group means
    for group, weight in zip(groups, weights):
        mean_dict = {}
        value_group = 0

        # Build a dictionary of Group Item -> List of values
        mean_dict = {}
        for group_zip, val in zip(group, vals):
            if group_zip not in mean_dict:
                mean_dict[group_zip] = [val]
            else:
                mean_dict[group_zip].append(val)

        # Calculate the mean of the List of values and update the weighted mean array
        for value_list in mean_dict.values():

            # The weighted mean is the mean of all the values * weight
            weighted_mean = s.mean(
                val for val in value_list if val is not None) * weight

            # Update the weighted mean array
            for index in range(len(value_list)):
                weighted_means[value_group] += weighted_mean
                value_group += 1

    # Finally calculate the demeaned values
    final_values = [x if x is None else x-y for x,
                    y in zip(vals, weighted_means)]

    return final_values
