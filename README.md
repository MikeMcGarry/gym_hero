[![Build Status](https://travis-ci.org/MikeMcGarry/gym_hero.svg?branch=master)](https://travis-ci.org/MikeMcGarry/gym_hero)

# Gym Hero Progress Charts

If you use the Gym Hero app (https://gymhero.me/) you can use this repo to chart your progress. 

It allows you to easily create charts from your exported workouts using a React app and Python Flask API.


## Getting Started

To get started create a 'data' folder in the controller/python-flask-app directory. Then export your workouts via email from the Gym Hero App by going to Settings > Export Workouts. Once you have received the export via email save the csv (not the one with excel in the name) file that is attached inside this data folder. Leave the name as is. 

Then from the directory with the docker-compose.yml file run docker-compose up --build. 

You can then navigate to localhost:3000 to see your progress.

You can currently view over time the volume of your workouts and the estimated one rep max of your exercises.

Note that if you find your charts are not populated you may need to modify the default AXIOS base url from 0.0.0.0 to 127.0.0.1 (leave the port the same).


## Customising which Exercises and Workouts you See

To change which exercises you want to see, modify the exercise name in the React App. The same for which workout you'd like to see the volume for.

This currently only works with kilograms (kg) but can be easily modified to work with pounds (lb) or other units.


