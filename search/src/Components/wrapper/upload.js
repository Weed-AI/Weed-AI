import React, {Component} from 'react';
import UploadDialog from '../upload/upload_dialog';
import AuthPrompt from '../auth/auth_prompt';
import { withStyles } from '@material-ui/core/styles';
import axios from 'axios';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import Paper from '@material-ui/core/Paper';
import content from './upload.md'
import { Helmet } from "react-helmet";
import { useArticleStyles } from '../../styles/common'
import Markdown from "../../Common/Markdown";

const PaddedPaper = withStyles((theme) => ({
    root: {
        padding: 8,
        marginBottom: 8,
    }
}))(Paper);

const useStyles = (theme) => ({
	...useArticleStyles(theme),
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
            isLoggedIn: false,
            upload_status: "None",
            upload_status_details: "",
        }
        this.retrieveUploadStatus = this.retrieveUploadStatus.bind(this);
        this.handleLogin = this.handleLogin.bind(this);
        this.handleLogout = this.handleLogout.bind(this);
    }

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

    componentWillMount() {
      fetch(content).then((response) => response.text()).then((text) => {
        this.setState({ markdownContent: text })
      })
    }

    async componentDidMount(){
        const isLoggedIn = await this.retrieveLoginStatus()
        if(isLoggedIn){
            this.retrieveUploadStatus()
            setInterval(this.retrieveUploadStatus, 50000)
        }
    }

    render() {
        const {classes} = this.props;
        return (
            <article className={classes.page}>
                <Helmet>
                    <title>Upload a dataset of weed imagery in crops - Weed-AI</title>
                    <meta name="description" content="Upload datasets of crop images annotated with weeds." />
                </Helmet>
                <h1>Sign In and Upload</h1>
                <p>We welcome new contributions of datasets of images with weeds already annotated.</p>
                { this.state.isLoggedIn
                ?
                <React.Fragment>
                <PaddedPaper elevation={2}>
                    <Typography gutterBottom variant="h6">Current upload status: {this.state.upload_status}</Typography>
                    <Typography variant="body1" style={{color: "#f0983a"}}>{this.state.upload_status_details}</Typography>
                </PaddedPaper>
                <div>
                    <UploadDialog handleUploadStatus={this.retrieveUploadStatus}/>
                    <Button variant="outlined" color="primary" onClick={this.handleLogout}>
                        Log out
                    </Button>
                </div>
                </React.Fragment>
                :
                <AuthPrompt handleLogin={this.handleLogin} handleLogout={this.handleLogout}/> }

                <Markdown source={this.state.markdownContent} />
            </article>
        )
    }
}

export default withStyles(useStyles)(UploadComponent);
