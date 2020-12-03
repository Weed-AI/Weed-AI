import React, { Component, useState } from 'react'
import { render } from "react-dom";
import { withTheme } from "react-jsonschema-form";
import { Theme as MuiTheme } from 'rjsf-material-ui';
import { withRouter } from 'react-router-dom';
import { agcontextSchema } from './schemas'
import './AgContextForm.css';
import Container from '@material-ui/core/Container';
import Box from '@material-ui/core/Box';
import { shadows } from '@material-ui/system';


const Form = withTheme(MuiTheme);

class AgContextForm extends Component {
    render() {
        const schema = agcontextSchema;

        const uiSchema = {
          title: "AgContext Entry Form"
        };

        const log = type => console.log.bind(console, type);

        const onSubmit = ({formData}, e) => console.log("Data submitted", formData);

        const handleSaveToPC = (payload) => {
            const fileData = JSON.stringify(payload.formData);
            const blob = new Blob([fileData], {type: "text/plain"});
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.download = `AgContext.json`;
            link.href = url;
            link.click();
        }

        return (
            <Form
              schema={schema}
              uiSchema={uiSchema}
              onSubmit={handleSaveToPC}
              //formData={formData}
              //onChange={e => setFormData(e.formData)}
            />
        );
    }
}


class StandaloneEditor extends Component {
    render() {
        return (
///            <div style={{maxWidth: "600px", margin: "2em auto", border: "thin" }}>
            <Container maxWidth="sm">
                <Box boxShadow={3} px={2}>
                    <AgContextForm />
                </Box>
            </Container>
///            </div>
        );
    }
}


export default AgContextForm;
export const Standalone = withRouter(StandaloneEditor);
