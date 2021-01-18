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
  const { match, history } = props;
  const { params } = match;
  const { page } = params;

  const tabNameToIndex = {
    0: "explore",
    1: "datasets",
    2: "upload",
    3: "about"
  };

  const indexToTabName = {
    explore: 0,
    datasets: 1,
    upload: 2,
    about: 3
  };

  const [selectedTab, setSelectedTab] = React.useState(indexToTabName[page]);

  const handleChange = (event, newValue) => {
    history.push(`/${tabNameToIndex[newValue]}`);
    setSelectedTab(newValue);
  };

  return (
    <div className={classes.root}>
      <AppBar position="fixed">
        <StyledTabs onChange={handleChange} value={selectedTab}>
          <StyledTab label="Explore" />
          <StyledTab label="Datasets" />
          <StyledTab label="Upload" />
          <StyledTab label="About" disabled />
          <Typography variant='p' className={classes.logo}><span style={{color: '#f0983a'}}>Weed ID</span>entification Database</Typography>
        </StyledTabs>
      </AppBar>
      {
        selectedTab === 0
        &&
        <div className={classes.container}>
            <ReactiveSearchComponent />
        </div>
      }
      {
        selectedTab === 1
        &&
        <div className={classes.container}>
            <DatasetComponent />
        </div>
      }
      {
        selectedTab === 2
        &&
        <div className={classes.container}>
            <UploadComponent />
        </div>
      }
      {
        selectedTab === 3
        &&
        <div className={classes.container}>
            About Page Placeholder
        </div>
      }
    </div>
  );
}