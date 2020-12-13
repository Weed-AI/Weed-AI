import React from 'react';
import 'react-dropzone-uploader/dist/styles.css';
import Dropzone from 'react-dropzone-uploader';
import axios from 'axios';


const Preview = ({ meta }) => {
    const { name, percent, status } = meta
    return (
      <span style={{ alignSelf: 'flex-start', margin: '10px 3%', fontFamily: 'Helvetica' }}>
        {name}, {Math.round(percent)}%, {status}
      </span>
    )
}

const UploaderMultiple = (props) => {
    const baseURL = new URL(window.location.origin);
    const getUploadParams = ({ file, meta }) => {
        const body = new FormData()
        body.append('upload_image', file)
        body.append('upload_id', props.upload_id)
        return { url: baseURL + 'api/upload_image/', body }
    }
  
    const handleChangeStatus = ({ meta }, status) => {
    }
  
    const handleSubmit = (files, allFiles) => {
        const body = new FormData()
        body.append('upload_id', props.upload_id)
        axios({
            method: 'post',
            url: baseURL + "api/submit_deposit/",
            data: body,
            headers: {'Content-Type': 'multipart/form-data' }
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
        PreviewComponent={Preview}
        styles={{ dropzone: { minHeight: 200, maxHeight: 250 } }}
      />
    )
  }

  export default UploaderMultiple;