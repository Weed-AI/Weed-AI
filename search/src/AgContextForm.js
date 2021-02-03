import React, { Component } from 'react'
import { withRouter } from 'react-router-dom';
import agcontextSchema from './Schemas/AgContext.json'
import Container from '@material-ui/core/Container';
import Box from '@material-ui/core/Box';
import {
  materialCells,
  materialRenderers,
} from '@jsonforms/material-renderers';
import { JsonForms } from '@jsonforms/react';
import GrowthStageControl from './GrowthStageControl';
import growthStageControlTester from './growthStageControlTester';

const uischema = {
  "type": "Categorization",
  "elements": [
    {
      "type": "Category",
      "label": "The Crop",
      "elements": [
        {
          "type": "Control",
          "scope": "#/properties/crop_type"
        },
        {
          "type": "Control",
          "label": "BBCH Growth Stage",
          "scope": "#/properties/bbch_growth_range"
        },
        {
          "type": "Control",
          "scope": "#/properties/soil_colour"
        },
        {
          "type": "Control",
          "scope": "#/properties/surface_cover"
        },
        {
          "type": "Control",
          "scope": "#/properties/surface_coverage"
        },
        {
          "type": "HorizontalLayout",
          "elements": [
            {
              "type": "Control",
              "scope": "#/properties/location_datum"
            },
            {
              "type": "Control",
              "scope": "#/properties/location_lat"
            },
            {
              "type": "Control",
              "scope": "#/properties/location_long"
            }
          ]
        }
      ]
    },
    {
      "type": "Category",
      "label": "The Photography",
      "elements": [
        {
          "type": "Control",
          "scope": "#/properties/camera_make"
        },
        {
          "type": "Control",
          "scope": "#/properties/camera_lens"
        },
        {
          "type": "Control",
          "scope": "#/properties/camera_lens_focallength"
        },
        {
          "type": "Control",
          "scope": "#/properties/camera_height"
        },
        {
          "type": "Control",
          "scope": "#/properties/camera_angle"
        },
        {
          "type": "Control",
          "scope": "#/properties/camera_fov"
        },
        {
          "type": "Control",
          "scope": "#/properties/lighting"
        },
        {
          "type": "Control",
          "scope": "#/properties/photography_description"
        }
      ]
    },
    {
      "type": "Category",
      "label": "Other Details",
      "elements": [
        {
          "type": "Control",
          "scope": "#/properties/cropped_to_plant"
        },
        {
          "type": "Control",
          "scope": "#/properties/emr_channels"
        },
        {
          "type": "Control",
          "scope": "#/properties/weather_description"
        }
      ]
    }
  ]
};

const renderers = [
  ...materialRenderers,
  { tester: growthStageControlTester, renderer: GrowthStageControl },
];

class AgContextForm extends Component {
    constructor(props) {
        super(props);
        this.state = {formData: this.props.formData};
    }

    render() {
        const schema = agcontextSchema;

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
        this.state = {formData: this.props.formData || {crop_type: "oats"} }
    }
    render() {
        const toJSON = (payload) => JSON.stringify(payload, null, 2);
        const handleSaveToPC = (payload) => {
            const fileData = toJSON(payload.formData);
            const blob = new Blob([fileData], {type: "text/plain"});
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
