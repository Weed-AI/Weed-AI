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
            autoProceed: false,
            debug: true,
            onBeforeUpload: (files) => {
                const updatedFiles = {};
                Object.keys(files).forEach(fileId => {
                    updatedFiles[fileId] = {
                        ...files[fileId],
                        name: `${props.upload_id}.${files[fileId].name}`
                    }
                    return updatedFiles;
                })
            }
        }).use(Tus, {
            endpoint: "http://localhost/api/upload_tus/",
            headers: {'X-CSRFToken': Cookies.get('csrftoken')},
            chunkSize: 1024 * 1024 * 10
        });
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
