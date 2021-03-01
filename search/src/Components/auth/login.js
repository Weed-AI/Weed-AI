import React from 'react';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField'
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import axios from 'axios';
import Cookies from 'js-cookie';


const useStyles = (theme) => ({
    paper: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
    },
    form: {
        width: '100%',
        marginTop: theme.spacing(1),
    },
    submit: {
        margin: theme.spacing(3, 0, 2),
    },
});

const baseURL = new URL(window.location.origin);

class LoginComponent extends React.Component {

    constructor() {
        super();
        this.state = {
            login_failure: false
        }
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(event) {
        event.preventDefault();
        const bodyFormData = new FormData();
        const data = new FormData(event.target);
        for (const [key, value] of data.entries()) {
            bodyFormData.append(key, value);
        }
        axios({
            method: 'post',
            url: baseURL + 'api/login/',
            mode: 'same-origin',
            data: bodyFormData,
            headers: {'Content-Type': 'multipart/form-data', 'X-CSRFToken': Cookies.get('csrftoken') }
        })
        .then((response) => {
            console.log(response);
            this.props.handleLogin();
            this.props.handleClose();
        })
        .catch((error) => {
            this.setState({login_failure: true})
            console.log(error);
        });
    }

    render() {
        const { classes } = this.props;
        return (
            <Container component="main" maxWidth="xs">
                <CssBaseline />
                <div className={classes.paper}>
                    <Typography component="h1" variant="h5">
                        Sign in
                    </Typography>
                    { this.state.login_failure ? <p style={{color: 'red'}}>Invalid username and credentials</p> : ""}
                    <form className={classes.form} noValidate onSubmit={this.handleSubmit} onChange={() => {this.setState({login_failure: false})}}>
                        <TextField
                            variant="outlined"
                            margin="normal"
                            required
                            fullWidth
                            id="username"
                            label="Username"
                            name="username"
                            autoComplete="username"
                            autoFocus
                        />
                        <TextField
                            variant="outlined"
                            margin="normal"
                            required
                            fullWidth
                            name="password"
                            label="Password"
                            type="password"
                            id="password"
                            autoComplete="current-password"
                        />
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            color="primary"
                            className={classes.submit}
                        >
                            Sign In
                        </Button>
                    </form>
                </div>
            </Container>
        );
    }
}

export default withStyles(useStyles)(LoginComponent);
