import React, {Component} from 'react';
import { Helmet } from "react-helmet";
import { withStyles } from '@material-ui/core/styles';
import Accordion from '@material-ui/core/Accordion';
import AccordionSummary from '@material-ui/core/AccordionSummary';
import AccordionDetails from '@material-ui/core/AccordionDetails';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import LinkIcon from '@material-ui/icons/Link';
import { Chip } from '@material-ui/core';
import { Button } from '@material-ui/core';
import Grid from '@material-ui/core/Grid';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import axios from 'axios';
import ListIcon from '@material-ui/icons/List';
import PhotoIcon from '@material-ui/icons/Photo';
import DownloadIcon from '@material-ui/icons/CloudDownload';
import IconButton from '@material-ui/core/IconButton';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import { makeStyles } from "@material-ui/core/styles";
import Cookies from 'js-cookie'
import ReactMarkdown from "react-markdown";
import {
    ReactiveComponent,
} from '@appbaseio/reactivesearch';
import SearchBase from '../search/SearchBase';
import ResultsList from '../search/ResultsList';
import agcontextSchema from '../../Schemas/AgContext.json'


const DESCRIPTION_BOILERPLATE = "\n\nEvery dataset in Weed-AI includes imagery of crops or pasture with weeds annotated, and is available in an MS-COCO derived format with standardised agricultural metadata."

export const useStyles = (theme) => ({
  root: {
    flexGrow: 1,
    margin: theme.spacing(10)
  },
  heading: {
    fontSize: theme.typography.pxToRem(20),
    fontWeight: theme.typography.fontWeightBold,
    color: 'white'
  },
  header: {
    backgroundColor: '#4490db',
    borderRadius: '4px'
  },
  summary: {
  },
  download: {
    fontSize: '1.2rem',
    backgroundColor: 'orange',
    color: 'black',
    marginBottom: "1rem",
    paddingTop: "1rem",
    paddingBottom: "1rem",
  },
  attribution: {
    width: "100%",
    "& dl": {
    },
    "& dl > dd": {
      margin: ".5em 0 1em 2em",
    },
  },
  topMatter: {
    marginBottom: "1em",
  },
  identifierList: {
    display: 'flex',
    flexWrap: 'wrap',
    listStyle: 'none',
    padding: 0,
    paddingTop: theme.spacing(0.5),
    margin: 0,
  },
  identifierChip: {
    margin: theme.spacing(0.5),
    marginLeft: 0,
    overflow: "ellipsis",
    maxWidth: "30em",
    "&:hover": {
      maxWidth: "none",
    },
  },
});

const baseURL = new URL(window.location.origin);


const useCardStyles = makeStyles({
  root: {
    minWidth: 175,
    margin: "4px",
    "&:hover, &:active": {
      "& $description": {
        maxHeight: "20em",
        textOverflow: "initial",
        overflow: "visible",
        whiteSpace: "normal",
        position: "relative",
        maxWidth: "20em"
      },
    },
  },
  title: {
    fontSize: 14,
  },
  value: {
    fontWeight: "140%",
    fontSize: 26,
    marginBottom: 12,
  },
  description: {
    maxWidth: 175,
    fontSize: ".8em",
    textOverflow: "ellipsis",
    overflow: "hidden",
    whiteSpace: "nowrap",
    maxHeight: "1.5em",
  },
});

const AgFieldCard = ({ title, value, description }) => {
  const classes = useCardStyles();
  return (
    <Card className={classes.root}>
      <CardContent>
        <Typography
          className={classes.title}
          component="h4"
          color="textSecondary"
          gutterBottom
        >
          {title}
        </Typography>
        <Typography className={classes.value}>{value}</Typography>
        <Typography className={classes.description} variant="body2" component="p">
          {description}
        </Typography>
      </CardContent>
    </Card>
  );
}

const useFieldListStyles = makeStyles({
  details: {
    flexWrap: "wrap",
  },
});

const AgContextFieldList = (props) => {
    const classes = useFieldListStyles();
    const {title, agcontext, fields, MyAccordionSummary, ...accordionProps} = props;
    const addUnit = (unit) => (val) => (typeof val == "number" ? val + unit : val)
    const formatters = {
      bbch_growth_range: (val) => (val["min"] !== undefined ? val["min"] + " to " + val["max"] : val),
      location: (val) => ((val.lat < 0 ? val.lat : "+" + val.lat) + ',' + (val.lon < 0 ? val.lon : "+" + val.lon)),
      camera_height: addUnit("mm"),
      camera_lens_focallength: addUnit("mm"),
      camera_angle: addUnit("°"),
      surface_coverage: (val) => (val.includes("-") ? val + "%" : val),
      cropped_to_plant: (val) => (val ? "cropped" : "uncropped"),
    }
    const format = (key, val) => (
      formatters.hasOwnProperty(key)
      ? formatters[key](val)
      : typeof val === "boolean" ? val.toString()
      : typeof val === "string" ? val.replace("_", " ") : val
    );
    const localAgcontext = {...agcontext}
    localAgcontext['location'] = {'lat': localAgcontext.location_lat, 'lon': localAgcontext.location_long};
    const schemas = Object.fromEntries(
      fields
      .filter(key => localAgcontext[key])
      .map(key =>
        [key,
          agcontextSchema.properties[key] ||
          (key == 'location'? {description: "Approximate location of photography, in decimal degrees (WGS84)"} : {})]
      )
    );
    const data = Object.keys(schemas).map(key => ({
      key: key,
      title: schemas[key].title || snakeToText(key),
      value: format(key, localAgcontext[key]),
      description: schemas[key].description,
    }))
    return (
      <Accordion {...accordionProps}>
        <MyAccordionSummary>{title}</MyAccordionSummary>
        <AccordionDetails className={classes.details}>
            {data.map(field => {
              return <AgFieldCard
                key={field.key}
                title={field.title}
                value={field.value}
                description={field.description}
              />
            })}
        </AccordionDetails>
      </Accordion>
    );
}

const AgContextDetails = (props) => {
    const {metadata, agcontext, ordinal, nContexts, MyAccordionSummary} = props;
    const tableFields = {"image_count": "# Images", "segmentation_count": "# Segments", "bounding_box_count": "# Bounding Boxes"}
    return (
      <article>
        {nContexts > 1 ? <h2>Agricultural Context {ordinal} of {nContexts}</h2> : ""}
        <Accordion defaultExpanded="true">
          <MyAccordionSummary>Sample of {agcontext.n_images} Images</MyAccordionSummary>
          <AccordionDetails>
            <SearchBase>
              <ReactiveComponent
                componentId="dataset_filter"
                customQuery={props => ({
                  query: {
                    term: {
                      "dataset_name.keyword": metadata.name,
                    }
                  }
                })}
              />
              <ResultsList
                  listProps={{
                    pagination: false,
                    infiniteScroll: false,
                    size: 4,
                    react: {and: ["dataset_filter"]},
                    showResultStats: false,
                    sortOptions: null,
                  }}
                  cardProps={{
                    linkToDataset: false,
                  }}
                  setOGImage={true}
              />
            </SearchBase>
          </AccordionDetails>
        </Accordion>
        <Accordion defaultExpanded='true'>
          <MyAccordionSummary>Annotation Statistics</MyAccordionSummary>
          <AccordionDetails>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Category</TableCell>
                    {Object.keys(tableFields).map((field) => <TableCell key={field}>{tableFields[field]}</TableCell>)}
                  </TableRow>
                </TableHead>
                <TableBody>
                  {Object.keys(agcontext.category_statistics).map((catName) =>
                    <TableRow key={catName}>
                      <TableCell>{catName}</TableCell>
                      {Object.keys(tableFields).map((field) => <TableCell key={field}>{agcontext.category_statistics[catName][field]}</TableCell>)}
                    </TableRow>
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </AccordionDetails>
        </Accordion>
        <AgContextFieldList MyAccordionSummary={MyAccordionSummary} agcontext={agcontext} title="The Crop" fields={["crop_type", "bbch_growth_range", "soil_colour", "surface_cover", "surface_coverage", "location"]} />
        <AgContextFieldList MyAccordionSummary={MyAccordionSummary} agcontext={agcontext} title="The Photography" fields={["camera_make", "camera_lens", "camera_lens_focallength", "camera_height", "camera_angle", "camera_fov", "ground_speed", "lighting", "photography_description"]} />
        <AgContextFieldList MyAccordionSummary={MyAccordionSummary} agcontext={agcontext} title="Other Details" fields={["cropped_to_plant", "emr_channels", "weather_description"]} />
      </article>
    );
}

const listToWords = l => l.map((x, i) => [i == 0 ? "" : i == l.length - 1 ? (i > 1 ? "," : "") + " and " : ", ", x]);

export const DatasetSummary = (props) => {
    const {metadata, agcontexts, classes, rootURL, upload_id} = props;
    const linkedEntity = (ent) => {
      if (ent.sameAs)
        return (<a href={ent.sameAs}>{ent.name}</a>);
      return ent.name;
    }

    const MyAccordionSummary = ({ children }) => (
      <AccordionSummary
        expandIcon={<ExpandMoreIcon />}
        aria-controls="panel1a-content"
        id="panel1a-header"
        className={classes.header}
      >
        <Typography className={classes.heading}>{children}</Typography>
      </AccordionSummary>
    );

    const getFirstLine = (s) => (s.match(/[^\n.]*/)[0]);
    const displayMeta = {...metadata}
    const yearPublished = (displayMeta.datePublished || "????").substr(0, 4);
    displayMeta["description"] = (metadata["description"] ?? "") + DESCRIPTION_BOILERPLATE;
    const datasetUrl = "https://weed-ai.sydney.edu.au/datasets/" + upload_id;
    displayMeta["identifier"] = [...displayMeta.identifier || [], datasetUrl];
    const authorList = listToWords(displayMeta.creator.map((creator) => creator.name));
    return (
      <React.Fragment>
        <Helmet>
          <title>{metadata.name} Dataset - Weed-AI</title>
          <meta property="og:title" content={"Weed-AI dataset: " + metadata.name} />
          <meta property="og:description" content={getFirstLine(displayMeta.description)} />
          <meta property="og:url" content={datasetUrl} />
          <meta property="og:type" content="article" />
          <meta property="og:article:author" content={authorList} />
          <meta name="description" content={getFirstLine(displayMeta.description) + " by " + authorList + "."} />
        </Helmet>
        <script type="application/ld+json">
        {
          JSON.stringify({
            ...{
              "@context": "https://schema.org/",
              "@type": "Dataset",
              "url": window.location.href
            },
            ...displayMeta
          })
        }
        </script>
        <Grid container spacing={3} className={classes.topMatter}>
          <Grid item xs={10}>
            <div className={classes.summary}>
              <div style={{display: 'flex'}}>
                <IconButton aria-label="back to list" color="secondary" onClick={() => window.location.assign(rootURL + 'datasets')}>
                  <ListIcon />
                </IconButton>
                <Typography variant='h4' style={{fontWeight: 600}}>{displayMeta.name}</Typography>
              </div>
              <div style={{fontSize: "1.2em" }}>
              <ReactMarkdown source={displayMeta.description}  />
              </div>
              <Typography>
                Published {displayMeta.datePublished ? ["in ", yearPublished] : []} by {listToWords(displayMeta.creator.map((creator, i) => (
                    [linkedEntity(creator), creator.affiliation ? (<span> ({linkedEntity(creator.affiliation)})</span>) : []]
                  )))}.
              </Typography>
              <ul className={classes.identifierList}>
                {displayMeta.identifier.map(uri =>
                  <li key={uri}><Chip className={classes.identifierChip} icon={<LinkIcon/>} label={uri} variant="outlined" /></li>
                )}
              </ul>
            </div>
          </Grid>
          <Grid item xs={2}>
            <div className={classes.summary}>
                <Button component="a" variant="contained" className={classes.download} startIcon={<DownloadIcon />} onClick={() => window.open(`${rootURL}/code/download/${upload_id}.zip`)}>Download in WeedCOCO format</Button>
        <Button variant="outlined" startIcon={<PhotoIcon/>} href={"/explore?dataset_name_filter=%5B%22" + metadata.name + "%22%5D"}>Explore the Images</Button>
            </div>
          </Grid>
        </Grid>
        <Accordion className={classes.attribution}>
          <MyAccordionSummary>Citation and Licensing</MyAccordionSummary>
          <AccordionDetails>
          <dl>
            {displayMeta.citation ?
              [<dt>Citation:</dt>, <dd>{displayMeta.citation}</dd>] :
              [<dt>Citation:</dt>, <dd>{listToWords(displayMeta.creator.map(creator => creator.name))} ({yearPublished}). "{displayMeta.name}." In <cite>Weed-AI</cite>. {displayMeta.identifier[0]}. Accessed {new Date().toISOString().substr(0, 10)}.</dd>]
            }
            <dt>Licence:</dt>
            <dd>{<a href={displayMeta.license}>{displayMeta.license}</a>}</dd>
            {displayMeta.funder ?
                <React.Fragment>
                <dt>Funders:</dt>
                <dd>
                {listToWords(displayMeta.funder.map(ent => linkedEntity(ent)))}
                </dd>
                </React.Fragment>
            : []}
          </dl>
          </AccordionDetails>
        </Accordion>
        {agcontexts.map((agcontext, idx) =>
          <AgContextDetails MyAccordionSummary={MyAccordionSummary} metadata={metadata} agcontext={agcontext} key={idx} ordinal={idx + 1} nContexts={agcontexts.length} classes={classes} />
        )}
      </React.Fragment>
    );
}
const capitalFirstLetter = (string) => string.charAt(0).toUpperCase() + string.slice(1);
const snakeToText = (snakeName) => snakeName.split("_").map(string => capitalFirstLetter(string)).join(" ");

class DatasetSummaryPage extends Component {
  constructor (){
    super()
    this.state = {
      metadata: {
        name: "",
        description: "",
        creator: [],
        license: ""       
      },
      agcontexts: []
    }
  }

  componentDidMount (){
    axios({
        method: 'get',
        url: baseURL + "api/upload_info/" + this.props.upload_id,
        mode: 'same-origin',
    })
    .then(res => res.data)
    .then(json => {
        this.setState(json)
    })
  }

  render (){
    const {classes} = this.props
    const esURL = new URL(window.location.origin)
    return (
      <div className={classes.root}>
        <DatasetSummary metadata={this.state.metadata} agcontexts={this.state.agcontexts} classes={classes} rootURL={esURL} upload_id={this.props.upload_id} />
      </div>
    );
  }
}

export default withStyles(useStyles)(DatasetSummaryPage);
