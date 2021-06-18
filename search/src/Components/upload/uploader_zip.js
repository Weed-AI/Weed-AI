import React from 'react';
import 'react-dropzone-uploader/dist/styles.css';
import Dropzone from 'react-dropzone-uploader';
import Cookies from 'js-cookie';


const UploaderZip  = props => {
    const baseURL = new URL(window.location.origin);
    const getUploadParams = ({ file, meta }) => {
        const body = new FormData()
        body.append('upload_id', props.upload_id)
        body.append('images', props.images)
        body.append('upload_image_zip', file)
        return { url: baseURL + 'api/upload_image_zip/',
                 mode: 'same-origin',
                 headers: {'X-CSRFToken': Cookies.get('csrftoken')},
                 body
               }
    }

    const syncImageErrorMessage = missingImages => {
        const missingImagesAmount = missingImages.length;
        if (missingImagesAmount == 0 && new Set(missingImages).size === 0) {
            props.handleValidation(true);
            props.handleErrorMessage("");
        } else {
            props.handleValidation(false);
            props.handleErrorMessage(`${missingImagesAmount} ${missingImagesAmount > 1 ? "images" : "image"} missing`, {error_type: "image", missingImages: missingImages});
        }
    }
  
    const handleChangeStatus = ({ meta, file, xhr }, status) => {
        if (status === 'done'){
            const res = JSON.parse(xhr.response)
            if (res.upload_id === props.upload_id) {
                if (res.missing_images.length === 0) {
                    props.handleValidation(true)
                    props.handleErrorMessage("")
                } else {
                    syncImageErrorMessage(res.missing_images)
                }
            }
        }
        else if (status === 'error_upload'){
            xhr.addEventListener('loadend', 
              (e) => {
                const res = e.target.responseText;
                props.handleErrorMessage(res);
                props.handleValidation(false)
              });
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

  export default UploaderZip;
