import React, { Component } from 'react'
import { Route, Switch, Redirect, withRouter } from "react-router-dom"
import {ThemeProvider} from '@material-ui/styles'
import NavbarComponent from './Components/wrapper/navbar'
import { Standalone as AgContextEditor } from './Components/forms/AgContextForm'
import { Standalone as MetadataEditor } from './Components/forms/MetadataForm'
import theme from './Components/ui/theme'
import './App.css'

class App extends Component {
	render() {
		return (
			<ThemeProvider theme={theme}>
				<Switch>
					<Redirect exact from="/" to="/explore" />
					<Route exact path='/agcontext/editor' component={AgContextEditor} />
					<Route exact path='/metadata/editor' component={MetadataEditor} /> {/* XXX: for development */}
					<Route exact path="/:page/:dataset_id?" render={props => <NavbarComponent {...props} />} />
				</Switch>
			</ThemeProvider>
		);
	}
}

export default withRouter(App);
