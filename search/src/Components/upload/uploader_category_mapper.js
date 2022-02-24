import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Accordion from '@material-ui/core/Accordion';
import Typography from '@material-ui/core/Typography';
import AccordionSummary from '@material-ui/core/AccordionSummary';
import AccordionDetails from '@material-ui/core/AccordionDetails';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import cloneDeep from 'lodash/cloneDeep';


const useStyles = (theme) => ({
    summary: {
        marginLeft: '2.5em'
    },
    row: {
        backgroundColor: theme.palette.grey[50],
    },
    categoryList: {
        overflow: "scroll",
        maxHeight: "15em",
        margin: theme.spacing(2),
    },
    incomplete: {
        color: 'red'
    },
    formControl: {
        margin: theme.spacing(1),
        minWidth: 120,
    },
    text_field: {
        marginRight: '1em',
        marginLeft: '1em',
    },
    applyButton: {
        float: 'right'
    },
    color: {
        height: '1.2em',
        width: '1.2em',
        borderRadius: '50%',
        marginRight: "1em",
    }
});

const isComplete = (category) => (category.role && category.scientific_name);

const CategoryEditor = ({ category, classes, isColor, changeRole, changeSciName }) => {
    const complete = isComplete(category);
    return (<Accordion className={complete ? classes.row : `${classes.row} ${classes.incomplete}`} defaultExpanded={!complete}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            {isColor ? <div className={classes.color} style={{backgroundColor: '#' + category.name}}></div> : []}
            <Typography>{isColor ? '#' : ''}{category.name}</Typography>
        </AccordionSummary>
        <AccordionDetails>
            <FormControl fullWidth={true} className={classes.formControl}>
                <InputLabel id="category">Role</InputLabel>
                <Select
                labelId="category"
                id="category"
                value={category.role}
                onChange={e => {changeRole(e)}}
                >
                    <MenuItem value={"crop"}>crop</MenuItem>
                    <MenuItem value={"weed"}>weed</MenuItem>
                </Select>
            </FormControl>
            <TextField fullWidth={true} className={classes.sci_name} label="Scientific name or UNSPECIFIED" value={category.scientific_name} onChange={e => {e.persist(); changeSciName(e)}}/>
        </AccordionDetails>
    </Accordion>);
}

class CategoryMapper extends React.Component {
    
    constructor(props) {
        super(props);
        this.state = {
            categories: this.props.categories
        }
        this.modifyCategories = this.modifyCategories.bind(this);
        this.changeRole = this.changeRole.bind(this);
        this.changeSciName = this.changeSciName.bind(this);
    }

    modifyCategories(index, field, value) {
        const newCategories = cloneDeep(this.state.categories);
        newCategories[index][field] = value;
        this.setState({categories: newCategories});
    }

    changeRole(e, index) {
        this.modifyCategories(index, "role", e.target.value);
        this.props.handleValidation(false);
        this.props.handleErrorMessage("");
    }

    changeSciName(e, index) {
        this.modifyCategories(index, "scientific_name", e.target.value);
        this.props.handleValidation(false);
        this.props.handleErrorMessage("");
    }

    render() {
        const { classes } = this.props;
        const nCategories = this.state.categories.length;
        const nComplete = this.state.categories.filter(isComplete).length;
        return (
            <React.Fragment>
                <p className={classes.summary}>{nCategories - nComplete} of {nCategories} {nCategories != 1 ? 'categories' : 'category'} need mapping to weedcoco categories</p>
                <div className={classes.categoryList}>
                    {
                        this.state.categories.map((category, index) => {
                            return <CategoryEditor
                                key={index} classes={classes}
                                category={category} isColor={/^[0-9A-Fa-f]{6}$/i.test(category.name)}
                                changeRole={(e) => this.changeRole(e, index)}
                                changeSciName={(e) => this.changeSciName(e, index)}
                            />
                        })
                    }
                </div>
                <Button variant="contained"
                        color="primary"
                        className={classes.applyButton}
                        onClick={() => {
                            if (nCategories && nCategories === nComplete) {
                                this.props.handleCategories(this.state.categories)
                                this.props.handleErrorMessage("")
                                this.props.handleValidation(true);
                            }
                            else {
                                this.props.handleErrorMessage("Role or scientific name missing")
                                this.props.handleValidation(true);
                            }
                        }}>Apply</Button>
            </React.Fragment>
        )
    }
}

export default withStyles(useStyles)(CategoryMapper);
