import pandas as pd
import json
import urllib.request
import os
import time

def get_data(username, app_token):
    """
    This function takes the username of a GymHero user and their app token and
    returns all their workouts as a JSON object loaded into Python types.

    param (str) username: The username to get workouts for
    param (str) app_token: The app token of the user

    return (list): The list of nested dictionaries containing the workout details
    """

    # Get the workout data from the GymHero api
    while True:
        try:
            response = urllib.request.urlopen(
                "https://api.fitty.co/users/{}/workouts?app_token={}".format(
                    username, app_token
                )).read()
            # Convert it to json
            workout_data = json.loads(response.decode('utf-8'))

            return workout_data

        except:
            time.sleep(30)

def process_data(workout_data):
    """
    This function takes the workout data and processes to be ready to be served
    by the api.

    param (list) workout_data: The list of nested dictionaries containing the workout details

    return (DataFrame) workouts_df: The dataframe containing the workouts
    """

    # Initialise an empty list to hold each set
    sets = []

    # Map the unit keys to the units
    weight_mapping = {
        0: '-',
        1: 'lb',
        2: 'kg'
    }

    # Iterate over each workout
    for workout in workout_data:
        # Get the workout details
        workout_id = workout['id']
        finished = workout['finished']
        workout_name = workout['label']
        workout_date = workout['date']
        print ('Working on workout {}'.format(workout_id))
        # Iterate over each exercise
        for exercise in workout['exercises']:
            # Get the exercise details
            exercise_name = exercise['label']
            exercise_units = weight_mapping[exercise['unit']]
            # If there are no sets skip this exercise
            if exercise['sets'] is None:
                continue
            # Iterate over the sets
            for weight_set in exercise['sets']:

                # Get the reps
                reps = weight_set['reps']

                # Get the weight if it exists
                if 'weight' in weight_set:
                    weight = weight_set['weight']
                # Else set to 0
                else:
                    weight = 0

                # Create the details for the current set
                current_set = {
                    'Workout #': workout_id,
                    'Finished': finished,
                    'Workout': workout_name,
                    'Date': workout_date,
                    'Exercise': exercise_name,
                    'Unit': exercise_units,
                    'Weight': weight,
                    'Reps': reps
                }

                # Append it to the list
                sets.append(current_set)

    # Create a dataframe from the list of sets
    workouts_df = pd.DataFrame(sets)

    # Replace any null values with 0
    workouts_df['Weight'] = workouts_df['Weight'].fillna(value=0)
    workouts_df['Reps'] = workouts_df['Reps'].fillna(value=0)

    # Ensure all lb are converted to kg
    workouts_df['Unit'] = workouts_df['Unit'].apply(
        lambda x: 'kg' if x == 'lb' else x)

    # All other units as seconds
    workouts_df['Unit'] = workouts_df['Unit'].apply(
        lambda x: 'sec' if x == '-' else x)

    # Trim the dates so that they become seconds since 1970 rather than milliseconds
    workouts_df['Date'] = workouts_df['Date'].apply(
        lambda x: int(str(x)[:-3]))

    # Return the dataframe
    return workouts_df

def save_data(workouts_df, file_path):
    """
    This function saves a dataframe to a file

    param (DataFrame) workouts_df: The data frame to save to a file
    param (str) file_path: The path to the output file
    """

    workouts_df.to_csv(file_path)
    print ('Saved workout data to {}'.format(file_path))


while True:

    workout_data = get_data(
        username=os.environ['GYM_HERO_USERNAME'],
        app_token=os.environ['GYM_HERO_APP_TOKEN'])

    workouts_df = process_data(workout_data=workout_data)

    save_data(
        workouts_df=workouts_df,
        file_path="./data/gym-hero-export.csv"
    )
    time.sleep(600)
