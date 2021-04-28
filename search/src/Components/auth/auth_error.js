import React from 'react';
import { withStyles } from '@material-ui/core/styles';


const styles = () => ({
    error: {
        color: 'red',
        margin: 0
    }
})

const AuthError = withStyles(styles)((props) => {
    const { classes, error } = props;
    return (
        <div>
            { error ? <p className={classes.error}>{ error }</p> : ""}
        </div>
    )
})

export default AuthError;