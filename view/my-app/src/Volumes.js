import React, { Component } from 'react';
import './App.css';
import axios from 'axios'
import queryString from 'query-string';
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
  ReferenceDot,
  ResponsiveContainer
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
        <p className="label">{`Volume: ${payload[1].value} kg`}</p>
      </div>
    );
  }

  return null;
};

class Volumes extends Component {
    render() {
        return (
            <div className={'Charts'}>
            <h1 className='BodyType'>Workout Volume</h1>
            <Volume workout="Chest" />
            <Volume workout="Legs/Abs" />
            <Volume workout="Back & Abs" />
            <Volume workout="Shoulders & Abs" />
            <Volume workout="Arms" />
            </div>
        );
    };
};


class Volume extends Component{
  constructor(props) {
    super(props);
    this.state = {
      max_volume: '',
      min_date: '',
      max_date: '',
      dates: [],
      volume: [],
      chart: [],
      workout: this.props.workout
    };

  };

  componentDidMount() {
    this.fetchValues().catch(err => null);
  }

  async fetchValues() {
    const values = await axios.post('/api/volume', queryString.stringify({
      workout_type: this.state.workout
    }));
    this.setState({
      chart: values.data.chart,
      max_volume: values.data.max_volume,
      min_date: values.data.min_date,
      max_date: values.data.max_date,
      dates: values.data.dates,
      volume: values.data.volume});
  }

  // Render the chart for the exercise
  render() {
    return (
      <div className={'Exercises'}>
      <h2 align="center">{this.state.workout}</h2>
      <ResponsiveContainer width="90%" aspect={2.4}>
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
          dataKey='volume'
          name='Value'
          domain={[dataMin => (dataMin-1000), dataMax => (dataMax+1000)]} />
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
        <ReferenceLine y={this.state.max_volume} stroke="red" strokeDasharray="3 3"/>
        <ReferenceDot
          x={Number(this.state.max_date)}
          y={this.state.volume.slice(-1)[0]}
          r={3}
          fill="red"
          stroke="none" />
      </ScatterChart>
      </ResponsiveContainer>
      </div>
    );
  };
};


export default Volumes;
