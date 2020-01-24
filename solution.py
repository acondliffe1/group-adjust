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

    group_means = []

    # Iterate through the groups and create a list of group means
    for group in groups:
        group_mean = []
        mean_dict = {}

        # Build a dictionary of Key -> List of values
        start = datetime.now()

        for item in range(len(group)):
            key = group[item]
            if key not in mean_dict:
                mean_dict[key] = [vals[item]]
            else:
                mean_dict[key].append(vals[item])

        end = datetime.now()
        print("Dictionary build: " + str(end - start))

        # Calculate the mean of the List of values and add it to the group means
        start = datetime.now()
        for lst in mean_dict.values():
            mean = s.mean(val for val in lst if val is not None)
            group_mean.extend([mean for index in range(len(lst))])
        group_means.append(group_mean)
        end = datetime.now()
        print("Calculate means: " + str(end - start))

    weighted_means = []

    start = datetime.now()

    for mean_group in zip(*group_means):
        weighted_means.append(
            sum(mean*weight for mean, weight in zip(mean_group, weights)))

    end = datetime.now()
    print("Weighted Means: " + str(end - start))
    start = datetime.now()
    final_values = [x if x is None else x-y for x,
                    y in zip(vals, weighted_means)]
    end = datetime.now()
    print("Final: " + str(end - start))
    return final_values

    # raise NotImplementedError
vals = [1, None, 3, 8, 5]
grps_1 = ['USA', 'USA', 'USA', 'USA', 'USA']
grps_2 = ['MA', 'MA', 'MA', 'RI', 'RI']
grps_3 = ['WEYMOUTH', 'BOSTON', 'BOSTON', 'PROVIDENCE', 'PROVIDENCE']
weights = [.15, .35, .5]

vals = 1000000*[1, None, 3, 5, 8, 7]
# If you're doing numpy, use the np.NaN instead
#vals = 1000000 * [1, np.NaN, 3, 5, 8, 7]
grps_1 = 1000000 * [1, 1, 1, 1, 1, 1]
grps_2 = 1000000 * [1, 1, 1, 1, 2, 2]
grps_3 = 1000000 * [1, 2, 2, 3, 4, 5]
weights = [.20, .30, .50]

group_adjust(vals, [grps_1, grps_2, grps_3], weights)
