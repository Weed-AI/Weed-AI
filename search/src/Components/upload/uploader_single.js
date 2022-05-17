import Cookies from 'js-cookie';
import React from 'react';
import Dropzone from 'react-dropzone-uploader';
import 'react-dropzone-uploader/dist/styles.css';
import { jsonSchemaTitle } from '../error/utils';


const UploaderSingle  = (props) => {
    const baseURL = new URL(window.location.origin);
    const getUploadParams = ({ file, meta }) => {
        const body = new FormData()
        body.append('weedcoco', file)
        body.append('upload_mode', props.upload_mode)
        body.append('upload_id', props.upload_id)
        body.append('schema', props.schema)
        return { url: baseURL + 'api/upload/',
                 mode: 'same-origin',
                 headers: {'X-CSRFToken': Cookies.get('csrftoken')},
                 body
               }
    }
  
    const handleChangeStatus = ({ meta, file, xhr }, status) => {
        if (status === 'done'){
            const res = JSON.parse(xhr.response)
            props.handleUploadId(res.upload_id)
            props.handleImages(res.images)
            props.handleCategories(res.categories)
            props.handleValidation(true)
            props.handleErrorMessage("")
        }
        else if (status === 'error_upload'){
            xhr.addEventListener('loadend', 
              (e) => {
                const res = JSON.parse(e.target.responseText);
                props.handleErrorMessage(jsonSchemaTitle(res), res);
                props.handleValidation(false)
              });
        }
        else if (status === 'error_file_size') {
            props.handleValidation(false)
            props.handleErrorMessage("The file size exceeds the limitation")
        }
        else if (status === 'removed') {
            props.handleValidation(false)
            props.handleErrorMessage("")
        }
    }
  
    return (
      <Dropzone
        getUploadParams={getUploadParams}
        onChangeStatus={handleChangeStatus}
        multiple={false}
        maxFiles={1}
        autoUpload={true}
        submitButtonContent={null}
        styles={{ dropzone: { minHeight: 200, maxHeight: 250 } }}
      />
    )
  }

  export default UploaderSingle;
