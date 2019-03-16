import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios'
const querystring = require('querystring');


axios.defaults.baseURL = 'http://0.0.0.0:5000';

class Form1 extends Component{

  state = {
    dates: [],
    max_date: '',
    max_one_rep_max: '',
    min_date: '',
    one_rep_max_estimates: []
  };

  componentDidMount() {
    this.fetchValues();
  }

  async fetchValues() {
    const values = await axios.post('/one-rep-max-estimates', querystring.stringify({
      exercise: 'Deadlifts'
    }));
    this.setState({
      dates: values.data.dates,
      max_date: values.data.max_date,
      max_one_rep_max: values.data.max_one_rep_max,
      min_date: values.min_date,
      one_rep_max_estimates: values.one_rep_max_estimates});
  }

  render(){
      return (
          <div className="form1">
              <p>hi-{this.state.max_date}-{this.state.max_one_rep_max}</p>
          </div>
      );
  }
}

export default Form1;
