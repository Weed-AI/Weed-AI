import Uppy from '@uppy/core';
import '@uppy/core/dist/style.css';
import '@uppy/dashboard/dist/style.css';
import { Dashboard } from '@uppy/react';
import Tus from '@uppy/tus';
import axios from 'axios';
import Cookies from 'js-cookie';
import React from 'react';
import 'react-dropzone-uploader/dist/styles.css';
import { jsonSchemaTitle } from '../error/utils';


const baseURL = new URL(window.location.origin);


const TUS_ENDPOINT = baseURL + 'tus/files/';
const TUS_CHUNK_SIZE = 1024 * 1024 * 10;


function getTusUploadFile(file) {
    const url = file.tus.uploadUrl;
    if( url ) {
        const m = url.match(RegExp('^' + TUS_ENDPOINT + '(.*)$'));
        if( m ) {
            return m[1];
        }
    }
    return null;
}


const getZipUploadResponse = ({upload_id, images, filename}) => {
    return new Promise((resolve, reject) => {
        const pollPeriod = 200;
        const body = new FormData()
        body.append("upload_id", upload_id);
        body.append("images", images);
        body.append("upload_image_zip", filename);
        axios({
            method: 'post',
            url: baseURL + "api/unpack_image_zip/",
            data: body,
            headers: {'X-CSRFToken': Cookies.get('csrftoken') }
        }).then(res => {
            const taskId = res.data.task_id;
            const poll = () => {
                axios({
                    method: 'get',
                    url: baseURL + "api/check_image_zip/" + taskId,
                    headers: {'X-CSRFToken': Cookies.get('csrftoken') }
                }).then(res => {
                    if (res.status !== 200) {
                        // keep waiting
                        setTimeout(poll, pollPeriod)
                    } else {
                        resolve(res)
                    }
                }).catch(reject)
            }
            setTimeout(poll, pollPeriod);
        }).catch(reject)
    })
}

class UploaderUppyZip extends React.Component {

    constructor(props) {
        super(props);
        
        this.uppy = new Uppy({
            id: 'zipfiles',
            restrictions: {
                maxNumberOfFiles: 1,
                minNumberOfFiles: 1,
                allowedFileTypes: [ "application/zip" ],
            },
            autoProceed: true,
        }).use(Tus, {
            endpoint: TUS_ENDPOINT,
            withCredentials: true,
            headers: {'X-CSRFToken': Cookies.get('csrftoken')},
            chunkSize: TUS_CHUNK_SIZE
        });
    }

    componentDidMount() {

        this.uppy.on("complete", (result) => {
            const files = result.successful;
            if( files.length !== 1 ) {
                console.log("Got wrong number of successful uploaded files");
                this.props.handleValidation(false);
                this.props.handleErrorMessage("Upload zipfile failed");
                return;
            }
            const filename = getTusUploadFile(files[0]);
            if( !filename ) {
                console.log("Couldn't get filename from Uppy return value")
                this.props.handleValidation(false);
                this.props.handleErrorMessage("Upload zipfile failed");
                return;
            }
            getZipUploadResponse({ upload_id: this.props.upload_id, images: this.props.images, filename}).then(res => {
                if( res.data.upload_id === this.props.upload_id ) {
                    if( res.data.missing_image_amount === 0 ) {
                        this.props.handleValidation(true);
                        this.props.handleErrorMessage("");
                    } else {
                        this.props.handleValidation(false);
                        this.props.syncImageErrorMessage(res.data.uploaded_images)
                    }
                } else {
                    this.props.handleValidation(false);
                    this.props.handleErrorMessage("Upload server error");
                }
            }).catch(err => {
                this.props.handleValidation(false)
                const data = err.response.data
                if (typeof data === "object") this.props.handleErrorMessage(jsonSchemaTitle(data), data);
                else this.props.handleErrorMessage(data.length <= 100 ? data : null || "Server error unpacking zipfile")
            });
        })
    }

    componentWillUnmount() {
        this.uppy.close();
    }


    render() {
        return (
            <Dashboard
                uppy={this.uppy}
                height={200}
                proudlyDisplayPoweredByUppy={false}
                doneButtonHandler={null}
                locale={{
                    strings: {
                        dropPasteFiles: "%{browseFiles}",
                        browseFiles: "Drag Files or Click to Browse",
                    },
                }}
            />
        )
    }

  
  }

  export default UploaderUppyZip;
