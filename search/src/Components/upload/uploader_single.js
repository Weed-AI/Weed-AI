import React from 'react';
import 'react-dropzone-uploader/dist/styles.css';
import Dropzone from 'react-dropzone-uploader';
import Cookies from 'js-cookie'


const csrftoken = Cookies.get('csrftoken');

function readBody(xhr) {
    var data;
    if (!xhr.responseType || xhr.responseType === "text") {
        data = xhr.responseText;
    } else if (xhr.responseType === "document") {
        data = xhr.responseXML;
    } else {
        data = xhr.response;
    }
    return data;
}

const UploaderSingle  = (props) => {
    const baseURL = new URL(window.location.origin);
    const getUploadParams = ({ file, meta }) => {
        const body = new FormData()
        body.append('weedcoco', file)
        return { url: baseURL + 'api/upload/',
                 mode: 'same-origin',
                 headers: {'X-CSRFToken': csrftoken},
                 body
               }
    }
  
    const handleChangeStatus = ({ meta, file, xhr }, status) => {
        if (status === 'done'){
            const res = JSON.parse(xhr.response)
            props.handleUploadId(res.upload_id)
            props.handleImages(res.images)
            props.handleErrorMessage("")
        }
        else if (status === 'error_upload'){
            // Weird things happen here
            props.handleErrorMessage("There is something wrong with the file")
        }
        else if (status === 'error_file_size') {
            props.handleErrorMessage("The file size exceeds the limitation")
        }
        else if (status === 'removed') {
            props.handleErrorMessage("")
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