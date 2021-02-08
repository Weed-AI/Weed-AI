import React, { Component, useState } from 'react'
import { withTheme } from "react-jsonschema-form";
import { Theme as MuiTheme } from 'rjsf-material-ui';
import { withRouter } from 'react-router-dom';
import { agcontextSchema } from './schemas'
import './AgContextForm.css';
import Container from '@material-ui/core/Container';
import Box from '@material-ui/core/Box';
import UploadJsonButton from './Components/ui/UploadJsonButton';


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
              formData={this.props.formData}
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
        return (
            <Container maxWidth="sm">
                <Box boxShadow={3} px={2} py={1} my={2}>
                    <AgContextForm formData={this.state.formData} onChange={e => this.setState({formData: e.formData})} />
                </Box>
                <UploadJsonButton initialValue={this.state.formData} downloadName="agcontext" onClose={(value) => {this.setState({formData: value})}} />
            </Container>
        );
    }
}


export default AgContextForm;
export const Standalone = withRouter(StandaloneEditor);
