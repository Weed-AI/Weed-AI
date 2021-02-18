import React, { useEffect } from 'react';
import PropTypes from 'prop-types';
import { makeStyles, withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Box from '@material-ui/core/Box';
import Drawer from '@material-ui/core/Drawer';
import IconButton from '@material-ui/core/IconButton';
import Link from '@material-ui/core/Link';
import MenuItem from '@material-ui/core/MenuItem';
import MenuIcon from '@material-ui/icons/Menu';
import Tab from '@material-ui/core/Tab';
import Tabs from '@material-ui/core/Tabs';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import ReactiveSearchComponent from './reactive_search';
import UploadComponent from './upload';
import DatasetComponent from './datasets';
import WeedCOCOComponent from './weedcoco';
import AboutComponent from './about';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.paper,
  },
  container: {
    marginTop: '3rem',
    '@media (max-width: 1000px)': {
      marginTop: '4.5rem',
    },
  },
  logo: {
    position: 'absolute',
    right: '2em',
    top: '0.2em',
    fontSize: '1.8rem',
    fontWeight: 700,
    color: "white",
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
    paddingLeft: '0px',
    paddingRight: '0px',
    '&$selected': {
      backgroundColor: 'orange',
    },
    "&:hover": {
      opacity: 1
    },
  },
  selected: {}
}))((props) => <Tab component="a" disableRipple {...props} />);

const sections = [
  {value: "explore", href: "/explore", label: "Explore"},
  {value: "datasets", href: "/datasets", label: "Datasets"},
  {value: "upload", href: "/upload", label: "Upload"},
  {value: "weedcoco", href: "/weedcoco", label: "WeedCOCO"},
  {value: "about", href: "/about", label: "About"},
]


const MobileNavbar = (props) => {
  const {classes, selectedTab, handleChange} = props;
  const [drawerOpen, setDrawerOpen] = React.useState(false);
  const getCurrentLabel = () => {
    const idx = sections.findIndex((x) => x.value == selectedTab);
    return idx == -1 ? "" : sections[idx].label;
  }
  return (
    <Toolbar>
      <IconButton
        edge="start" className={classes.menuButton} color="inherit"
        aria-label="menu" aria-has-popup="true"
        onClick={() => {setDrawerOpen(true)}}
      >
        <MenuIcon />
      </IconButton>
      <Drawer open={drawerOpen} anchor="left" onClose={() => {setDrawerOpen(false)}}>
        { sections.map((section) =>
          <Link onClick={handleChange} href={section.href} color="inherit" style={{ textDecoration: "none" }} key={section.label} >
            <MenuItem selected={selectedTab == section.value}>{section.label}</MenuItem>
          </Link>
        ) }
      </Drawer>
      <Typography>{getCurrentLabel()}</Typography>
      <Logo classes={classes} />
    </Toolbar>
  );
}

const Logo = (props) => {
  const {classes} = props;
  return (
      <Typography variant='p' className={classes.logo}><span style={{color: '#f0983a'}}>Weed-</span>AI</Typography>
  );
}

const DesktopNavbar = (props) => {
  const {handleChange, selectedTab, classes} = props;
  return (
    <StyledTabs onChange={handleChange} value={selectedTab}>
      { sections.map((section) => <StyledTab value={section.value} href={section.href} label={section.label} />) }
      <Logo classes={classes} />
    </StyledTabs>
  );
}

export default function NavbarComponent(props) {

  const classes = useStyles();
  const { match } = props;
  const { params } = match;
  const { page, dataset_id } = params;

  const [selectedTab, setSelectedTab] = React.useState(page);
  const [mobileView, setMobileView] = React.useState(false);

  useEffect(() => {
    const setResponsiveness = () => {
      return window.innerWidth < 1000
        ? setMobileView(true)
        : setMobileView(false);
    };
    setResponsiveness();
    window.addEventListener("resize", () => setResponsiveness());
  }, []);

  const handleChange = (event, newValue) => {
    window.location.assign(`/${newValue}`);
  };

  return (
    <div className={classes.root}>
      <AppBar position="fixed" style={{
    backgroundImage: "url(/weedai-background-trunc.png)",
    backgroundRepeat: "no-repeat",
    backgroundPosition: "right center",
    backgroundSize: "15rem",
  }}>
        { mobileView ?
          <MobileNavbar selectedTab={selectedTab} classes={classes} handleChange={handleChange} /> :
          <DesktopNavbar selectedTab={selectedTab} classes={classes} handleChange={handleChange} /> }
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
        selectedTab === "weedcoco" && <WeedCOCOComponent />
      }
      {
        selectedTab === "about" && <AboutComponent />
      }
      </div>
    </div>
  );
}
