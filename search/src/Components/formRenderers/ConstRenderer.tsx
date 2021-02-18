import React from 'react';
import { withJsonFormsControlProps } from '@jsonforms/react';
import { schemaMatches, rankWith } from '@jsonforms/core';

export const ConstRenderer = withJsonFormsControlProps(({schema, handleChange, path}) => {
  setTimeout((() => handleChange(path, schema['const'])), 10);
  return (<React.Fragment></React.Fragment>);
});

export const constTester = rankWith(
  10, //increase rank as needed
  schemaMatches((schema) => schema["const"])
);


export default ConstRenderer;
