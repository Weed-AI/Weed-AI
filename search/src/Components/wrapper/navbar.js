import React from 'react';
import PropTypes from 'prop-types';
import { makeStyles, withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Typography from '@material-ui/core/Typography';
import Box from '@material-ui/core/Box';
import ReactiveSearchComponent from './reactive_search';
import UploadComponent from './upload';
import DatasetComponent from './datasets';

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box p={3}>
          {children}
        </Box>
      )}
    </div>
  );
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.any.isRequired,
  value: PropTypes.any.isRequired,
};

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.paper,
  },
  container: {
    marginTop: '3rem'
  },
  logo: {
    position: 'absolute',
    right: '0.7em',
    top: '0.2em',
    fontSize: '1.8rem',
    fontWeight: 700
  }
}));

const StyledTabs = withStyles({
    indicator: {
      display: 'flex',
      justifyContent: 'center',
      backgroundColor: 'transparent',
      '& > span': {
        maxWidth: 0
      },
    },
  })((props) => <Tabs {...props} TabIndicatorProps={{ children: <span /> }} />);

const StyledTab = withStyles((theme) => ({
  root: {
    textTransform: 'none',
    color: 'white',
    fontWeight: theme.typography.fontWeightBold,
    fontSize: theme.typography.pxToRem(18),
    marginRight: theme.spacing(1),
    '&$selected': {
      backgroundColor: 'orange',
    },
    "&:hover": {
      opacity: 1
    },
  },
  selected: {}
}))((props) => <Tab disableRipple {...props} />);

export default function NavbarComponent(props) {

  const classes = useStyles();
  const { match } = props;
  const { params } = match;
  const { page, dataset_id } = params;

  const [selectedTab, setSelectedTab] = React.useState(page);

  const handleChange = (event, newValue) => {
    window.location.assign(`/${newValue}`);
  };

  return (
    <div className={classes.root}>
      <AppBar position="fixed">
        <StyledTabs onChange={handleChange} value={selectedTab}>
          <StyledTab value="explore" label="Explore" />
          <StyledTab value="datasets" label="Datasets" />
          <StyledTab value="upload" label="Upload" />
          <StyledTab value="about" label="About" disabled />
          <Typography variant='p' className={classes.logo}><span style={{color: '#f0983a'}}>Weed</span>AI</Typography>
        </StyledTabs>
      </AppBar>
      <div className={classes.container}>
      {
        selectedTab === "explore" && <ReactiveSearchComponent />
      }
      {
        selectedTab === "datasets" && <DatasetComponent upload_id={dataset_id}/>
      }
      {
        selectedTab === "upload" && <UploadComponent />
      }
      {
        selectedTab === "about" && <p>About Page Placeholder</p>
      }
      </div>
    </div>
  );
}
