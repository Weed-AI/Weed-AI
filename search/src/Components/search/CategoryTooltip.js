import axios from 'axios';
import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Link from '@material-ui/core/Link';
import Tooltip from '@material-ui/core/Tooltip';
import wssa_vernacular_names from '../../Data/wssa_vernacular_names.json';

const useStyles = makeStyles((theme) => ({
  taxonomy: {
    "& > li:first-child": {
      listStyleType: "none",
    },
    "& > li": {
      listStyleType: "\">  \"",
    },
    paddingLeft: "2em",
  },
  rank: {
    fontVariant: "small-caps",
    fontSize: ".9em",
    marginLeft: ".4em",
  },
  heading: {
    width: "100%",
    display: "block",
    textAlign: "center",
    borderBottom: "#ffffff33 solid thin",
  },
  vernacular: {
    marginTop: theme.spacing(1),
  },
  scientificName: {
    fontStyle: "italic",
    color: "#ADD8E6",
  }
}));

export const CategoryCard = (props) => {
  const { categoryName, canonicalName, vernacularName, rank } = props;
  const classes = useStyles()
  const hierarchy = ["kingdom", "phylum", "order", "family", "genus", "species"].map(hRank => ({
    name: props[hRank],
    key: props[hRank + "Key"],
    rank: hRank,
  })).filter(entry => entry.name !== undefined);
  if (hierarchy.length && hierarchy[hierarchy.length - 1].name !== canonicalName) {
    hierarchy.push({
      "name": canonicalName,
      "key": props.key,
      "rank": rank.toLowerCase()
    });
  }
  // Workaround for anomalies in GBIF vernacular names: use WSSA names
  const updatedVernacularName = wssa_vernacular_names[canonicalName.toLowerCase()] || vernacularName;
  return (
    <React.Fragment>
    <Typography variant="body1" className={classes.heading}>{categoryName}</Typography>
    { updatedVernacularName ? <Typography variant="body2" className={classes.vernacular}>{updatedVernacularName}</Typography> : []}
    { canonicalName ?
      <ul className={classes.taxonomy}>
         {hierarchy.map(entry =>
           <li key={entry.rank}>
             <Link target="_blank" rel="noopener" href={"https://www.gbif.org/species/" + entry.key} variant="caption" display="inline" className={classes.scientificName}>{entry.name}</Link>
             <Typography className={classes.rank} variant="caption" display="inline"> {entry.rank}</Typography>
           </li>
         )}
      </ul>
    : [] }
    </React.Fragment>
  )
};

const gbifPromisesCache = {
  "UNSPECIFIED": {then: () => {}}
};

const CategoryTooltip = ({ categoryName, children }) => {
  const [gbifData, setGbifData] = React.useState({});
  const species = categoryName.match(/^([^:]*): (.*)/)[2];
  React.useEffect(() => {
    if (species === undefined)
      return;
    gbifPromisesCache[categoryName] = (
      gbifPromisesCache[categoryName] === undefined
      ? (axios.get("https://api.gbif.org/v1/species?name=" + encodeURIComponent(species) + "&datasetKey=d7dddbf4-2cf0-4f39-9b2a-bb099caae36c&taxonomicStatus=ACCEPTED"))
      : gbifPromisesCache[categoryName]);
    gbifPromisesCache[categoryName].then(response => {
      if (response.data && response.data.results) {
        setGbifData(response.data.results.filter(entry => entry.taxonomicStatus == "ACCEPTED")[0]);
      }
    })
  });
  return <Tooltip
      interactive
      title={<CategoryCard categoryName={categoryName} {...gbifData} />}
    >
      {children}
    </Tooltip>;
}

export default CategoryTooltip;
