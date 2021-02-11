import React, { Component } from 'react'
import { withRouter } from 'react-router-dom';
import schema from './Schemas/Metadata.json'
import Container from '@material-ui/core/Container';
import Box from '@material-ui/core/Box';
import {
  materialCells,
  materialRenderers,
} from '@jsonforms/material-renderers';
import { JsonForms } from '@jsonforms/react';

const uischema = {
    "type": "Categorization",
    "elements": [
        {
            "type": "Category",
            "label": "Basics",
            "elements": [
                {
                    "type": "Control",
                    "scope": "#/properties/name"
                },
                {
                    "type": "Control",
                    "scope": "#/properties/creator"
                },
                {
                    "type": "Control",
                    "scope": "#/properties/description",
                    "options": {"multi": true}
                },
                {
                    "type": "Control",
                    "scope": "#/properties/datePublished"
                },
                {
                    "type": "Control",
                    "scope": "#/properties/license"
                },
            ]
        },
        {
            "type": "Category",
            "label": "Referencing",
            "elements": [
                {
                    "type": "Control",
                    "scope": "#/properties/identifier"
                },
                {
                    "type": "Control",
                    "scope": "#/properties/citation",
                    "options": {"multi": true}
                },
                {
                    "type": "Control",
                    "scope": "#/properties/sameAs"
                },
            ],
        },
        {
            "type": "Category",
            "label": "Extra",
            "elements": [
                {
                    "type": "Control",
                    "scope": "#/properties/funder"
                },
            ]
        }
    ]
};

const renderers = [
  ...materialRenderers
];

// TODO: refactor boilerplate wrt AgContextForm code
export const toJSON = (payload) => JSON.stringify(payload, null, 2);
export const handleSaveToPC = (payload) => {
    const fileData = toJSON(payload);
    const blob = new Blob([fileData], {type: "application/json"});
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.download = `Metadata.json`;
    link.href = url;
    link.click();
}

class MetadataForm extends Component {
    constructor(props) {
        super(props);
        this.state = {formData: this.props.formData};
    }

    render() {
        return (
            <JsonForms
              schema={schema}
              uischema={uischema}
              data={this.state.formData}
              renderers={renderers}
              cells={materialCells}
              onChange={e => {
                  this.setState({formData: e.data});
                  if (this.props.onChange) {
                      e.formData = e.data;
                      this.props.onChange(e);
                  }
              }}
            />
        );
    }
}


class StandaloneEditor extends Component {
    constructor(props) {
        super(props);
        this.state = {formData: this.props.formData || {} }
    }
    render() {
        return (
            <Container maxWidth="sm">
                <h2>Dataset Metadata</h2>
                <Box boxShadow={3} px={2} py={1} my={2}>
                    <MetadataForm formData={this.state.formData} onChange={e => this.setState({formData: e.formData})} />
                </Box>
                <Box boxShadow={3} px={2} py={1} my={2}>
                    <label>JSON representation of Metadata</label>
                    <textarea readOnly={true} style={{width: "100%", height: "5em"}} value={toJSON(this.state.formData)} / >
                    <button onClick={e => handleSaveToPC(this.state.formData)}>Download</button>
                </Box>
            </Container>
        );
    }
}


export default MetadataForm;
export const Standalone = withRouter(StandaloneEditor);