import React from 'react';
import 'react-dropzone-uploader/dist/styles.css';
import Dropzone from 'react-dropzone-uploader';
import {jsonSchemaTitle} from '../error/utils';
import axios from 'axios';
import Cookies from 'js-cookie';


const voc_max_size = 1024 * 100;
const UploaderVoc = (props) => {
    const baseURL = new URL(window.location.origin);

    const removeVoc = file => {
        const body = new FormData()
        body.append('voc_name', file.name)
        body.append('voc_id', props.voc_id)
        axios({
            method: 'post',
            url: baseURL + "api/remove_voc/",
            data: body,
            headers: {'Content-Type': 'multipart/form-data', 'X-CSRFToken': Cookies.get('csrftoken')}
        }).then(() => {
            props.handleErrorMessage("")
        })
    }

    const getUploadParams = ({ file, meta }) => {
        const body = new FormData()
        body.append('voc', file)
        body.append('voc_id', props.voc_id)
        return { url: baseURL + 'api/upload_voc/',
                 mode: 'same-origin',
                 headers: {'X-CSRFToken': Cookies.get('csrftoken')},
                 body
               }
    }
    
    const handleSubmit = (files, allFiles) => {
        const body = new FormData()
        body.append('voc_id', props.voc_id)
        axios({
            method: 'post',
            url: baseURL + "api/submit_voc/",
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

    const handleChangeStatus = ({ meta, file, xhr }, status) => {
      if (status === 'error_upload'){
          props.handleErrorMessage("Wrong file format")
          props.handleValidation(false)
      }
      else if (status === 'error_file_size') {
          props.handleErrorMessage("The file size exceeds the limitation")
          props.handleValidation(false)
      }
      else if (status === 'removed') {
          removeVoc(file)
      }
    }

    return (
      <Dropzone
        getUploadParams={getUploadParams}
        multiple={true}
        maxSizeBytes={voc_max_size}
        autoUpload={true}
        onChangeStatus={handleChangeStatus}
        onSubmit={handleSubmit}
        styles={{ dropzone: { minHeight: 200, maxHeight: 250 } }}
      />
    )
  }

  export default UploaderVoc;
