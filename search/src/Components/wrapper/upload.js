import React, {Component} from 'react';
import UploadDialog from '../upload/upload_dialog';
import AuthPrompt from '../auth/auth_prompt';
import { withStyles } from '@material-ui/core/styles';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import axios from 'axios';
import Button from '@material-ui/core/Button';
import ReactMarkdown from "react-markdown";


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

const markdownContent = `
## Annotation Formats

We currently support uploads in MS COCO and [WeedCOCO](/weedcoco) formats.


We natively support WeedCOCO format which extends on MS COCO to specify a weed
ID-oriented category naming scheme, to include agricultural context and
[schema.org/Dataset](https://schema.org/Dataset)-compatible metadata. We provide an uploader
for MS COCO format, with forms to enter agricultural context and metadata
please ensure the category names are conformant before uploading.

We require that contributors license their images and annotations under the
liberal [CC-BY 4.0 licence](https://creativecommons.org/licenses/by/4.0/)
(Creative Commons Attribution Required). Uploaders must have the rights to the
content that they upload, and must agree to release their content (images and
annotations) under the terms of that licence.

In brief (and not a substitute for the License), the CC BY 4.0 License enables
users to freely share and adapt the material for any purpose, even
commercially, given appropriate attribution and that there are no additional
restrictions made.

## Data Quality Requirements

Submitted datasets that contain any of the following will be rejected by
dataset reviewers:

* Irrelevant images (such as non-weed or crop imagery)
*  Poor image quality (over/under exposed, blurry images)
* Unlabelled or poorly labelled data
* Images with personally identifiable content (such as faces and vehicle details)
* Images with explicit content

Currently only new images to the repository will be accepted.

## Upload Process

The uploading process is a five-step process:

1. Select the data annotation format above.
2. Upload the annotation file. Only COCO or WeedCOCO are supported currently. Please check that your images and annotations.
3. If not WeedCOCO, upload the AgContext file or generate a new one by completing the online form.
4. Include publication-level metadata about the dataset and how to attribute it.
5. Finally, upload the relevant images for the dataset

A Weed-AI administrator will review your submission. If the dataset is accepted
you will be notified and can continue uploading new datasets. The new dataset
will appear on the datasets page for other users to peruse.

Only one dataset per uploader can be in submission and review at any time.


`;

class UploadComponent extends Component {
    constructor(){
        super()
        this.state = {
            isLoggedIn: false,
            upload_status: "None",
            upload_status_details: "",
            upload_type: "",
        }
        this.handleChange = this.handleChange.bind(this);
        this.retrieveUploadStatus = this.retrieveUploadStatus.bind(this);
        this.handleLogin = this.handleLogin.bind(this);
        this.handleLogout = this.handleLogout.bind(this);
    }

    handleChange(event){
        this.setState({upload_type: event.target.value})
    };

    handleLogin(){
        this.setState({isLoggedIn: true})
        this.retrieveUploadStatus()
        this.intervalID = setInterval(this.retrieveUploadStatus, 5000)
        window.location.reload(false)
    }

    handleLogout(){
        axios.get(baseURL + "api/logout/")
        .then(res => {
            console.log(res)
            this.setState({isLoggedIn: false})
            clearInterval(this.intervalID)
        })
    }

    retrieveUploadStatus(){
        axios.get(baseURL + "api/upload_status/")
        .then(res => res.data)
        .then(json => {
            this.setState({upload_status: upload_status_mapping[json.upload_status],
                           upload_status_details: json.upload_status_details})
        })
        .catch(() => {
            this.setState({upload_status: "None",
                upload_status_details: ""})
        })
    }

    retrieveLoginStatus(){
        return new Promise((resolve, reject) => {
            axios.get(baseURL + "api/login_status/")
            .then(res => {
                if(res.status === 200){
                    this.setState({isLoggedIn: true})
                    resolve(true)
                }
            })
            .catch(err => {
                reject(false)
            })
        })
    }

    async componentDidMount(){
        const isLoggedIn = await this.retrieveLoginStatus()
        if(isLoggedIn){
            this.retrieveUploadStatus()
            setInterval(this.retrieveUploadStatus, 5000)
        }
    }

    render() {
        const {classes} = this.props;
        return (
            <div className={classes.upload_container}>
                <h1>Sign In and Upload</h1>
                <p>We welcome new contributions of datasets of images with weeds already annotated.</p>
                { this.state.isLoggedIn
                ?
                <React.Fragment>
                <div>
                    <h2>Current upload status: {this.state.upload_status}</h2>
                    <p style={{color: "#f0983a"}}>{this.state.upload_status_details}</p>
                    <Button variant="outlined" color="primary" onClick={this.handleLogout}>
                        Log out
                    </Button>
                </div>
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
                            <MenuItem value="coco">COCO</MenuItem>
                            <MenuItem value="voc" disabled>VOC (not implemented)</MenuItem>
                            <MenuItem value="masks" disabled>Segmentation masks (not implemented)</MenuItem>
                        </Select>
                    </FormControl>
                    <UploadDialog handleUploadStatus={this.retrieveUploadStatus} upload_type={this.state.upload_type}/>
                </div>
                </React.Fragment>
                :
                <AuthPrompt handleLogin={this.handleLogin} handleLogout={this.handleLogout}/> }

                <ReactMarkdown source={markdownContent} />
            </div>
        )
    }
}

export default withStyles(useStyles)(UploadComponent);
