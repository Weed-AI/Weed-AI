import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Autocomplete from '@material-ui/lab/Autocomplete';
import axios from 'axios';
import {jsonSchemaTitle} from '../error/utils';


const useStyles = (theme) => ({
    applyButton: {
        float: 'right'
    },
    loginButton: {
    }
});

const baseURL = new URL(window.location.origin);

class CvatRetriever extends React.Component {
    
    constructor(props) {
        super(props);
        this.state = {
            cvat_logged_in: false,
            cvat_tasks: [],
            selected_task_id: 0
        }
        this.retrieveCvatTasksList = this.retrieveCvatTasksList.bind(this);
        this.retrieveTaskExportFile = this.retrieveTaskExportFile.bind(this);
    }

    async retrieveCvatTasksList() {
        const current_tasks_list = []
        let current_page = 1
        while(true){
            try {
                let res = await axios.get(baseURL + `cvat-annotation/api/v1/tasks?page_size=10&page=${current_page}`)
                const data = res.data
                if (!this.state.cvat_logged_in && data.count > 0) this.setState({cvat_logged_in: true})
                for (const task of data.results) {
                    current_tasks_list.push({name: task.name, id: task.id, })
                }
                current_page = current_page + 1
                if (data.count < 10) {
                    this.setState({cvat_tasks: current_tasks_list})
                    break
                }
            } catch (error) {
                console.log(error)
                this.setState({cvat_logged_in: false})
                break
            }
        }
    }
    
    async retrieveTaskExportFile() {
        try {
            const res = await axios.get(baseURL + `cvat-annotation/api/v1/tasks/${this.state.selected_task_id}/annotations?format=COCO%201.0&filename=temp.zip`)
            if (res.statusText === 'Created') {
                const cvat_res = await axios.get(baseURL + `api/retrieve_cvat_task/${this.state.selected_task_id}`)
                const payload = cvat_res.data
                this.props.handleUploadId(payload.upload_id)
                this.props.handleImages(payload.images)
                this.props.handleCategories(payload.categories)
                this.props.handleValidation(true)
            }
        } catch (error) {
            console.log(error)
            const err = JSON.parse(error.responseText)
            this.props.handleErrorMessage(jsonSchemaTitle(err), err)
            this.props.handleValidation(false)
        }
        
    }

    componentDidMount() {
        this.retrieveCvatTasksList();
        setInterval(this.retrieveCvatTasksList, 5000)
    }

    render() {
        const { classes } = this.props;
        if(this.state.cvat_logged_in){
            return (
                <React.Fragment>
                    <Autocomplete
                            options={this.state.cvat_tasks}
                            getOptionLabel={(task) => task.name}
                            style={{ width: 300 }}
                            renderInput={(params) => <TextField {...params} label="Select a specific CVAT task" variant="outlined" />}
                            onChange={(_, value) => {
                                if (value == null) {
                                    this.state.selected_task_id = 0
                                    this.props.handleCvatTaskId(0)
                                } else {
                                    this.state.selected_task_id = value.id
                                    this.props.handleCvatTaskId(value.id)
                                }
                            }}
                    />
                    <Button 
                            variant="contained"
                            color="primary"
                            className={classes.applyButton}
                            disabled={this.state.selected_task_id == 0}
                            onClick={this.retrieveTaskExportFile}>
                        Apply
                    </Button>
                </React.Fragment>
            )
        }
        else {
            return (
                <React.Fragment>
                    <Button 
                        variant="contained"
                        color="primary"
                        className={classes.loginButton}
                        onClick={()=> window.open(baseURL + "cvat-annotation", "_blank")}>
                        Login to CVAT
                    </Button>
                </React.Fragment>
            )
        }
    }
}

export default withStyles(useStyles)(CvatRetriever);
