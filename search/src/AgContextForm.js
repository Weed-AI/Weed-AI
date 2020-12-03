import React, { Component, useState } from 'react'
import { render } from "react-dom";
import Form, { withTheme } from "react-jsonschema-form";
import { Theme as MuiTheme } from 'rjsf-material-ui';
import { withRouter } from 'react-router-dom';
import MaterialJsonSchemaForm from 'react-jsonschema-form-material-ui'
// TODO: load schema from file
// For some reason loading the schema from file throw "unsupported field schema for field" errors 
// import { agcontextSchema } from './schemas'
import './AgContextForm.css';

class AgContextForm extends Component {
    render() {
        console.log("hello world");
        const schema = {
          "$id": "https://weedid.sydney.edu.au/schema/AgContext.json",
          "type": "object",
          "required": [
            "id",
            "crop_type",
            "bbch_descriptive_text",
            "bbch_code",
            "grains_descriptive_text",
            "soil_colour",
            "surface_cover",
            "surface_coverage",
            "weather_description",
            "location_lat",
            "location_long",
            "location_datum",
            "camera_make",
            "camera_lens",
            "camera_lens_focallength",
            "camera_height",
            "camera_angle",
            "camera_fov",
            "photography_description",
            "lighting",
            "cropped_to_plant"
          ],
          "properties": {
            "id": {
              "type": "number",
              "description": "A number identifying the AgContext."
            },
            "crop_type": {
              "type": "string",
              "enum": [
                "wheat",
                "barley",
                "oats",
                "triticale",
                "sorghum",
                "rice",
                "lupins",
                "chickpeas",
                "lentils",
                "field_peas",
                "faba_beans",
                "mung_beans",
                "canola",
                "mustard",
                "flax",
                "linseed",
                "safflower",
                "cotton",
                "carrots",
                "weed_only",
                "other"
              ],
              "description": "Crop type.\nOne of several strings describing the crop grown in the image."
            },
            "grains_descriptive_text": {
              "type": "string",
              "enum": [
                "emergence",
                "seedling",
                "tillering",
                "stem_elongation",
                "booting",
                "ear_emergence",
                "flowering",
                "milky_dough",
                "dough",
                "ripening",
                "na"
              ],
              "description": "Grains descriptive text.\nOne of ten possible strings describing the crop developmental stage.\nIf this AgContext is not in a cropping environment, use value \"na\"."
            },
            "bbch_descriptive_text": {
              "type": "string",
              "enum": [
                "germination",
                "sprouting",
                "bud development",
                "leaf development",
                "formation of side shoots",
                "tillering",
                "stem elongation",
                "rosette growth",
                "shoot development",
                "development of harvestable vegetative parts",
                "bolting",
                "inflorescence emergence",
                "heading",
                "flowering",
                "development of fruit",
                "ripening or maturity of fruit and seed",
                "senescence",
                "beginning of dormancy",
                "na"
              ],
              "description": "BBCH descriptive text.\nOne of several possible strings describing the stage of the crop, chosen from a list of possible terms used by the BBCH.\nIf this AgContext is not in a cropping environment, use value \"na\"."
            },
            "bbch_code": {
              "type": "string",
              "pattern": "^gs[1-9][0-9]$|^gs0[1-9]$|^na$",
              "description": "BBCG descriptive text.\nOne of several possible strings describing the stage of the crop, chosen from a list of codes used by the BBCH.\nIf this AgContext is not in a cropping environment, use value \"na\"."
            },
            "soil_colour": {
              "type": "string",
              "enum": [
                "not_visible",
                "black",
                "dark_brown",
                "brown",
                "red_brown",
                "dark_red",
                "yellow",
                "pale_yellow",
                "white",
                "grey",
                "variable"
              ],
              "description": "Soil colour.\nGeneral description of the soil colour."
            },
            "surface_cover": {
              "type": "string",
              "enum": [
                "cereal",
                "oilseed",
                "legume",
                "cotton",
                "black_plastic",
                "white_plastic",
                "woodchips",
                "other",
                "none"
              ],
              "description": "Surface cover type.\nOne of several strings describing the background cover (including stubble of previous crops) that is behind any plants in the images."
            },
            "surface_coverage": {
              "type": "string",
              "enum": [
                "0-25",
                "25-50",
                "50-75",
                "75-100",
                "na"
              ],
              "description": "Percent of coverage in image.\nApproximate measurement of the percent of the soil in the image that is covered by the surface cover."
            },
            "weather_description": {
              "type": "string",
              "description": "Weather conditions in images.\nFree text description of approximate weather conditions during the image capture session."
            },
            "location_lat": {
              "type": "number",
              "minimum": -90,
              "maximum": 90,
              "description": "Latitude in decimal degrees.\nApproximate latitude location of the AgContext, in decimal degrees."
            },
            "location_long": {
              "type": "number",
              "minimum": 0,
              "maximum": 180,
              "description": "Longitude in decimal degrees.\nApproximate longitude location of the AgContext, in decimal degrees."
            },
            "location_datum": {
              "type": "number",
              "enum": [
                4326
              ],
              "description": "EPSG code of spatial coordinates.\nEuropean Petroleum Survey Group code that identifies the projection used for the spatial coordinates."
            },
            "camera_make": {
              "type": "string",
              "description": "Type of camera.\nFree text denoting the model/make of camera used for this AgContext."
            },
            "camera_lens": {
              "type": "string",
              "description": "Type of lens.\nFree text denoting the model/make of lens used for this AgContext."
            },
            "camera_lens_focallength": {
              "type": "number",
              "minimum": 0,
              "description": "Focal length of the lens mounted to the camera.\nThe focal length of the lens being used in this AgContext, measured in millimeters."
            },
            "camera_height": {
              "type": "number",
              "minimum": 0,
              "description": "Height of camera.\nAn number representing the height of the camera, measured in millimeters ."
            },
            "camera_angle": {
              "type": "number",
              "description": "Angle of camera. A number representing the angle at which the camera is positioned, in degrees. A camera facing straight down would be 90. A camera facing forward would be 0."
            },
            "camera_fov": {
              "anyOf": [
                {
                  "type": "number",
                  "minimum": 1,
                  "maximum": 180
                },
                {
                  "type": "string",
                  "enum": [
                    "variable"
                  ]
                }
              ],
              "description": "Field of view for camera.\nA number representing the angle captured by the camera across the diagonal of an image, measured in degrees.\nIf this is not fixed within the AgContext, use value \"variable\"."
            },
            "photography_description": {
              "type": "string",
              "description": "Description of photography.\nFree text description of salient aspects of camera, mount and lighting."
            },
            "lighting": {
              "type": "string",
              "enum": [
                "artificial",
                "natural"
              ],
              "description": "Description of the lighting in  the images.\nTwo possible strings describing the lighting in the images."
            },
            "cropped_to_plant": {
              "type": "boolean",
              "description": "Has the image been cropped to the plant?\nA boolean indicating if the image has been cropped to the plant."
            },
            "emr_channels": {
              "type": "string",
              "description": "EMR channels captured in images.\nA string describing the electromagnetic radiation channels captured.\nIn most cases, this will be \"visual\"."
            }
          }
        };


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

        const out = (
            <Form
              schema={schema}
              uiSchema={uiSchema}
              onSubmit={handleSaveToPC}
              //formData={formData}
              //onChange={e => setFormData(e.formData)}
            />
        );
        console.log(out);
        return out;
    }
}

export default withRouter(AgContextForm);
