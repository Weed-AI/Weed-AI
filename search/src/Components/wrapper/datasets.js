import React, {Component} from 'react';
import DatasetList from '../dataset/dataset_list';
import DatasetSummaryPage from '../dataset/dataset_summary';
import axios from 'axios';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';

const baseURL = new URL(window.location.origin); 

class DatasetComponent extends Component {
    constructor() {
        super()
        this.state = {
            is_staff: false,
            upload_id: "*",
            upload_id_list: [],
            upload_list: [],
            awaiting_id_list: [],
            awaiting_list: [],
            editing_id_list: [],
            editing_list: [],
            editing: false,
        }
        this.handleUploadid = this.handleUploadid.bind(this)
        this.handleSwitchEditingMode = this.handleSwitchEditingMode.bind(this)
    }

    componentDidMount () {
        axios.get(baseURL + 'api/upload_list/')
        .then(res => res.data)
        .then(json => {
            this.setState({upload_list: json})
            const upload_id_list = json.map(row => row.upload_id)
            this.setState({upload_id_list: upload_id_list})
            if (upload_id_list.includes(this.props.upload_id)) {
                this.setState({upload_id: this.props.upload_id})
            }
        })
        
        axios.get(baseURL + 'api/awaiting_list/')
        .then(res => res.data)
        .then(json => {
            this.setState({awaiting_list: json, is_staff: true})
            const awaiting_id_list = json.map(row => row.upload_id)
            this.setState({awaiting_id_list: awaiting_id_list})
            if (awaiting_id_list.includes(this.props.upload_id)) {
                this.setState({upload_id: this.props.upload_id})
            }
        })
        .catch(err => console.log(err))

        axios.get(baseURL + 'api/editing_list/')
        .then(res => res.data)
        .then(json => {
            this.setState({editing_list: json})
            const editing_id_list = json.map(row => row.upload_id)
            this.setState({editing_id_list: editing_id_list})
            if (editing_id_list.includes(this.props.upload_id)) {
                this.setState({upload_id: this.props.upload_id})
            }
        })
        .catch(err => console.log(err))
    }

    handleUploadid (upload_id) {
        this.setState({
            upload_id: upload_id
        })
    }

    handleSwitchEditingMode () {
        this.setState({
            editing: !this.state.editing
        })
    }

    render() {
        const editingToggle = 
        this.state.editing_id_list.length > 0 && this.state.upload_id === "*"
        ?
        (
            <FormControlLabel
            control={
            <Switch
                checked={this.state.editing}
                onClick={this.handleSwitchEditingMode}
                name="checkedA"
                color="primary"
            />
            }
            label="Show only Datasets I own"
            />
        )
        :
        ""
        let datasetSection;
        if (this.state.upload_id === "*") {
            if (!this.state.editing){
                // Dataset listing
                if (!this.state.is_staff || this.state.awaiting_list.length == 0) {
                    datasetSection = <DatasetList title={""} handleUploadid={this.handleUploadid} upload_list={this.state.upload_list} />;
                } else {
                    datasetSection = (
                        <React.Fragment>
                            <DatasetList title={"Awaiting approval"} handleUploadid={this.handleUploadid} upload_list={this.state.awaiting_list} inReview={true} />
                            <DatasetList title={"Public"} handleUploadid={this.handleUploadid} upload_list={this.state.upload_list} />
                        </React.Fragment>
                    );
                }
            }
            else {
                datasetSection = <DatasetList title={""} handleUploadid={this.handleUploadid} upload_list={this.state.editing_list} />;
            }
       } else {
            datasetSection = <DatasetSummaryPage upload_id={this.state.upload_id} handleUploadid={this.handleUploadid}/>;
       }
       return [editingToggle, datasetSection]
    }
}

export default DatasetComponent;
