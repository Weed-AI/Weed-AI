import React from 'react';
import About from './components/header/About';
import Welcome from './components/header/Welcome';
import NavBar from './components/header/NavBar';
import ReactiveSearchComponent from './components/reactive_search';
import { Route, Switch, Redirect } from 'react-router-dom';

export const Routes = () => {
    return (
        <div>
            <NavBar />
            <Switch>
                <Route exact path="/Welcome" component={Welcome} />
                <Route exact path="/">
                    <Redirect to="/Welcome" />
                </Route>
                <Route exact path="/Search" component={ReactiveSearchComponent} />
                <Route exact path="/About" component={About} />
            </Switch>
        </div>
    );
};