import React, { Component } from 'react';
import './App.css';
import axios from 'axios'
import querystring from 'querystring';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceLine,
  Scatter,
  ScatterChart,
  ReferenceDot
} from 'recharts';
import moment from 'moment';

// Function to convert UNIX timestamp to a readable date format
var ConvertUNIX = (unix) => {
  return moment.unix(Number(unix)).format('DD-MM-YYYY');
};

// Create a custom tooltip that displays the time and the value
const CustomTooltip = ({ active, payload, label }) => {
  if (active) {
    // Convert the UNIX timestamp date to a readable format
    // payload[0] is the x value, payload[1] is the y value
    var workout_date = ConvertUNIX(payload[0].value);
    return (
      <div className="custom-tooltip">
        <p className="label">{`Workout Date: ${workout_date}`}</p>
        <p className="label">{`Est. One Rep Max: ${payload[1].value} kg`}</p>
      </div>
    );
  }

  return null;
};

// This is the component that holds all of our charts
class Charts extends Component {
    render() {
        return (
            <div className={'Charts'}>
            <h1 className='BodyType'>Legs</h1>
            <Chart exercise="Goblet Squat" />
            <Chart exercise="Stiff Leg Deadlift" />
            <Chart exercise="Leg Extension" />
            <Chart exercise="Deadlifts" />
            <Chart exercise="Squat" />
            <Chart exercise="Leg Press" />
            <h1 className='BodyType'>Shoulders</h1>
            <Chart exercise="DB Shoulder Press" />
            <Chart exercise="Military Press" />
            <Chart exercise="Standing Side Lateral Raise" />
            <Chart exercise="Rear Machine Fly" />
            <h1 className='BodyType'>Chest</h1>
            <Chart exercise="DB Bench" />
            <Chart exercise="Incline DB Bench" />
            <Chart exercise="Incline Bench Press" />
            <Chart exercise="Bench Press" />
            <Chart exercise="Machine Fly" />
            <h1 className='BodyType'> Back</h1>
            <Chart exercise="T-Bar Rows" />
            <Chart exercise="BB Row" />
            <Chart exercise="Wide Grip Lat Pulldown (Machine Kings Cross London)" />
            <Chart exercise="Bent Over DB Row" />
            <Chart exercise="BB Row (Underhand)" />
            <h1 className='BodyType'>Arms</h1>
            <Chart exercise="Barbell Curl (21s)" />
            <Chart exercise="Barbell Curl" />
            <Chart exercise="Rope Pushdown" />
            <Chart exercise="Standing DB Curl" />
            <Chart exercise="Close Grip Bench" />
            </div>
        );
    };
};

// This component is for each chart
class Chart extends Component{
  // Constructor function to set our initial state including exercise
  constructor(props) {
    super(props);
    this.state = {
      dates: [],
      max_date: '',
      max_one_rep_max: '',
      min_date: '',
      one_rep_max_estimates: [],
      chart: [],
      workouts: [],
      exercise: this.props.exercise
    };

  };

  // Mount function to fetch exercise details from the API
  componentDidMount() {
    this.fetchValues();
  }

  // This calls the API to get the exercise details
  async fetchValues() {
    // Async request to get the exercise details
    const values = await axios.post('/api/one-rep-max-estimates', querystring.stringify({
      exercise: this.state.exercise
    }));
    // Set the state from the results from the API
    this.setState({
      dates: values.data.dates,
      max_date: values.data.max_date,
      max_one_rep_max: values.data.max_one_rep_max,
      min_date: values.data.min_date,
      one_rep_max_estimates: values.data.one_rep_max_estimates,
      chart: values.data.chart});
  }

  // Render the chart for the exercise
  render() {
    return (
      <div className={'Exercises'}>
      <h2 align="center">{this.state.exercise}</h2>
      <ScatterChart
        width={1400}
        height={600}
        margin={{
          top: 20, right: 20, bottom: 20, left: 20,
        }}>

        <XAxis
          dataKey = 'workout'
          domain = {['auto', 'auto']}
          name = 'Workout Date'
          tickFormatter = {(unixTime) => moment.unix(Number(unixTime)).format('DD-MM-YYYY')}
          tickCount={20}
          type = 'number'
        />
        <YAxis
          dataKey='one_rep_max_estimate'
          name='Value'
          domain={[dataMin => (dataMin-10), dataMax => (dataMax+10)]} />
        <CartesianGrid />
        <Tooltip content={<CustomTooltip />} />
        <Scatter
          data = {this.state.chart}
          line = {{ stroke: "#00d8ff" }}
          lineJointType = 'monotone'
          lineType = 'joint'
          name = 'One Rep Max Est.'
          fill="#00d8ff"
          shape="circle"
        />
        <ReferenceLine y={this.state.max_one_rep_max} stroke="red" strokeDasharray="3 3"/>
        <ReferenceDot
          x={Number(this.state.max_date)}
          y={this.state.one_rep_max_estimates.slice(-1)[0]}
          r={3}
          fill="red"
          stroke="none" />
      </ScatterChart>
      </div>
    );
  };
};

export default Charts;
