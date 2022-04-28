import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import cloneDeep from 'lodash/cloneDeep';


const useStyles = (theme) => ({
    summary: {
        marginLeft: '2.5em'
    },
    row: {
        display: 'flex',
        alignItems: 'baseline'
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
        margin: '1em'
    }
});

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
        this.modifyCategories(index, "scientific_name", e.target.value);
        this.props.handleErrorMessage("");
    }

    getStats(categories) {
        const nCategories = categories.length;
        const nComplete = categories.filter(category => category.role && category.scientific_name).length;
        return {nCategories, nComplete}
    }

    render() {
        const { classes } = this.props;
        const { nCategories, nComplete } = this.getStats(this.state.categories);
        return (
            <React.Fragment>
                <p className={classes.summary}>
                    {nCategories === nComplete ? 0 : <span className={classes.incomplete}>{nCategories - nComplete}</span>} of {nCategories} {nCategories != 1 ? 'categories' : 'category'} need mapping to weedcoco categories
                </p>
                <ol>
                    {
                        this.state.categories.map((category, index) => {
                            return (
                                <li className={category.role && category.name ? classes.row : `${classes.row} ${classes.incomplete}`}>
                                    {/^[0-9A-Fa-f]{6}$/i.test(category.name) ? <div className={classes.color} style={{backgroundColor: '#' + category.name}}></div> : <p>{category.name}</p>}
                                    <p className={classes.text_field}> is a</p>
                                    <FormControl className={classes.formControl}>
                                        <InputLabel id="category">Role</InputLabel>
                                        <Select
                                        labelId="category"
                                        id="category"
                                        value={category.role}
                                        onChange={e => {this.changeRole(e, index)}}
                                        >
                                            <MenuItem value={"crop"}>crop</MenuItem>
                                            <MenuItem value={"weed"}>weed</MenuItem>
                                        </Select>
                                    </FormControl>
                                    <p className={classes.text_field}>of type</p>
                                    <TextField className={classes.sci_name} label="Scientific name or UNSPECIFIED" value={category.scientific_name} onChange={e => {e.persist(); this.changeSciName(e, index)}}/>
                                </li>
                            )
                        })
                    }
                </ol>
            </React.Fragment>
        )
    }
}

export default withStyles(useStyles)(CategoryMapper);
