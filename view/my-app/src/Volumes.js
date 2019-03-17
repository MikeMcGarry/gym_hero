import React, { Component } from 'react';
import './App.css';
import axios from 'axios'
import querystring from 'querystring';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ReferenceLine, Dot
} from 'recharts';

axios.defaults.baseURL = 'http://0.0.0.0:5000';


class Volumes extends Component {
    render() {
        return (
            <div className={'Charts'}>
            <Volume workout="Chest" />
            <Volume workout="Legs" />
            <Volume workout="Back" />
            <Volume workout="Shoulders" />
            <Volume workout="Arms" />
            </div>
        );
    };
};


class Volume extends Component{
  constructor(props) {
    super(props);
    this.state = {
      chart: [],
      workout: this.props.workout
    };

  };

  componentDidMount() {
    this.fetchValues();
  }

  async fetchValues() {
    const values = await axios.post('/volume', querystring.stringify({
      workout_type: this.state.workout
    }));
    this.setState({
      chart: values.data.chart});
  }

  render() {
    return (
      <div className={'Exercises'}>
      <h1 align="center">{this.state.workout}</h1>
      <LineChart
        width={1400}
        height={500}
        data={this.state.chart}
        margin={{
          top: 5, right: 30, left: 20, bottom: 10,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="workout" />
        <YAxis
          dataKey="volume"
          type="number"
          domain={[dataMin => (dataMin-1000), dataMax => (dataMax + 1000)]}/>
        <Tooltip
          active="True"/>
        <Legend />
        <Line type="monotone" dataKey="volume" stroke="#00d8ff" />
      </LineChart>
      </div>
    );
  };
};


export default Volumes;
