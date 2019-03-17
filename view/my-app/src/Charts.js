import React, { Component } from 'react';
import './App.css';
import axios from 'axios'
import querystring from 'querystring';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ReferenceLine
} from 'recharts';

axios.defaults.baseURL = 'http://0.0.0.0:5000';

class Charts extends Component {
    render() {
        return (
            <div className={'Charts'}>
            <Chart exercise="DB Shoulder Press" />
            <Chart exercise="Goblet Squat" />
            <Chart exercise="Deadlifts" />
            <Chart exercise="BB Row" />
            </div>
        );
    };
};

class Chart extends Component{
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

  componentDidMount() {
    this.fetchValues();
  }

  async fetchValues() {
    const values = await axios.post('/one-rep-max-estimates', querystring.stringify({
      exercise: this.state.exercise
    }));
    this.setState({
      dates: values.data.dates,
      max_date: values.data.max_date,
      max_one_rep_max: values.data.max_one_rep_max,
      min_date: values.data.min_date,
      one_rep_max_estimates: values.data.one_rep_max_estimates,
      chart: values.data.chart});
    return values;
  }

  render() {
    return (
      <div className={'Exercises'}>
      <h1 align="center">{this.state.exercise}</h1>
      <LineChart
        width={1000}
        height={500}
        data={this.state.chart}
        margin={{
          top: 5, right: 30, left: 20, bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="workout" />
        <YAxis />
        <Tooltip />
        <Legend />
        <ReferenceLine y={this.state.max_one_rep_max} stroke="red" strokeDasharray="3 3" />
        <Line type="monotone" dataKey="one_rep_max_estimate" stroke="#00d8ff" />
      </LineChart>
      </div>
    );
  };
};

/*

  render(){
      return (
          <div className="form1">
              <p>hi-{this.state.chart}-{this.state.max_date}</p>
          </div>
      );
  }
}

*/

export default Charts;
