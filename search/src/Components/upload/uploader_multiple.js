import React from 'react';
import 'react-dropzone-uploader/dist/styles.css';
import Dropzone from 'react-dropzone-uploader';
import axios from 'axios';


const UploaderMultiple = (props) => {
    const esURL = new URL(window.location.origin);
    const baseURL = new URL(window.location.origin);
    const getUploadParams = ({ file, meta }) => {
        const body = new FormData()
        body.append('upload_image', file)
        body.append('upload_id', props.upload_id)
        return { url: baseURL + 'api/upload_image/', body }
    }
  
    const handleChangeStatus = ({ meta }, status) => {
        console.log(status, meta)
    }
  
    const handleSubmit = (files, allFiles) => {
        const body = new FormData()
        body.append('upload_id', props.upload_id)
        axios({
            method: 'post',
            url: esURL + "api/submit_deposit/",
            data: body,
            headers: {'Content-Type': 'multipart/form-data' }
        })
        .then(res => {
            console.log(res);
        })
    }
    
    const handleValidate = ({ meta }) => {
        return !props.images.includes(meta.name)
    }

    return (
      <Dropzone
        getUploadParams={getUploadParams}
        onChangeStatus={handleChangeStatus}
        onSubmit={handleSubmit}
        validate={handleValidate}
        styles={{ dropzone: { minHeight: 200, maxHeight: 250 } }}
      />
    )
  }

  export default UploaderMultiple;