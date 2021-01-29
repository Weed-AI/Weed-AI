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
    constructor(props) {
        super(props);
        this.state = {formData: this.props.formData};
    }

    render() {
        const schema = agcontextSchema;

        const uiSchema = {
          title: "AgContext Entry Form"
        };

        return (
            <Form
              schema={schema}
              uiSchema={uiSchema}
              formData={this.state.formData}
              onChange={e => {
                  this.setState({formData: e.formData});
                  if (this.props.onChange) {
                      this.props.onChange(e);
                  }
              }}
              children={true}  // hides submit
            />
        );
    }
}


class StandaloneEditor extends Component {
    constructor(props) {
        super(props);
        this.state = {formData: this.props.formData || {crop_type: "oats"} }
    }
    render() {

        const onSubmit = ({formData}, e) => console.log("Data submitted", formData);

        const toJSON = (payload) => JSON.stringify(payload, null, 2);
        const handleSaveToPC = (payload) => {
            const fileData = toJSON(payload);
            const blob = new Blob([fileData], {type: "application/json"});
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.download = `AgContext.json`;
            link.href = url;
            link.click();
        }

        return (
            <Container maxWidth="sm">
                <Box boxShadow={3} px={2} py={1} my={2}>
                    <AgContextForm formData={this.state.formData} onChange={e => this.setState({formData: e.formData})} />
                </Box>
                <Box boxShadow={3} px={2} py={1} my={2}>
                    <label>JSON representation of AgContext</label>
                    <textarea style={{width: "100%", height: "5em"}} value={toJSON(this.state.formData)} / >
                    <button onClick={e => handleSaveToPC(this.state.formData)}>Download</button>
                </Box>
            </Container>
        );
    }
}


export default AgContextForm;
export const Standalone = withRouter(StandaloneEditor);
