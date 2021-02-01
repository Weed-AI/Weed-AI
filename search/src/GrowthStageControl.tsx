import { withJsonFormsControlProps } from '@jsonforms/react';
import React from 'react';
import Slider from '@material-ui/core/Slider';
import Tooltip from '@material-ui/core/Tooltip';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core/styles';


function ValueLabelComponent(props: any) {
  const { children, open, value } = props;

  return (
    <Tooltip open={open} enterTouchDelay={0} placement="top" title={value}>
      {children}
    </Tooltip>
  );
}


interface GrowthStageControlProps {
  data: any;
  handleChange(path: string, value: any): void;
  path: string;
}

const GrowthStageSlider = withStyles(
  {
    mark: {
      backgroundColor: '#000',
      height: 8,
      width: 8,
      marginLeft: -4,
      marginTop: -3,
    },
  })(Slider);

const GrowthStageControl = ({ data, handleChange, path }: GrowthStageControlProps) => {
  const [value, setValue] = React.useState([0, 99]);

;
  const fineLabels : { [key: number]: string; } = {
     0: "Dry seed (caryopsis)",
     1: "Beginning of seed imbibition",
     3: "Seed imbibition complete",
     5: "Radicle emerged from caryopsis",
     6: "Radicle elongated, root hairs and/or side roots visible",
     7: "Coleoptile emerged from caryopsis",
     9: "Emergence: coleoptile penetrates soil surface (cracking stage)",
    10: "First leaf through coleoptile",
    11: "First leaf unfolded",
    12: "2 leaves unfolded",
    13: "3 leaves unfolded",
    14: "4 leaves unfolded",
    15: "5 leaves unfolded",
    16: "6 leaves unfolded",
    17: "7 leaves unfolded",
    18: "8 leaves unfolded",
    19: "9 or more leaves unfolded",
    20: "No tillers",
    21: "Beginning of tillering: first tiller detectable",
    22: "2 tillers detectable",
    23: "3 tillers detectable",
    24: "4 tillers detectable",
    25: "5 tillers detectable",
    26: "6 tillers detectable",
    27: "7 tillers detectable",
    28: "8 tillers detectable",
    29: "End of tillering. Maximum no. of tillers detectable",
    30: "Beginning of stem elongation: pseudostem and tillers erect, first internode begins to elongate, top of inflorescence at least 1 cm above tillering node",
    31: "First node at least 1 cm above tillering node",
    32: "Node 2 at least 2 cm above node 1",
    33: "Node 3 at least 2 cm above node 2",
    34: "Node 4 at least 2 cm above previous node",
    35: "Node 5 at least 2 cm above previous node",
    36: "Node 6 at least 2 cm above previous node",
    37: "Flag leaf just visible, still rolled",
    39: "Flag leaf stage: flag leaf fully unrolled, ligule just visible",
    41: "Early boot stage: flag leaf sheath extending",
    43: "Mid boot stage: flag leaf sheath just visibly swollen",
    45: "Late boot stage: flag leaf sheath swollen",
    47: "Flag leaf sheath opening",
    49: "First awns visible (in awned forms only)",
    51: "Beginning of heading: tip of inflorescence emerged from sheath, first spikelet just visible",
    52: "20% of inflorescence emerged",
    53: "30% of inflorescence emerged",
    54: "40% of inflorescence emerged",
    55: "Middle of heading: half of inflorescence emerged",
    56: "60% of inflorescence emerged",
    57: "70% of inflorescence emerged",
    58: "80% of inflorescence emerged",
    59: "End of heading: inflorescence fully emerged",
    61: "Beginning of flowering: first anthers visible",
    65: "Full flowering: 50% of anthers mature",
    69: "End of flowering: all spikelets have completed flowering but some dehydrated anthers may remain",
    71: "Watery ripe: first grains have reached half their final size",
    73: "Early milk",
    75: "Medium milk: grain content milky, grains reached final size, still green",
    77: "Late milk",
    83: "Early dough",
    85: "Soft dough: grain content soft but dry. Fingernail impression not held",
    87: "Hard dough: grain content solid. Fingernail impression held",
    89: "Fully ripe: grain hard, difficult to divide with thumbnail",
    92: "Over-ripe: grain very hard, cannot be dented by thumbnail",
    93: "Grains loosening in day-time",
    97: "Plant dead and collapsing",
    99: "Harvested product",
  }
  const grainStageLabels = Array(100);
  [
    {label: "Emergence", lo: 0, hi: 9},
    {label: "Seedling", lo: 10, hi: 19},
    {label: "Tillering", lo: 20, hi: 29},
    {label: "Stem Elongation", lo: 30, hi: 39},
    {label: "Booting", lo: 40, hi: 49},
    {label: "Ear emergence", lo: 50, hi: 59},
    {label: "Flowering", lo: 60, hi: 69},
    {label: "Milky Dough", lo: 70, hi: 79},
    {label: "Dough", lo: 80, hi: 89},
    {label: "Ripening", lo: 90, hi: 99},
  ].forEach(({label, lo, hi}) => {
    for (var i = lo; i <= hi; i++) {
      grainStageLabels[i] = label;
    }
  });
  const bbchStageLabels = Array(100);
  [
    {label: "Germination, sprouting, bud development", lo: 0, hi: 9},
    {label: "Leaf development", lo: 10, hi: 19},
    {label: "Formation of side shoots, tillering", lo: 20, hi: 29},
    {label: "Stem elongation, rosette growth, shoot development", lo: 30, hi: 39},
    {label: "Development of harvestable vegetative parts, bolting", lo: 40, hi: 49},
    {label: "Inflorescence emergence, heading", lo: 50, hi: 59},
    {label: "Flowering", lo: 60, hi: 69},
    {label: "Development of fruit", lo: 70, hi: 79},
    {label: "Ripening or maturity of fruit and seed", lo: 80, hi: 89},
    {label: "Senescence, beginning of dormancy", lo: 90, hi: 99},
  ].forEach(({label, lo, hi}) => {
    for (var i = lo; i <= hi; i++) {
      bbchStageLabels[i] = label;
    }
  });
  const formatValueLabel = (value: number) => {
    var fineLabel = fineLabels[value];
    if (!fineLabel)
      fineLabel = "[No fine-grained BBCH code]";
    return (
      <ul>
      <li>BBCH GS{value.toString().padStart(2, "0")}: {fineLabel}</li>
      <li>Coarse Stage {value.toString().substring(0, 1)}: {bbchStageLabels[value]}</li>
      <li>Grain growth: {grainStageLabels[value]}</li>
      </ul>
      );
  }
  const formatValueAria = (value: number) => {
    return "BBCH GS" + value.toString().padStart(2, "0") + ": " + fineLabels[value];
  }
  const sliderHandleChange = (event : any, newValue : any) => {
    setValue(newValue);
    var exportValue = newValue;
    if (newValue[0] === 0 && newValue[1] === 99) {
      exportValue = null;
    }
    handleChange(path, exportValue);
  };


  return (
    <div>
    <Typography id="range-slider" gutterBottom>
        Crop Growth Stage Range
    </Typography>
    <GrowthStageSlider
        value={value}
        min={0}
        marks={[{value: 0}, {value: 10}, {value: 20}, {value: 30}, {value: 40}, {value: 50}, {value: 60}, {value: 70}, {value: 80}, {value: 90}]}
        step={1}
        max={99}
        onChange={sliderHandleChange}
        valueLabelDisplay="auto"
        aria-labelledby="range-slider"
        getAriaValueText={formatValueAria}
        valueLabelFormat={formatValueLabel}
        ValueLabelComponent={ValueLabelComponent}
    />
    </div>
  );
};

export default withJsonFormsControlProps(GrowthStageControl);
