import numpy as np

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
    if len(groups) != len(weights):
        raise ValueError("Number of groups must equal number of weights")
    for group in groups:
        if len(group) != len(vals):
            raise ValueError(
                "Number of items in each group must equal number of vals")

    # Turn all inputs into NP arrays
    vals = np.array(vals)
    groups = np.array(groups)
    weights = np.array(weights)

    # Create an empty array for the weighted means that we calculate
    weighted_means = np.zeros(len(vals))

    # For each group in the group list, take the weight and calculate the weighted means for each unique element
    for group, weight in zip(groups, weights):
        u = np.unique(group)

        # For each unique group calculate a weighted mean by:
        #  1. Get the positions of the elements in the group and select the values that we are interested in from vals
        #  2. Calculate a weighted mean and use the positions to apply it to the accumulated weighted means
        for group_num in u:
            positions = [group == group_num]

            group_vals = np.select(positions, [vals], np.NaN)
            weighted_mean = np.nanmean(group_vals) * weight
            mean_array = np.zeros(len(vals))
            np.putmask(mean_array, positions, weighted_mean)
            weighted_means += mean_array

    # Final demeaned values
    final_vals = vals - weighted_means

    return final_vals
