import React from 'react';
import { ControlElement, Resolve } from '@jsonforms/core';
import { JsonFormsDispatch } from '@jsonforms/react';
import { MaterialOneOfRenderer } from '@jsonforms/material-renderers';
import { schemaMatches, rankWith } from '@jsonforms/core';
import { isOneOfControl } from '@jsonforms/core';
import { FormControl, InputLabel, FormHelperText } from '@material-ui/core';


interface Props {
  data: any;
  path: string;
  uischemas: any;
  schema: any;
  uischema: any;
  findUISchema: any;
  renderers: any;
}

export const oneOfTester = rankWith(50, isOneOfControl);


export const OneOfRenderer = (props : Props) => {
    const controlElement = props.uischema as ControlElement;
    const resolvedSchema = Resolve.schema(props.schema, `${controlElement.scope}`);
    const [ showDesc, setShowDesc ] = React.useState(false);
    return (
        <div style={{paddingTop: "1em"}} onFocus={() => setShowDesc(true)} onBlur={() => setShowDesc(false)}>
            <InputLabel>{resolvedSchema.title}</InputLabel>
            <div style={{ marginLeft: "1em" }}>
              <MaterialOneOfRenderer
                  {...props}
              />
            </div>
            { showDesc && resolvedSchema.description
              ? <FormHelperText>{resolvedSchema.description}</FormHelperText>
              : []
            }
        </div>
    );
};

export default OneOfRenderer;
