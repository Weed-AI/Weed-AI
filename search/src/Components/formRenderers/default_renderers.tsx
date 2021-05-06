import { fixedItemsTester, FixedItemsRenderer } from './FixedItemsRenderer';
import { constTester, ConstRenderer } from './ConstRenderer';
import { oneOfTester, OneOfRenderer } from './OneOfRenderer';
import {
  materialCells,
  materialRenderers,
} from '@jsonforms/material-renderers';

const renderers = [
  ...materialRenderers,
  { tester: constTester, renderer: ConstRenderer },
  { tester: fixedItemsTester, renderer: FixedItemsRenderer },
  { tester: oneOfTester, renderer: OneOfRenderer },
];
export default renderers;
