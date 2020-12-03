import React, { Component, useState } from 'react'
import { render } from "react-dom";
import Form, { withTheme } from "react-jsonschema-form";
import { Theme as MuiTheme } from 'rjsf-material-ui';
import { withRouter } from 'react-router-dom';
import MaterialJsonSchemaForm from 'react-jsonschema-form-material-ui'
// TODO: load schema from file
// For some reason loading the schema from file throw "unsupported field schema for field" errors 
import { agcontextSchema } from './schemas'
import './AgContextForm.css';

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

export default withRouter(AgContextForm);
