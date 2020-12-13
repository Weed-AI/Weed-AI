import React, { Component } from 'react';
import {ThemeProvider} from '@material-ui/styles'
import NavbarComponent from './Components/wrapper/navbar'
import theme from './Components/ui/theme'
import './App.css'


class App extends Component {
	render() {
		return (
			<ThemeProvider theme={theme}>
				<NavbarComponent />
			</ThemeProvider>
		);
	}
}

export default App;
