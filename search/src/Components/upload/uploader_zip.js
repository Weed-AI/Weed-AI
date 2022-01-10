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

const TUS_ENDPOINT = 'http://localhost/tus/files/';


function getTusUploadFile(file) {
    console.log("getTusUploadFile");
    console.log(file);
    const url = file.tus.uploadUrl;
    if( url ) {
        const m = url.match(RegExp('^' + TUS_ENDPOINT + '(.*)$'));
        if( m ) {
            return m[1];
        }
    }
    return null;
}


class UploaderUppyZip extends React.Component {

    constructor(props) {
        super(props);
        
        const baseURL = new URL(window.location.origin);

        this.uppy = new Uppy({
            id: 'zipfiles',
            restrictions: {
                maxNumberOfFiles: 1,
                minNumberOfFiles: 1,
                allowedFileTypes: [ "application/zip" ],
            },
            autoProceed: false,
            debug: true,
            // onBeforeUpload: (files) => {
            //     const updatedFiles = {};
            //     console.log(`onBeforeUpload triggered, prepending upload_id ${props.upload_id}`);
            //     Object.keys(files).forEach(fileId => {
            //         console.log(`trying to reset filename for ${fileId}`);
            //         updatedFiles[fileId] = {
            //             ...files[fileId],
            //             meta: {
            //                 ...files[fileId].meta,
            //                 name: `${props.upload_id}.${files[fileId].name}`
            //             }
            //         }
            //     });
            //     return updatedFiles;
            // }
        }).use(Tus, {

            endpoint: TUS_ENDPOINT,
//            headers: {'X-CSRFToken': Cookies.get('csrftoken')},
            chunkSize: 1024 * 1024 * 10
        });
    }

    componentDidMount() {
        console.log('/-\ setting event handlers on uppy');

        this.uppy.on("upload", (data) => {
            console.log(">> from uppy event: upload");
            console.log(`upload_id = ${this.props.upload_id}`);
            console.log(data);
        })

        this.uppy.on("complete", (result) => {
            const baseURL = new URL(window.location.origin);
            console.log(">> from uppy event: complete");
            const files = result.successful;
            if( files.length === 1 ) {
                console.log("Calling unpack on backend");
                const filename = getTusUploadFile(files[0]);
                console.log(`upload file = ${filename}`);
                console.log(`upload_id = ${this.props.upload_id}`);
                if( filename ) {
                    const body = new FormData()
                    body.append("upload_id", this.props.upload_id);
                    body.append("images", this.props.images);
                    body.append("upload_image_zip", filename);
                    axios({
                        method: 'post',
                        url: baseURL + "api/unpack_image_zip_tus/",
                        data: body,
                        headers: {'X-CSRFToken': Cookies.get('csrftoken') }
                    }).then(res => {
                        console.log('got response from unpack');
                        console.log(res.data);
                        if( res.data.upload_id === this.props.upload_id ) {
                            if( res.data.missing_images.length === 0 ) {
                                this.props.handleValidation(true);
                                this.props.handleErrorMessage("");
                            } else {
                                this.props.handleValidation(false);
                                this.props.syncImageErrorMessage(res.data.missing_images)
                            }
                        } else {
                            this.props.handleValidation(false);
                            this.props.handleErrorMessage("Upload server error");
                        }
                    }).catch(err => {
                        this.props.handleValidation(false)
                        const data = err.response.data
                        if (typeof data === "object") this.props.handleErrorMessage(jsonSchemaTitle(data), data);
                        else this.props.handleErrorMessage(data || "Server error unpacking zipfile")
                    });
                } else {
                    console.log("Couldn't get filename from Uppy return value")
                    this.props.handleValidation(false);
                    this.props.handleErrorMessage("Upload zipfile failed");
                }
            } else {
                console.log("Got wrong number of successful uploaded files");
                this.props.handleValidation(false);
                this.props.handleErrorMessage("Upload zipfile failed");
            }
        })
    }

    componentWillUnmount() {
        this.uppy.close();
    }


    render() {
        return (
            <Dashboard
                uppy={this.uppy}
                locale={{
                    strings: {
                        dropHereOr: "Drop here or %{browse}",
                        browse: "browse",
                    },
                }}
            />
        )
    }

  
  }

  export default UploaderUppyZip;
