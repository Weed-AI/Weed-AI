import React from 'react';
import { ControlElement, Resolve, composePaths } from '@jsonforms/core';
import { JsonFormsDispatch } from '@jsonforms/react';
import { schemaMatches, rankWith } from '@jsonforms/core';


interface Props {
  data: any;
  path: string;
  uischemas: any;
  schema: any;
  uischema: any;
  findUISchema: any;
}

export const fixedItemsTester = rankWith(
	5, schemaMatches((schema) => {return ((schema.minItems !== undefined) && (schema.minItems === schema.maxItems)); })
);


export const FixedItemsRenderer = ({ data, path, uischemas, schema, uischema, findUISchema } : Props) => {
    const controlElement = uischema as ControlElement;
    const resolvedSchema = Resolve.schema(schema, `${controlElement.scope}/items`);

    const range = (start : number, stop : number) => {
        var out = [];
        for (var i = start; i < stop; i++)
            out.push(i);
        return out;
    }

    return (
        <div>
        {
            range(0, schema.minItems).map(index => {
                //const uischema = findUISchema(uischemas, resolvedSchema, controlElement.scope, path);
                const childPath = composePaths(path, `${index}`);

                return (
                <JsonFormsDispatch
                    schema={resolvedSchema}
                    uischema={uischema}
                    path={childPath}
                    key={childPath}
                />
                );
            })
        }
        </div>
    );
};

export default FixedItemsRenderer;
