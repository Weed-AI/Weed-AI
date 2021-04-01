import React, {Component} from 'react';
import { Helmet } from "react-helmet";
import { withStyles } from '@material-ui/core/styles';
import Accordion from '@material-ui/core/Accordion';
import AccordionSummary from '@material-ui/core/AccordionSummary';
import AccordionDetails from '@material-ui/core/AccordionDetails';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
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
import IconButton from '@material-ui/core/IconButton';
import Cookies from 'js-cookie'
import ReactMarkdown from "react-markdown";


const DESCRIPTION_BOILERPLATE = "\n\nEvery dataset in Weed-AI includes imagery of crops or pasture with weeds annotated, and is available in an MS-COCO derived format with standardised agricultural metadata."

const useStyles = (theme) => ({
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
    padding: '1.5em 0',
    width: '100%',
    fontSize: '1.2rem',
    fontWeight: 900,
    backgroundColor: 'orange',
    color: 'white',
  }
});

const baseURL = new URL(window.location.origin);

const AgContextFieldList = (props) => {
    const {title, agcontext, fields, classes, ...accordionProps} = props;
    const formatters = {
      bbch_growth_range: (val) => (val["min"] !== undefined ? val["min"] + " to " + val["max"] : val),
    }
    const format = (key, val) => (formatters.hasOwnProperty(key) ? formatters[key](val) : val);
    return (
      <Accordion {...accordionProps}>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1a-content"
          id="panel1a-header"
          className={classes.header}
        >
          <Typography className={classes.heading}>{title}</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <ul>
            {fields.map(key =>
            (agcontext[key] ? <li key={key}><Typography variant='body2'>{snakeToText(key)}:&nbsp;{format(key, agcontext[key])}</Typography></li> : ""))
            }
          </ul>
        </AccordionDetails>
      </Accordion>
    );
}

const AgContextDetails = (props) => {
    const {agcontext, ordinal, nContexts, classes} = props;
    const tableFields = {"image_count": "# Images", "segmentation_count": "# Segments", "bounding_box_count": "# Bounding Boxes"}
    return (
      <article>
        {nContexts > 1 ? <h2>Agricultural Context {ordinal} of {nContexts}</h2> : ""}
        <Accordion defaultExpanded='true'>
          <AccordionSummary
            expandIcon={<ExpandMoreIcon />}
            aria-controls="panel1a-content"
            id="panel1a-header"
            className={classes.header}
          >
            <Typography className={classes.heading}>Annotation Statistics</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <p>Total number of images: {agcontext.n_images}</p>
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
        <AgContextFieldList defaultExpanded="true" classes={classes} agcontext={agcontext} title="The Crop" fields={["crop_type", "bbch_growth_range", "soil_colour", "surface_cover", "surface_coverage", "location_lat", "location_long"]} />
        <AgContextFieldList classes={classes} agcontext={agcontext} title="The Photography" fields={["camera_make", "camera_lens", "camera_lens_focallength", "camera_height", "camera_angle", "camera_fov", "ground_speed", "lighting", "photography_description"]} />
        <AgContextFieldList classes={classes} agcontext={agcontext} title="Other Details" fields={["cropped_to_plant", "emr_channels", "weather_description"]} />
      </article>
    );
}

export const DatasetSummary = (props) => {
    const {metadata, agcontexts, classes, rootURL, upload_id} = props;
    const linkedEntity = (ent) => {
      if (ent.sameAs)
        return (<a href={ent.sameAs}>{ent.name}</a>);
      return ent.name;
    }
    const getFirstLine = (s) => (s.match(/[^\n.]*/)[0]);
    const displayMeta = {...metadata}
    displayMeta["description"] = (metadata["description"] ?? "") + DESCRIPTION_BOILERPLATE;
    return (
      <React.Fragment>
        <Helmet>
          <title>"{displayMeta.name}" Dataset in Weed-AI: a repository of weed imagery in crops</title>
          <meta name="description" content={getFirstLine(displayMeta.description) + " by " + displayMeta.creator.map((creator) => creator.name).join(', ') + "."} />
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
        <Grid container spacing={3}>
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
              <dl>
                <dt>Creators:</dt>
                <dd>
                  <ul>
                  {displayMeta.creator.map((creator, i) => (
                    <li key={i}>
                      {linkedEntity(creator)}{creator.affiliation ? (<span>, {linkedEntity(creator.affiliation)}</span>) : []}
                    </li>
                  ))}
                  </ul>
                </dd>
                <dt>Licence:</dt>
                <dd>{<a href={displayMeta.license}>{displayMeta.license}</a>}</dd>
                {displayMeta.funder ?
                    <React.Fragment>
                    <dt>Funders:</dt>
                    <dd>
                      <ul>
                        {displayMeta.funder.map(ent => <li key={ent.name}>{linkedEntity(ent)}</li>)}
                      </ul>
                    </dd>
                    </React.Fragment>
                : []}
              </dl>
              { /* TODO: link to Explore searching for just this dataset */ }
            </div>
          </Grid>
          <Grid item xs={2}>
            <div className={classes.summary}>
                <Button className={classes.download} onClick={() => window.open(`${rootURL}/code/download/${upload_id}.zip`)}>Download in WeedCOCO format</Button>
            </div>
          </Grid>
        </Grid>
        {agcontexts.map((agcontext, idx) =>
          <AgContextDetails agcontext={agcontext} key={idx} ordinal={idx + 1} nContexts={agcontexts.length} classes={classes} />
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
    const body = new FormData()
    body.append('upload_id', this.props.upload_id)
    axios({
        method: 'post',
        url: baseURL + "api/upload_info/",
        mode: 'same-origin',
        data: body,
        headers: {'Content-Type': 'multipart/form-data', 'X-CSRFToken': Cookies.get('csrftoken') }
    })
    .then(res => res.data)
    .then(json => {
        this.setState(json)
    })
    .then(() => {
        console.log(this.state)
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

export const TestDatasetSummary = () => {
    const props = {
        "metadata": {
            "creator": [
                {"name": "Sebastian Haug"},
                {"name": "J\u00f6rn Ostermann", "sameAs": "https://orcid.org/0000-0002-6743-3324", "affiliation": {"name": "Leibniz Universität Hannover", "sameAs": "https://ror.org/0304hq317", "@type": "Organization"}}
            ],
            "funder": [{"name": "some funder"}],
            "name": "A Crop/Weed Field Image Dataset for the Evaluation of Computer Vision Based Precision Agriculture Tasks",
            "datePublished": "2015-03-19",
            "identifier": ["doi:10.1007/978-3-319-16220-1_8"],
            "license": "https://github.com/cwfid/dataset",
            "description": "Foobar",
            "citation": "Sebastian Haug, Jörn Ostermann: A Crop/Weed Field Image Dataset for the Evaluation of Computer Vision Based Precision Agriculture Tasks, CVPPP 2014 Workshop, ECCV 2014"
        },
        "agcontexts": [
            {"n_images": 3, "category_statistics": 
        {"crop: foo": {"annotation_count": 2, "image_count": 1, "segmentation_count": 2, "bounding_box_count": 2},
        "weed: bar": {"annotation_count": 3, "image_count": 2, "segmentation_count": 3, "bounding_box_count": 3},
        "weed: blah": {"annotation_count": 1, "image_count": 1, "segmentation_count": 0, "bounding_box_count": 0}},
                "id": 77, "lighting": "natural", "bbch_code": "na", "crop_type": "sorghum", "camera_fov": "variable", "camera_lens": "Telephoto", "camera_make": "Canon", "soil_colour": "dark_brown", "camera_angle": 45, "emr_channels": "visual", "location_lat": 80, "camera_height": 500, "location_long": 80, "surface_cover": "oilseed", "cropped_to_plant": true, "surface_coverage": "0-25", "weather_description": "rainy", "bbch_descriptive_text": "stem elongation", "camera_lens_focallength": 180, "grains_descriptive_text": "emergence", "photography_description": "poor lighting"}]}
    const Out = withStyles(useStyles)(DatasetSummary);
    return (<div style={{ margin: "3em" }}><Out {...props} /></div>);
}

export default withStyles(useStyles)(DatasetSummaryPage);
