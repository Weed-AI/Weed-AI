import React, { Component } from 'react';
import ReactiveSearchComponent from './Components/reactive_search';
import LoginComponent from './Components/login'
import RegisterComponent from './Components/register'
import './App.css';
import {
	Switch,
	Route,
	Redirect,
	withRouter
} from 'react-router-dom';

class App extends Component {

	constructor(){
		super();
		this.state = {
			isLoggedIn:  localStorage.getItem('isLoggedIn')? JSON.parse(localStorage.getItem('isLoggedIn')): false,
			registeredUsers: localStorage.getItem('registeredUsers')? JSON.parse(localStorage.getItem('registeredUsers')): []
		}
		this.registerUser = this.registerUser.bind(this);
		this.loginUser = this.loginUser.bind(this);
	}

	componentDidUpdate(){
		localStorage.setItem('isLoggedIn', JSON.stringify(this.state.isLoggedIn))
		localStorage.setItem('registeredUsers', JSON.stringify(this.state.registeredUsers))
	}

	registerUser(form_user) {
		const {firstName, lastName, email, password} = form_user;
		this.setState(prevState => {
			return {
				registeredUsers: [
					...prevState.registeredUsers,
					{
						firstName: firstName,
						lastName: lastName,
						email: email,
						password: password
					}
				]
			}
		})
		this.props.history.push("/")
	}

	loginUser(form_user) {
		const {email, password} = form_user;
		this.state.registeredUsers.forEach(user => {
			if(user.email === email && user.password === password){
				this.setState({
					isLoggedIn: true,
				})
				this.props.history.push("/")
			}
		})
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
						<LoginComponent loginHandler={this.loginUser}/>:
					</Route>
					<Route exact path="/register">
						<RegisterComponent registerHandler={this.registerUser}/>
					</Route>
					<Route exact path="/search">
						<ReactiveSearchComponent />:
					</Route>
				</Switch>
			</div>
		)
	}
}

export default withRouter(App);
