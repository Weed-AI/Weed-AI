import React from 'react';
import {jsonSchemaTransform} from './utils';
import Markdown from "../../Common/Markdown";
import { makeStyles } from '@material-ui/core/styles';
import Accordion from '@material-ui/core/Accordion';
import AccordionSummary from '@material-ui/core/AccordionSummary';
import AccordionDetails from '@material-ui/core/AccordionDetails';
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
import Typography from '@material-ui/core/Typography';


const useStyles = makeStyles((theme) => ({
    root: {
      width: '100%',
    },
    heading: {
      fontSize: theme.typography.pxToRem(15),
      fontWeight: theme.typography.fontWeightRegular,
    },
  }));


const JsonSchemaDetails = (props) => {
    const {details} = props
    const classes = useStyles();
    const tfError = jsonSchemaTransform(details)
    const tfDisplay = Object.keys(tfError).map((path) => {
        return (
            <div className={classes.root}>
                <Accordion>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                        <Typography className={classes.heading}>
                            {tfError[path].instances.length}
                            <span> </span>
                            {tfError[path].instances.length > 1 ? "errors": "error"} in the {path}
                        </Typography>
                    </AccordionSummary>
                    <AccordionDetails style={{display: 'block'}}>
                        <ol>
                            {tfError[path].instances.map(error =>
                                <li key={error.path}>In {error.path}: {error.message}</li>
                            )}
                        </ol>
                        {tfError[path].description ? <p>Description of this field:</p> : ""}
                        <Markdown source={tfError[path].description} />
                    </AccordionDetails>
                </Accordion>
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
