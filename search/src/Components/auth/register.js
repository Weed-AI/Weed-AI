import React from 'react'
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField'
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import axios from 'axios';
import Cookies from 'js-cookie'


const csrftoken = Cookies.get('csrftoken');

const useStyles = (theme) => ({
    paper: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
    },
    form: {
      width: '100%',
      marginTop: theme.spacing(3),
    },
    submit: {
      margin: theme.spacing(3, 0, 2),
    },
  });

const baseURL = new URL(window.location.origin);

class RegisterComponent extends React.Component {

    constructor() {
        super();
        this.state = {
            duplicate_username: false
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
            url: baseURL + 'api/register/',
            mode: 'same-origin',
            data: bodyFormData,
            headers: {'Content-Type': 'multipart/form-data', 'X-CSRFToken': csrftoken }
        })
        .then((response) => {
            console.log(response);
            this.props.handleClose();
        })
        .catch((error) => {
            this.setState({duplicate_username: true})
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
                Sign up
                </Typography>
                {this.state.duplicate_username ? <p style={{color: 'red'}}>This username already exists</p> : ""}
                <form className={classes.form} noValidate onSubmit={this.handleSubmit} id="register-form">
                <Grid container spacing={2}>
                    <Grid item xs={12} sm={12}>
                    <TextField
                        name="username"
                        variant="outlined"
                        required
                        fullWidth
                        id="username"
                        label="Username"
                        autoFocus
                        onChange={() => {this.setState({duplicate_username: false})}}
                    />
                    </Grid>
                    <Grid item xs={12}>
                    <TextField
                        variant="outlined"
                        required
                        fullWidth
                        id="email"
                        label="Email Address"
                        name="email"
                        autoComplete="email"
                    />
                    </Grid>
                    <Grid item xs={12}>
                    <TextField
                        variant="outlined"
                        required
                        fullWidth
                        name="password"
                        label="Password"
                        type="password"
                        id="password"
                        autoComplete="current-password"
                    />
                    </Grid>
                </Grid>
                <Button
                    type="submit"
                    fullWidth
                    variant="contained"
                    color="primary"
                    className={classes.submit}
                >
                    Sign Up
                </Button>
                </form>
            </div>
            </Container>
        );
    }  
}

export default withStyles(useStyles)(RegisterComponent);