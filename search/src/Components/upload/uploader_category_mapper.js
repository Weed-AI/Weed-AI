import { FormHelperText } from '@material-ui/core';
import Accordion from '@material-ui/core/Accordion';
import AccordionDetails from '@material-ui/core/AccordionDetails';
import AccordionSummary from '@material-ui/core/AccordionSummary';
import FormControl from '@material-ui/core/FormControl';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';
import { withStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import cloneDeep from 'lodash/cloneDeep';
import React from 'react';
import { formatCategoryName } from '../../Common/weedcocoUtil';


const useStyles = (theme) => ({
    summary: {
        marginLeft: '2.5em'
    },
    row: {
        backgroundColor: theme.palette.primary.light,
    },
    rowDetails: {
        backgroundColor: theme.palette.grey[100],
        display: "block",
    },
    categoryList: {
        overflow: "scroll",
        maxHeight: "20em",
        margin: theme.spacing(2),
    },
    incomplete: {
        color: 'red'
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
    },
	formControl: {
		marginBottom: theme.spacing(3),
	}
});

const isComplete = (category) => (category.role && category.scientific_name);

const CategoryEditor = ({ category, classes, isColor, changeRole, changeSciName, changeSubcategory }) => {
    const complete = isComplete(category);
    return (<Accordion className={classes.row} defaultExpanded={!complete}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />} className={complete ? "" : classes.incomplete}>
            {isColor ? <div className={classes.color} style={{backgroundColor: '#' + category.name}}></div> : []}
            <Typography>
                {isColor ? '#' : ''}{category.name} → <em>
                    {formatCategoryName({role: category.role, taxon: category.scientific_name, subcategory: category.subcategory})}
                </em>
            </Typography>
        </AccordionSummary>
        <AccordionDetails className={classes.rowDetails}>
            <Typography></Typography>
            <FormControl size="small" fullWidth className={classes.formControl}>
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
                <FormHelperText>Does this category indicate a weed or a crop in this dataset?</FormHelperText>
            </FormControl>
            <TextField size="small" fullWidth className={classes.sci_name}
                label="Species or other taxon"
                value={category.scientific_name} onChange={e => {e.persist(); changeSciName(e)}}
                helperText="Either 'UNSPECIFIED' or lowercase scientific name (family, genus, species depending on level of annotation)."
                />
            <TextField size="small" fullWidth
                label="Subcategory (optional)"
                value={category.subcategory} onChange={e => {e.persist(); changeSubcategory(e)}}
                helperText="Use this arbitrary label to distinguish among growth stages or plant parts within a species." />
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

    componentDidMount() {
        const { nCategories, nComplete } = this.getStats(this.state.categories)
        if (nCategories === nComplete) {
            this.props.handleValidation(true);
            this.props.handleErrorMessage("");
        }
    }

    modifyCategories(index, field, value) {
        const newCategories = cloneDeep(this.state.categories);
        newCategories[index][field] = value;
        this.setState({categories: newCategories});

        const { nCategories, nComplete } = this.getStats(newCategories);
        if (nCategories && nCategories === nComplete) {
            this.props.handleCategories(newCategories);
            this.props.handleErrorMessage("");
            this.props.handleValidation(true);
        } else {
            this.props.handleErrorMessage("Role or scientific name missing")
            this.props.handleValidation(false);
        }
    }

    changeRole(e, index) {
        this.modifyCategories(index, "role", e.target.value);
        this.props.handleErrorMessage("");
    }

    changeSciName(e, index) {
        this.modifyCategories(index, "scientific_name", e.target.value.toLowerCase());
        this.props.handleErrorMessage("");
    }

    changeSubcategory(e, index) {
        this.modifyCategories(index, "subcategory", e.target.value);
        this.props.handleErrorMessage("");
    }

    getStats(categories) {
        const nCategories = categories.length;
        const nComplete = categories.filter(isComplete).length;
        return {nCategories, nComplete}
    }

    render() {
        const { classes } = this.props;
        const { nCategories, nComplete } = this.getStats(this.state.categories);
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
                                changeSubcategory={(e) => this.changeSubcategory(e, index)}
                            />
                        })
                    }
                </div>
            </React.Fragment>
        )
    }
}

export default withStyles(useStyles)(CategoryMapper);
