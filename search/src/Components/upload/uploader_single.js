import React from 'react';
import 'react-dropzone-uploader/dist/styles.css';
import Dropzone from 'react-dropzone-uploader';
import Cookies from 'js-cookie'


const csrftoken = Cookies.get('csrftoken');

const UploaderSingle  = (props) => {
    const baseURL = new URL(window.location.origin);
    const getUploadParams = ({ file, meta }) => {
        const body = new FormData()
        body.append('weedcoco', file)
        return { url: baseURL + 'api/upload/',
                 headers: {'X-CSRFToken': csrftoken},
                 body
               }
    }
  
    const handleChangeStatus = ({ meta, file, xhr }, status) => {
        if (status === 'done'){
            const res = JSON.parse(xhr.response);
            props.handleUploadId(res.upload_id)
            props.handleImages(res.images)
        }
    }
  
    // const handleSubmit = (files, allFiles) => {
    //   files.map(f => f.restart())
    //   allFiles.forEach(f => f.remove())
    // }
  
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