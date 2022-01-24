import React from 'react';
import 'react-dropzone-uploader/dist/styles.css';
import Cookies from 'js-cookie';
import axios from 'axios';


class UploaderCvat extends React.Component {

    constructor(props) {
        super(props);
        this.state = { task_id: '' };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }
    
    handleChange(event) {
        this.setState({task_id: event.target.value});
    }

    handleSubmit(event) {
        const baseURL = new URL(window.location.origin);
        const body = new FormData();
        body.append('upload_id', this.props.upload_id);
        body.append('task_id', this.state.task_id);

        event.preventDefault();

        axios({
            method: 'post',
            url: baseURL + "api/copy_cvat/",
            data: body,
            headers: {'Content-Type': 'multipart/form-data', 'X-CSRFToken': Cookies.get('csrftoken')}
        }).then(res => {
            const jres = JSON.parse(res)
            if (jres.upload_id === this.props.upload_id) {
                if (jres.missing_images.length === 0) {
                    this.props.handleValidation(true)
                    this.props.handleErrorMessage("")
                } else {
                    this.props.syncImageErrorMessage(jres.missing_images)
                }
            }
            this.props.handleResult("")
        }).catch(err => {
            const res = err.response
            this.props.handleValidation(false)
            this.props.handleErrorMessage(res.data)
        })

    }

    render() {
        return (
      <form onSubmit={this.handleSubmit}>
      <input name="task_id" type="text" value={this.state.task_id} onChange={this.handleChange} />
      <input type="submit" value="Copy from CVAT" />
      </form>
        )
    }
}


  export default UploaderCvat;
