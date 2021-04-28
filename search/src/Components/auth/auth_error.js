import React from 'react';


const AuthError = (props) => {
    const { error } = props;
    return (
        <div>
            { error ? <p style={{color: 'red', margin: 0}}>{ error }</p> : ""}
        </div>
    )
}

export default AuthError;