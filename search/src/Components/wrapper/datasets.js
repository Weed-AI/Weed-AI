import React, {Component} from 'react';
import DatasetList from '../dataset/dataset_list';
import DatasetSummary from '../dataset/dataset_summary';
import axios from 'axios';

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
            awaiting_list: []
        }
        this.handleUploadid = this.handleUploadid.bind(this)
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
    }

    handleUploadid (upload_id) {
        this.setState({
            upload_id: upload_id
        })
    }

    render() {
        return (
            <React.Fragment>
                {this.state.upload_id === "*"?
                <DatasetList handleUploadid={this.handleUploadid} upload_list={this.state.upload_list} awaiting_list={this.state.awaiting_list} is_staff={this.state.is_staff}/>:
                <DatasetSummary upload_id={this.state.upload_id} handleUploadid={this.handleUploadid}/>}
            </React.Fragment>
        )
    }
}

export default DatasetComponent;