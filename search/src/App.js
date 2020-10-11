import React, { Component } from 'react';
import ReactiveSearchComponent from './Components/reactive_search';
import LoginComponent from './Components/login'
import RegisterComponent from './Components/register'
import './App.css';
import {
	Switch,
	Route,
	Redirect
} from 'react-router-dom';

class App extends Component {

	constructor(){
		super();
		this.state = {
			isLoggedIn: true
		}
	}

	render() {
		return (
			<div>
				<Switch>
					<Route exact path="/">
					{
						!this.state.isLoggedIn ?
						<Redirect to="/login"/>:
						<Redirect to="/search"/>
					}
					</Route>
					<Route exact path="/login">
						<LoginComponent />
					</Route>
					<Route exact path="/register">
						<RegisterComponent />
					</Route>
					<Route exact path="/search">
						<ReactiveSearchComponent />
					</Route>
				</Switch>
			</div>
		)
	}
}

export default App;
