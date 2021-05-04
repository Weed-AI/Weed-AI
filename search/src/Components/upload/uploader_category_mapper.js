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
    formControl: {
        margin: theme.spacing(1),
        minWidth: 120,
    },
    span: {
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
        this.changeCategory = this.changeCategory.bind(this);
        this.changeSciName = this.changeSciName.bind(this);
    }

    modifyCategories(index, field, value) {
        const newCategories = cloneDeep(this.state.categories);
        newCategories[index][field] = value;
        this.setState({categories: newCategories});
    }

    changeCategory(e, index) {
        this.modifyCategories(index, "category", e.target.value);
        this.props.handleCategoryStatus(false);
        this.props.handleErrorMessage("init");
    }

    changeSciName(e, index) {
        this.modifyCategories(index, "scitific_name", e.target.value);
        this.props.handleCategoryStatus(false);
        this.props.handleErrorMessage("init");
    }

    render() {
        const { classes } = this.props;
        return (
            <React.Fragment>
                <p className={classes.summary}>{this.state.categories.length} {this.state.categories.length > 1 ? 'categories' : 'category'} need mapping to weedcoco categories</p>
                <ol>
                    {
                        this.state.categories.map((category, index) => {
                            return (
                                <li className={classes.row}>
                                    <p className={classes.span}>{category.name} is a</p>
                                    <FormControl className={classes.formControl}>
                                        <InputLabel id="category">Category</InputLabel>
                                        <Select
                                        labelId="category"
                                        id="category"
                                        value={category.category}
                                        onChange={e => {this.changeCategory(e, index)}}
                                        >
                                            <MenuItem value={"crop"}>crop</MenuItem>
                                            <MenuItem value={"weed"}>weed</MenuItem>
                                        </Select>
                                    </FormControl>
                                    <p className={classes.span}>of species</p>
                                    <TextField label="Scitific name" onChange={e => {e.persist(); this.changeSciName(e, index)}}/>
                                </li>
                            )
                        })
                    }
                </ol>
                <Button variant="contained"
                        color="primary"
                        className={classes.applyButton}
                        onClick={() => {
                            if (this.state.categories.length > 0 && this.state.categories.length === this.state.categories.filter(category => category.category.length > 0).length) {
                                this.props.handleCategories(this.state.categories)
                                this.props.handleErrorMessage("")
                                this.props.handleCategoryStatus(true)
                            }
                            else {
                                this.props.handleErrorMessage("Category missing")
                                this.props.handleCategoryStatus(false)
                            }
                        }}>Apply</Button>
            </React.Fragment>
        )
    }
}

export default withStyles(useStyles)(CategoryMapper);