import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
import json
from flask_cors import CORS

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
gym_hero = pd.read_csv("./data/gym-hero-export.csv")

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
            {key: 'max', 'Date': 'first'})

    max_one_rep_max = _exercise[key].max()
    min_date = _exercise['Date'].min()
    max_date = _exercise['Date'].max()

    return (
        {'max_one_rep_max': max_one_rep_max,
         'min_date': min_date,
         'max_date': max_date,
         'dates': list(_exercise['Date'].values),
         'one_rep_max_estimates': list(_exercise[key].values)}
     )

app = Flask(__name__)
CORS(app)
@app.route("/one-rep-max-estimates", methods=['POST'])
def hello():
    exercise = request.form.get('exercise')
    return (jsonify(timeline_max(exercise, one_rep=True)), 200)
