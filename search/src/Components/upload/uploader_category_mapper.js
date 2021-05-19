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
        marginRight: '1em'
    },
    applyButton: {
        float: 'right'
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

    modifyCategories(index, field, value) {
        const newCategories = cloneDeep(this.state.categories);
        newCategories[index][field] = value;
        this.setState({categories: newCategories});
    }

    changeRole(e, index) {
        this.modifyCategories(index, "role", e.target.value);
        this.props.handleCategoriesSaved(false);
        this.props.handleErrorMessage("init");
    }

    changeSciName(e, index) {
        this.modifyCategories(index, "scientific_name", e.target.value);
        this.props.handleCategoriesSaved(false);
        this.props.handleErrorMessage("init");
    }

    render() {
        const { classes } = this.props;
        const nCategories = this.state.categories.length;
        const nComplete = this.state.categories.filter(category => category.role && category.scientific_name).length;
        return (
            <React.Fragment>
                <p className={classes.summary}>{nCategories - nComplete} of {nCategories} {nCategories != 1 ? 'categories' : 'category'} need mapping to weedcoco categories</p>
                <ol>
                    {
                        this.state.categories.map((category, index) => {
                            return (
                                <li className={category.role && category.name ? classes.row : `${classes.row} ${classes.incomplete}`}>
                                    <p className={classes.text_field}>{category.name} is a</p>
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
                                    <p className={classes.text_field}>of species</p>
                                    <TextField className={classes.sci_name} label="Scientific name or UNSPECIFIED" value={category.scientific_name} onChange={e => {e.persist(); this.changeSciName(e, index)}}/>
                                </li>
                            )
                        })
                    }
                </ol>
                <Button variant="contained"
                        color="primary"
                        className={classes.applyButton}
                        onClick={() => {
                            if (nCategories && nCategories === nComplete) {
                                this.props.handleCategories(this.state.categories)
                                this.props.handleErrorMessage("")
                                this.props.handleCategoriesSaved(true)
                            }
                            else {
                                this.props.handleErrorMessage("Role or scientific name missing")
                                this.props.handleCategoriesSaved(false)
                            }
                        }}>Apply</Button>
            </React.Fragment>
        )
    }
}

export default withStyles(useStyles)(CategoryMapper);
