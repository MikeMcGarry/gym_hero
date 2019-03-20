import React from 'react';
import ReactDOM from 'react-dom';
import Charts from './Charts';
import Volumes from './Volumes';

it('renders without crashing', () => {
  const div = document.createElement('div');
  ReactDOM.render(<Charts />, div);
  ReactDOM.unmountComponentAtNode(div);
  ReactDOM.render(<Volumes />, div);
  ReactDOM.unmountComponentAtNode(div);
});
