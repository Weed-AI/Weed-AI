import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import './index.css';
import App from './App';
import { Standalone as AgContextEditor } from './AgContextForm';
import * as serviceWorker from './serviceWorker';


//import RouterMapping from './RouterMapping';
const RouterMapping = () => (
  <Router>
    <Route exact path='/' component={App} />
    <Route exact path='/agcontext/editor' component={AgContextEditor} />
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
