import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios'

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
    const values = await axios.post('/one-rep-max-estimates', {
      exercise: "DB Bench"
    });
    this.setState({
      dates: values.dates,
      max_date: values.max_date,
      max_one_rep_max: values.max_one_rep_max,
      min_date: values.min_date,
      one_rep_max_estimates: values.one_rep_max_estimates});
  }

  render(){
      return (
          <div class="form">
              <form action="http://localhost:5000/one-rep-max-estimates" method="post">
                  JSON Exercise: <input type="text" name="place"/>
                  <input type="submit" value="Submit"/>
              </form>
          </div>
      );
  }
}

export default Form1;
