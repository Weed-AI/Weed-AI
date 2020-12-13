import React, {Component} from 'react';
import UploadDialog from '../upload/upload_dialog';
import { withStyles } from '@material-ui/core/styles';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import axios from 'axios';


const useStyles = (theme) => ({
    upload_container: {
        margin: theme.spacing(10)
    },
    formControl: {
        margin: theme.spacing(2),
        minWidth: 200,
    },
})

const baseURL = new URL(window.location.origin);
const upload_status_mapping = {
    'N': 'None',
    'P': 'Processing',
    'I': 'Incomplete',
    'AR': 'Awaiting Review',
    'F': 'Failed',
    'C': 'Complete'
}

class UploadComponent extends Component {
    constructor(){
        super()
        this.state = {
            upload_status: "None",
            upload_status_details: "",
            upload_type: "",
        }
        this.handleChange = this.handleChange.bind(this);
        this.retrieveUploadStatus = this.retrieveUploadStatus.bind(this);
    }

    handleChange(event){
        this.setState({upload_type: event.target.value})
    };

    retrieveUploadStatus(){
        axios.get(baseURL + "api/upload_status/")
        .then(res => res.data)
        .then(json => {
            this.setState({upload_status: upload_status_mapping[json.upload_status],
                           upload_status_details: json.upload_status_details})
        })
    }

    componentDidMount(){
        this.retrieveUploadStatus()
        setInterval(this.retrieveUploadStatus, 5000)
    }

    render() {
        const {classes} = this.props;
        return (
            <div className={classes.upload_container}>
                <h2>Current upload status: {this.state.upload_status}</h2>
                <p style={{color: "#f0983a"}}>{this.state.upload_status_details}</p>
                <br />
                <p>We welcome new contributions of datasets of images with weeds already annotated.</p>
                <p>See <em>our guide</em> for collecting and annotating images.</p>
                <p>We support several standard formats of upload, accompanied with detailed metadata.</p>
                <br />
                <div style={{ display: 'flex', alignItems: 'center' }}>
                    <FormControl className={classes.formControl}>
                        <Select
                        value={this.state.upload_type}
                        displayEmpty
                        onChange={this.handleChange}
                        >
                            <MenuItem value="" disabled>
                                Select annotation format
                            </MenuItem>
                            <MenuItem value="weedcoco">WeedCOCO</MenuItem>
                            <MenuItem value="coco" disabled>COCO (not implemented)</MenuItem>
                            <MenuItem value="voc" disabled>VOC (not implemented)</MenuItem>
                            <MenuItem value="masks" disabled>Segmentation masks (not implemented)</MenuItem>
                        </Select>
                    </FormControl>
                    <UploadDialog handleUploadStatus={this.retrieveUploadStatus} uploadType={this.state.upload_type}/>
                </div>
            </div>
        )
    }
}

export default withStyles(useStyles)(UploadComponent);