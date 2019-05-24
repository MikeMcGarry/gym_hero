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
while True:
    try:
        gym_hero = pd.read_csv("./data/gym-hero-export.csv")
        break
    except:
        print ('File does not exist yet, waiting 30 secs before retrying')
        time.sleep(30)


# Split out the headers
gym_hero_headers = gym_hero[np.isfinite(gym_hero['Workout duration'])]
gym_hero_headers = gym_hero_headers.drop(
    columns=[
        'Exercise',
        'Set #',
        'Reps',
        'Weight',
        'Unit',
        'Muscle group',
        'Workout'
        ]
    )

# Split out the exercise content
gym_hero_content = gym_hero[np.isfinite(gym_hero['Reps'])]
gym_hero_content = gym_hero_content.drop(
    columns=[
        'Date',
        'Workout duration',
        'Link',
        'Workout note'
        ]
    )

# Merge the two together
gym_hero_merged = pd.merge(
    gym_hero_content,
    gym_hero_headers,
    how='left',
    left_on='Workout #',
    right_on='Workout #'
)

# Fill in null values with 0 for weight
gym_hero_merged['Weight'] = gym_hero_merged['Weight'].fillna(value=0)

# Change anything with units of lb to kg
gym_hero_merged['Unit'] = gym_hero_merged['Unit'].apply(
    lambda x: 'kg' if x == 'lb' else x)

# Change anything with units of - to sec
gym_hero_merged['Unit'] = gym_hero_merged['Unit'].apply(
    lambda x: 'sec' if x == '-' else x)

# Convert the date to datetime format
gym_hero_merged['Date'] = pd.to_datetime(gym_hero_merged['Date'])


def timeline_max(exercise, one_rep_lookup=one_rep_max_lookup, one_rep=False):
    """
    This function

    param str exercise: The exercise to generate the one rep max estimates for
    param dict one_rep_lookup: The lookup table to use to find one rep max estimates
    param bool one_rep: A flag to specify whether or not to calculate one rep max estimates
    return dict: The one rep max estimates 

    """

    _exercise = gym_hero_merged.loc[
        gym_hero_merged['Exercise'] == exercise, :].copy(
            deep=True)

    key = 'Weight'

    if one_rep:
        _exercise['one_rep_max_ratio'] = _exercise['Reps'].apply(
            lambda x: one_rep_lookup[int(x)] if x in one_rep_lookup.keys() else 0)
        _exercise['one_rep_max'] = _exercise['Weight'].divide(
            _exercise['one_rep_max_ratio'])
        key = 'one_rep_max'

    _exercise = _exercise.groupby(
        ['Exercise', 'Date']).agg(
            {key: 'max', 'Date': 'first', 'Workout #': 'first'})

    max_one_rep_max = _exercise[key].max()

    dates = list(_exercise['Date'].apply(lambda x: str(int(time.mktime(x.timetuple())))).values)
    min_date = str(min(dates))
    max_date = str(max(dates))
    one_rep_max_estimates = list(_exercise[key].values)
    workouts = list(_exercise['Workout #'].values)
    chart = [{'workout': str(date), 'one_rep_max_estimate': str(round(weight,2))} for date, weight in zip(dates, one_rep_max_estimates)]

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
    gym_hero_merged_weighted = gym_hero_merged.loc[gym_hero_merged['Unit'] == 'kg']
    gym_hero_merged_weighted = gym_hero_merged.loc[gym_hero_merged['Workout'] == workout_type]
    gym_hero_merged_weighted_copy = gym_hero_merged_weighted.copy(deep=True)
    gym_hero_merged_weighted['volume'] = gym_hero_merged_weighted_copy.loc[:, 'Reps'].multiply(
        gym_hero_merged_weighted_copy.loc[:, 'Weight'], axis=0)
    gym_hero_merged_weighted_sum = gym_hero_merged_weighted.groupby('Workout #').agg({
        'Workout': 'first',
        'volume': 'sum',
        'Date':'first',
        'Workout duration':'first'})

    dates = list(gym_hero_merged_weighted_sum['Date'].apply(lambda x: str(int(time.mktime(x.timetuple())))).values)
    volume = list(gym_hero_merged_weighted_sum['volume'].values)
    min_date = str(min(dates))
    max_date = str(max(dates))
    max_volume = gym_hero_merged_weighted_sum['volume'].max()
    chart = [{'workout': str(date), 'volume': str(round(volume,2))} for date, volume in zip(dates, volume)]
    return (
        {'max_volume': max_volume,
         'min_date': min_date,
         'max_date': max_date,
         'dates': dates,
         'volume': volume,
         'chart': chart,
         }
    )


app = Flask(__name__)
CORS(app)

@app.route("/one-rep-max-estimates", methods=['POST'])
def POST_one_rep_max_estimates():
    exercise = request.form.get('exercise')
    return (jsonify(timeline_max(exercise, one_rep=True)), 200)

@app.route("/volume", methods=['POST'])
def GET_volume():
    workout_type = request.form.get('workout_type')
    return (jsonify(volume(workout_type)), 200)
