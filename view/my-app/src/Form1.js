import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios'
import querystring from 'querystring';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
} from 'recharts';

axios.defaults.baseURL = 'http://0.0.0.0:5000';

class Form1 extends Component{

  state = {
    dates: [],
    max_date: '',
    max_one_rep_max: '',
    min_date: '',
    one_rep_max_estimates: [],
    chart: [],
    workouts: []
  };

  componentDidMount() {
    this.fetchValues();
  }

  async fetchValues() {
    const values = await axios.post('/one-rep-max-estimates', querystring.stringify({
      exercise: 'DB Shoulder Press'
    }));
    this.setState({
      dates: values.data.dates,
      max_date: values.data.max_date,
      max_one_rep_max: values.data.max_one_rep_max,
      min_date: values.data.min_date,
      one_rep_max_estimates: values.data.one_rep_max_estimates,
      chart: values.data.chart});
  }

  render() {
    return (
      <LineChart
        width={500}
        height={300}
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
        <Line type="monotone" dataKey="pv" stroke="#8884d8" activeDot={{ r: 8 }} />
        <Line type="monotone" dataKey="one_rep_max_estimate" stroke="#82ca9d" />
      </LineChart>
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

export default Form1;
