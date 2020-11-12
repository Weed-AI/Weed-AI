import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter as Router, Route, Link} from 'react-router-dom';
import './index.css';
import App from './App';
import Form from './Form';
import * as serviceWorker from './serviceWorker';

//import RouterMapping from './RouterMapping';
const RouterMapping = () => (
  <Router>
    <Route exact path='/' component={App} />
    <Route path='/Form,' component={Form} />

  </Router>
);

ReactDOM.render(
  <RouterMapping />, 
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
