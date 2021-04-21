import React from 'react';
import {jsonSchemaTransform} from './utils';


const JsonSchemaDetails = (props) => {
    const {details} = props
    const tfError = jsonSchemaTransform(details)
    const tfDisplay = Object.keys(tfError).map((path) => {
        return (
            <div>
                <p>{tfError[path].instances.length} {tfError[path].instances.length > 1 ? "errors": "error"} in the {path}</p>
                {tfError[path].instances.map((error) => <p>{error.message} @ {error.path}</p>)}
                <p>Description:</p>
                <p>{tfError[path].description}</p>
                <br/>
            </div>
        )
    })
    return tfDisplay
}

const ErrorDetails = (props) => {
    const {details} = props;
    return (
            details.error_type === "jsonschema"
            ?
            <JsonSchemaDetails details={details}/>
            :
            typeof details === typeof ""
            ?
            details
            :
            ""
        )
}

export default ErrorDetails;