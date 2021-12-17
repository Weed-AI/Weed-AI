import React from 'react';
import Button from '@material-ui/core/Button';

import 'react-dropzone-uploader/dist/styles.css';
import Dropzone from 'react-dropzone-uploader';
import Cookies from 'js-cookie';

import Uppy from '@uppy/core';
import '@uppy/core/dist/style.css';
import '@uppy/dashboard/dist/style.css';
import Tus from '@uppy/tus';
import { Dashboard, useUppy } from '@uppy/react';





const UploaderZip  = props => {
    const baseURL = new URL(window.location.origin);

    const uppy = useUppy(() => {
        return new Uppy({
            id: 'uppy',
            autoProceed: false,
            debug: true,
        }).use(Tus, {
            endpoint: "http://localhost/api/upload_tus/",
            headers: {'X-CSRFToken': Cookies.get('csrftoken')},
            chunkSize: 1024 * 1024 * 10
        });
    })

    uppy.on('complete', (result) => {
        console.log("upload complete")
    });

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
  
    const handleChangeStatus = ({ meta, file, xhr }, status) => {
        if (status === 'done'){
            const res = JSON.parse(xhr.response)
            if (res.upload_id === props.upload_id) {
                if (res.missing_images.length === 0) {
                    props.handleValidation(true)
                    props.handleErrorMessage("")
                } else {
                    props.syncImageErrorMessage(res.missing_images)
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
        <Dashboard
            id="uppy"
            width="750"
            height="250"
            uppy={uppy}
            locale={{
                strings: {
                    dropHereOr: "Drop here or %{browse}",
                    browse: "browse",
                },
            }}
        />
    )

  
    // return (
    //   <Dropzone
    //     getUploadParams={getUploadParams}
    //     onChangeStatus={handleChangeStatus}
    //     multiple={false}
    //     maxFiles={1}
    //     accept=".zip"
    //     autoUpload={true}
    //     submitButtonContent={null}
    //     styles={{ dropzone: { minHeight: 200, maxHeight: 250 } }}
    //   />
    // )
  }

  export default UploaderZip;
