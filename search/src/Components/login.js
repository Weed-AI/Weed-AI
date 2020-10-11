import React from 'react';
import {Link} from 'react-router-dom';

function LoginComponent() {
    return (
        <div>
            <h1>Login Page</h1>
            <button>
                <Link to="/register" style={{textDecoration: "none"}}>
                    Sign up
                </Link>
            </button>
        </div>
    )
}

export default LoginComponent;