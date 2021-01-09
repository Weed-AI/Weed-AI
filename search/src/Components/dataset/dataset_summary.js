import React, {Component} from 'react';
import { withStyles } from '@material-ui/core/styles';
import Accordion from '@material-ui/core/Accordion';
import AccordionSummary from '@material-ui/core/AccordionSummary';
import AccordionDetails from '@material-ui/core/AccordionDetails';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import { Button } from '@material-ui/core';
import Grid from '@material-ui/core/Grid';
import axios from 'axios';
import ListIcon from '@material-ui/icons/List';
import IconButton from '@material-ui/core/IconButton';
import Cookies from 'js-cookie'


const csrftoken = Cookies.get('csrftoken');

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
    height: '20vh'
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

class DatasetSummary extends Component {
  constructor (){
    super()
    this.state = {
      metadata: {
        info: [],
        license: [],
        collections: []
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
        data: body,
        headers: {'Content-Type': 'multipart/form-data', 'X-CSRFToken': csrftoken }
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
    const capitalFirstLetter = (string) => string.charAt(0).toUpperCase() + string.slice(1)
    const converter = (snakeName) => snakeName.split("_").map(string => capitalFirstLetter(string)).join(" ")
    const getAttribute = (collection, key) => collection.length > 0 && key in collection[0] ? collection[0][key] : ""
    return (
      <div className={classes.root}>
        <Grid container spacing={3}>
          <Grid item xs={10}>
            <div className={classes.summary}>
              <div style={{display: 'flex'}}>
                <IconButton aria-label="back to list" color="secondary" onClick={() => this.props.handleUploadid("*")}>
                  <ListIcon />
                </IconButton>
                <Typography variant='h4' style={{fontWeight: 600}}>{getAttribute(this.state.metadata.info, "name")}</Typography>
              </div>
              <p>
                {getAttribute(this.state.metadata.collections, "title")}
              </p>
              <p>
                Author:
                &nbsp;
                {getAttribute(this.state.metadata.collections, "author")}
              </p>
              <p>
                Licence:
                &nbsp;
                {getAttribute(this.state.metadata.license, "license_name")}
                &nbsp;
                {getAttribute(this.state.metadata.license, "url")}
              </p>
            </div>
          </Grid>
          <Grid item xs={2}>
            <div className={classes.summary}>
                <Button className={classes.download}>Download in WeedCOCO format</Button>
            </div>
          </Grid>
        </Grid>
        <Accordion defaultExpanded='true'>
          <AccordionSummary
            expandIcon={<ExpandMoreIcon />}
            aria-controls="panel1a-content"
            id="panel1a-header"
            className={classes.header}
          >
            <Typography className={classes.heading}>Agricultural Context</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Grid container spacing={2}>
              {this.state.agcontexts.length > 0 ?
               Object.keys(this.state.agcontexts[0]).map(key =>
              <Grid item xs={2}><Typography variant='p'>{converter(key)}:&nbsp;{this.state.agcontexts[0][key]}</Typography></Grid>)
               :""
              }
            </Grid>
          </AccordionDetails>
        </Accordion>
        <Accordion disabled>
          <AccordionSummary
            expandIcon={<ExpandMoreIcon />}
            aria-controls="panel2a-content"
            id="panel2a-header"
            className={classes.header}
          >
            <Typography className={classes.heading}>Annotations for Classification</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Typography>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse malesuada lacus ex,
              sit amet blandit leo lobortis eget.
            </Typography>
          </AccordionDetails>
        </Accordion>
        <Accordion disabled>
          <AccordionSummary
            expandIcon={<ExpandMoreIcon />}
            aria-controls="panel2a-content"
            id="panel2a-header"
            className={classes.header}
          >
            <Typography className={classes.heading}>Sample of 17,509 Images</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Typography>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse malesuada lacus ex,
              sit amet blandit leo lobortis eget.
            </Typography>
          </AccordionDetails>
        </Accordion>
      </div>
    );
  }
}

export default withStyles(useStyles)(DatasetSummary);