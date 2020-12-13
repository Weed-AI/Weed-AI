import React, {Component} from 'react';
import DatasetList from '../dataset/dataset_list';
import DatasetSummary from '../dataset/dataset_summary';
import axios from 'axios';

const baseURL = new URL(window.location.origin); 

class DatasetComponent extends Component {
    constructor() {
        super()
        this.state = {
            upload_id: "*",
            upload_list: []
        }
        this.handleUploadid = this.handleUploadid.bind(this)
    }

    componentDidMount () {
        axios.get(baseURL + 'api/upload_list/')
        .then(res => res.data)
        .then(json => {
            this.setState({upload_list: json})
        })
    }

    handleUploadid (upload_id) {
        this.setState({
            upload_id: upload_id
        })
    }

    render() {
        return (
            <React.Fragment>
                {this.state.upload_id === "*" ? <DatasetList handleUploadid={this.handleUploadid} upload_list={this.state.upload_list}/> : <DatasetSummary upload_id={this.state.upload_id} handleUploadid={this.handleUploadid}/>}
            </React.Fragment>
        )
    }
}

export default DatasetComponent;