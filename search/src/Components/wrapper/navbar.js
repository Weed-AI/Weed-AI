import React from 'react';
import PropTypes from 'prop-types';
import { makeStyles, withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Typography from '@material-ui/core/Typography';
import Box from '@material-ui/core/Box';
import ReactiveSearchComponent from './reactive_search'
import UploadComponent from './upload'
import DatasetComponent from './datasets'

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

function a11yProps(index) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}

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

export default function NavbarComponent() {
  const classes = useStyles();
  const [value, setValue] = React.useState(0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <div className={classes.root}>
      <AppBar position="fixed">
        <StyledTabs onChange={handleChange} value={value}>
          <StyledTab label="Explore" {...a11yProps(0)}/>
          <StyledTab label="Datasets" {...a11yProps(1)} />
          <StyledTab label="Upload" {...a11yProps(2)} />
          <StyledTab label="About" disabled {...a11yProps(3)} />
          <Typography variant='p' className={classes.logo}><span style={{color: '#f0983a'}}>Weed ID</span>entification Database</Typography>
        </StyledTabs>
      </AppBar>
      <TabPanel value={value} index={0}>
        <div className={classes.container}>
            <ReactiveSearchComponent />
        </div>
      </TabPanel>
      <TabPanel value={value} index={1}>
        <div className={classes.container}>
            <DatasetComponent />
        </div>
      </TabPanel>
      <TabPanel value={value} index={2}>
        <div className={classes.container}>
            <UploadComponent />
        </div>
      </TabPanel>
      <TabPanel value={value} index={3}>
        <div className={classes.container}>
            About Page Placeholder
        </div>
      </TabPanel>
    </div>
  );
}