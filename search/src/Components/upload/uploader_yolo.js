import React from 'react';
import 'react-dropzone-uploader/dist/styles.css';
import Dropzone from 'react-dropzone-uploader';
import {jsonSchemaTitle} from '../error/utils';
import axios from 'axios';
import Cookies from 'js-cookie';

const UploaderYolo = (props) => {
    const baseURL = new URL(window.location.origin);

    const removeYoloFile = file => {
        const body = new FormData()
        body.append('yolo_filename', file.name)
        body.append('yolo_id', props.yolo_id)
        axios({
            method: 'post',
            url: baseURL + "api/remove_yolo/",
            data: body,
            headers: {'Content-Type': 'multipart/form-data', 'X-CSRFToken': Cookies.get('csrftoken')}
        }).then(() => {
            props.handleErrorMessage("")
        })
    }

    const getUploadParams = ({ file, meta }) => {
        const body = new FormData()
        body.append('yolo_file', file)
        body.append('yolo_id', props.yolo_id)
        return {
            url: baseURL + 'api/upload_yolo/',
            mode: 'same-origin',
            headers: {'X-CSRFToken': Cookies.get('csrftoken')},
            body
        }
    }

    const handleSubmit = (files, allFiles) => {
        const body = new FormData()
        body.append('yolo_id', props.yolo_id)
        body.append('upload_id', props.upload_id)
        axios({
            method: 'post',
            url: baseURL + "api/submit_yolo/",
            data: body,
            headers: {'Content-Type': 'multipart/form-data', 'X-CSRFToken': Cookies.get('csrftoken')}
        }).then(res => {
            res = res.data
            props.handleUploadId(res.upload_id)
            props.handleImages(res.images)
            props.handleCategories(res.categories)
            props.handleValidation(true)
            props.handleErrorMessage("")
        }).catch(err => {
            const res = err.response
            props.handleValidation(false)
            try {
                res = JSON.parse(res.data)
                props.handleErrorMessage(jsonSchemaTitle(res), res)
            } catch (e) {
                props.handleErrorMessage(res.data)
            }
        })
    }

    const handleChangeStatus = ({ meta, file }, status) => {
      if (status === 'error_upload'){
          props.handleErrorMessage("Error during upload")
          props.handleValidation(false)
      } else if (status === 'removed') {
          removeYoloFile(file)
      }
    }

    return (
      <Dropzone
        getUploadParams={getUploadParams}
        multiple={true}
        autoUpload={true}
        onChangeStatus={handleChangeStatus}
        onSubmit={handleSubmit}
        accept=".txt,.yaml"
        inputContent="Drop .txt annotation files and the data.yaml file"
        styles={{ dropzone: { minHeight: 200, maxHeight: 250 } }}
      />
    )
  }

  export default UploaderYolo;