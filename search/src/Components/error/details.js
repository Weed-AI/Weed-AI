import React from 'react';
import {jsonSchemaTransform} from './utils';
import ReactMarkdown from "react-markdown";


const JsonSchemaDetails = (props) => {
    const {details} = props
    const tfError = jsonSchemaTransform(details)
    const tfDisplay = Object.keys(tfError).map((path) => {
        return (
            <div>
                <p>{tfError[path].instances.length} {tfError[path].instances.length > 1 ? "errors": "error"} in the {path}</p>
                <ol>
                    {tfError[path].instances.map(error =>
                        <li key={error.path}>In {error.path}: {error.message}</li>
                    )}
                </ol>
                {tfError[path].description ? <p>Description of this field:</p> : ""}
                <ReactMarkdown source={tfError[path].description} />
                <br/>
            </div>
        )
    })
    return tfDisplay
}


const MissingImageDetails = (props) => {
    const {details} = props
    const listOfMissingImages = details.missingImages.map((image) => <li>{image}</li>)
    return <ul>{listOfMissingImages}</ul>
}


const ErrorDetails = (props) => {
    const {details} = props;
    return (
            details.error_type === "jsonschema"?
            <JsonSchemaDetails details={details}/>
            :
            details.error_type === "image"?
            <MissingImageDetails details={details}/>
            :
            typeof details === typeof ""?
            details
            :
            ""
        )
}

export default ErrorDetails;