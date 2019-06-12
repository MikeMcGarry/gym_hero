import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
import json
from flask_cors import CORS
import time
import datetime

'''
The lookup table for generating the one rep max estimate, the key is the number
of reps and the value is the percentage of the one rep maximum the weight at
this number of reps is estimated to be.

To get the one rep maximum from this value you divide the weight by it.
'''
one_rep_max_lookup = {
    1: 1,
    2: 0.97,
    3: 0.94,
    4: 0.92,
    5: 0.89,
    6: 0.86,
    7: 0.83,
    8: 0.81,
    9: 0.78,
    10: 0.75,
    11: 0.73,
    12: 0.72,
    13: 0.70,
    14: 0.68,
    15: 0.67,
    16: 0.65,
    17: 0.64,
    18: 0.63,
    19: 0.61,
    20: 0.60,
    21: 0.59,
    22: 0.58,
    23: 0.57,
    24: 0.56,
    25: 0.55,
    26: 0.54,
    27: 0.53,
    28: 0.52,
    29: 0.51,
    30: 0.50
}

# Import the workout data
def import_data():
    while True:
        try:
            # Read the data
            gym_hero = pd.read_csv("./data/gym-hero-export.csv")
            return gym_hero
            break
        except:
            # Wait 30 seconds and print an update if it can't be found
            print ('File does not exist yet, waiting 5 secs before retrying')
            time.sleep(5)


def timeline_max(exercise, one_rep_lookup=one_rep_max_lookup, one_rep=False):
    """
    This function takes an exercise and determines either the gross maximum
    weight lifted or the estimated one rep maximum for each workout over time

    param (str) exercise: The exercise to generate the one rep max estimates for
    param (dict) one_rep_lookup: The lookup table to use to find one rep max estimates
    param (bool) one_rep: A flag to specify whether or not to calculate one rep max estimates
    return (dict): The one rep max estimates over time
    """
    gym_hero_merged = import_data()

    # Get all the rows associated with this exercise
    _exercise = gym_hero_merged.loc[
        gym_hero_merged['Exercise'] == exercise, :].copy(
            deep=True)

    # The key to find the maximum gross weight lifted for each workout
    key = 'Weight'

    # If the one rep flag is true use the estimated one rep maximum
    if one_rep:
        # Caclculate the one rep max ratio for the given number of reps for each set
        _exercise['one_rep_max_ratio'] = _exercise['Reps'].apply(
            lambda x: one_rep_lookup[int(x)] if x in one_rep_lookup.keys() else 0)
        # Divide the weight of each set by this ratio to get the estimated one rep max
        _exercise['one_rep_max'] = _exercise['Weight'].divide(
            _exercise['one_rep_max_ratio'])
        # Set the key to find the maximum one rep maximum for each workout
        key = 'one_rep_max'

    # Group the exercises by workout and take the max value of the key
    _exercise = _exercise.groupby(
        ['Exercise', 'Date']).agg(
            {key: 'max', 'Date': 'first', 'Workout #': 'first'})

    # Find the maximum one rep maximum across all workouts, i.e. personal best
    max_one_rep_max = _exercise[key].max()

    # Get the dates
    dates = list(_exercise['Date'].values)
    # Get the date of the first ever workout with this exercise
    min_date = str(min(dates))
    # Get the date of the most recent workout with this exercise
    max_date = str(max(dates))
    # Convert the dates to strings
    dates = [str(date) for date in dates]
    # Get the one rep max estimates to a list
    one_rep_max_estimates = list(_exercise[key].values)
    # Get the workout numbers as a list
    workouts = list(_exercise['Workout #'].values)
    # Create a list of key value pairs with the workout date and estimated one rep maximum
    # This is to make it easier for charting in other applications
    chart = [{'workout': str(date), 'one_rep_max_estimate': str(round(weight,2))} for date, weight in zip(dates, one_rep_max_estimates)]
    # Return a dictionary with all the values created above
    return (
        {'max_one_rep_max': max_one_rep_max,
         'min_date': min_date,
         'max_date': max_date,
         'dates': dates,
         'one_rep_max_estimates': list(_exercise[key].values),
         'chart': chart,
         }
     )

def volume(workout_type):
    """
    This function takes a workout name and returns the total volume for that
    workout type over time

    param (str) workout_type: The name of the workout
    return (dict): The volume figures over time
    """

    gym_hero_merged = import_data()

    # Filter out all exercises that aren't recorded in kilograms
    gym_hero_merged_weighted = gym_hero_merged.loc[gym_hero_merged['Unit'] == 'kg']
    # Select all workouts which match the given workout type
    gym_hero_merged_weighted = gym_hero_merged.loc[gym_hero_merged['Workout'] == workout_type]
    # Make a copy
    gym_hero_merged_weighted_copy = gym_hero_merged_weighted.copy(deep=True)
    # Get a volume figure for each set of each exercise
    gym_hero_merged_weighted['volume'] = gym_hero_merged_weighted_copy.loc[:, 'Reps'].multiply(
        gym_hero_merged_weighted_copy.loc[:, 'Weight'], axis=0)
    # Sum the volume figures for each workout
    gym_hero_merged_weighted_sum = gym_hero_merged_weighted.groupby('Workout #').agg({
        'Workout': 'first',
        'volume': 'sum',
        'Date':'first'})

    # Create a list of the dates in a format that can be easily consumed
    dates = list(gym_hero_merged_weighted_sum['Date'].values)
    # Create a list of the volume figures
    volume = list(gym_hero_merged_weighted_sum['volume'].values)
    # Get the date of the first ever workout of this type
    min_date = str(min(dates))
    # Get the date of the most recent workout of this type
    max_date = str(max(dates))
    # Convert the dates to strings
    dates = [str(date) for date in dates]
    # Get the maximum volume across all workouts of this type
    max_volume = gym_hero_merged_weighted_sum['volume'].max()
    # Create a list of key value pairs with the workout date and the volume
    # This is to make it easier for charting in other applications
    chart = [{'workout': str(date), 'volume': str(round(volume,2))} for date, volume in zip(dates, volume)]
    # Return a dictionary with all the values created above
    return (
        {'max_volume': max_volume,
         'min_date': min_date,
         'max_date': max_date,
         'dates': dates,
         'volume': volume,
         'chart': chart,
         }
    )

# Create a new Flask app
app = Flask(__name__)
# Turn CORS on
CORS(app)

# POST request method for getting one rep max estimates
@app.route("/one-rep-max-estimates", methods=['POST'])
def POST_one_rep_max_estimates():
    """
    This function gets the exercise from a POST request and returns the
    one rep max estimates over time

    return (dict): The one rep max estimates over time
    """
    exercise = request.form.get('exercise')
    return (jsonify(timeline_max(exercise, one_rep=True)), 200)

@app.route("/volume", methods=['POST'])
def GET_volume():
    """
    This function gets the workout type from a POST request and returns
    the volume for this workout type over time

    return (dict): The volume figures over time
    """
    workout_type = request.form.get('workout_type')
    return (jsonify(volume(workout_type)), 200)
