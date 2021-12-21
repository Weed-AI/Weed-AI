import React, { useEffect } from 'react';

import 'react-dropzone-uploader/dist/styles.css';
import Dropzone from 'react-dropzone-uploader';
import Cookies from 'js-cookie';

import axios from 'axios';

import Uppy from '@uppy/core';
import '@uppy/core/dist/style.css';
import '@uppy/dashboard/dist/style.css';
import Tus from '@uppy/tus';
import { Dashboard, useUppy } from '@uppy/react';

import {jsonSchemaTitle} from '../error/utils';


// note - the uppy.on complete needs to be able to get the propertis
// for the component so that it knows the uploadId - plus how do I
// get those to the onBeforeUpload hook?

const uppy = new Uppy({
    id: 'zipfiles',
    restrictions: {
        maxNumberOfFiles: 1,
        minNumberOfFiles: 1,
        allowedFileTypes: [ "application/zip" ],
    },
    autoProceed: false,
    debug: true,
    onBeforeUpload: (files) => {
        const updatedFiles = {};
        Object.keys(files).forEach(fileId => {
            updatedFiles[fileId] = {
                ...files[fileId],
                name: `prefix.${files[fileId].name}`
            }
            return updatedFiles;
        })
    }
}).use(Tus, {
    endpoint: "http://localhost/api/upload_tus/",
    headers: {'X-CSRFToken': Cookies.get('csrftoken')},
    chunkSize: 1024 * 1024 * 10
});





const UploaderZip  = props => {
    const baseURL = new URL(window.location.origin);


    useEffect(() => {
        const handler = (status, event) => {
            props.handleTusUpload(event.body);
        };
        uppy.on('complete', handler);
        // Tell React to remove the old listener if a different function is passed to the `handleFileUploaded` prop:
        return () => {
            uppy.off('complete', handler);
        };
    }, [props.handleTusUpload]);




    // const getUploadParams = ({ file, meta }) => {
    //     const body = new FormData()
    //     body.append('upload_id', props.upload_id)
    //     body.append('images', props.images)
    //     body.append('upload_image_zip', file)
    //     return { url: baseURL + 'api/upload_image_zip/',
    //              mode: 'same-origin',
    //              headers: {'X-CSRFToken': Cookies.get('csrftoken')},
    //              body
    //            }
    // }
  
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

    // note - this is still setting too many listeners.
    // see https://github.com/transloadit/uppy/issues/2692

    uppy.once('complete', result => {
        console.log("upload complete");
        // console.log("successful files", result.successful)
        // console.log("failed files", result.failed);
        const files = result.successful;
        if( files.length === 1 ) {
            console.log("NOT Calling unpack on backend");
            console.log(files[0]);
        // axios({
        //     method: 'post',
        //     url: baseURL + "api/unpack_image_zip_tus/",
        //     data: {
        //         "upload_image_zip": files[0],
        //     },
        //     headers: {'X-CSRFToken': Cookies.get('csrftoken') }
        // }).then(res => {
        //     if( res.upload_id === props.upload_id ) {
        //         if( res.missing_images.length === 0 ) {
        //             props.handleValidation(true);
        //             props.handleErrorMessage("");
        //         } else {
        //             props.syncImageErrorMessage(res.missing_images)
        //         }
        //     }
        // }).catch(err => {
        //     props.handleValidation(false)
        //     const data = err.response.data
        //     if (typeof data === "object") props.handleErrorMessage(jsonSchemaTitle(data), data);
        //     else props.handleErrorMessage(data || "Server error unpacking zipfile")
        // });
        } else {
            console.log("Got wrong number of successful uploaded files");
        // props.handleValidation(false);
        // props.handleErrorMessage("Upload zipfile failed");
        }
    })


    return (
        <Dashboard
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
