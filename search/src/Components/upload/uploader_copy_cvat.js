import React from 'react';
import { useState, useEffect } from "react";
import CircularProgress from '@material-ui/core/CircularProgress';
import Button from '@material-ui/core/Button';
import axios from 'axios';
import Cookies from 'js-cookie';


const CopyCvatUploader = (props) => {
    const baseURL = new URL(window.location.origin);
    const { upload_id, cvat_task_id, images, handleValidation, handleErrorMessage } = props;
    const [loading, setLoading] = useState(false);
    const [copied, setCopied] = useState(false);
    const syncImageErrorMessage = updatedFilesName => {
        const missingImagesAmount = images.length - updatedFilesName.length;
        const missingImages = [...images].filter(image => !updatedFilesName.includes(image));
        if (missingImagesAmount == 0 && new Set(missingImages).size === 0) {
            handleValidation(true);
            handleErrorMessage("");
        } else {
            handleValidation(false);
            handleErrorMessage(`${missingImagesAmount} ${missingImagesAmount > 1 ? "images" : "image"} missing`, {error_type: "image", missingImages: missingImages});
        }
    }
    const copyCvatImage = () => {
        const body = new FormData()
        body.append('upload_id', upload_id)
        body.append('task_id', cvat_task_id)
        setLoading(true)
        axios({
            method: 'post',
            url: baseURL + "api/copy_cvat/",
            data: body,
            headers: {'Content-Type': 'multipart/form-data', 'X-CSRFToken': Cookies.get('csrftoken') }
        }).then(res => {
            const data = res.data
            if (data.upload_id === upload_id) {
                if (data.missing_images.length === 0) {
                    handleValidation(true)
                    handleErrorMessage("")
                } else {
                    syncImageErrorMessage(data.missing_images)
                }
                setCopied(true)
            }
        })
        .catch(err => {
            handleErrorMessage(err.responseText)
            handleValidation(false)
        })
        setLoading(false)
    }

    useEffect(() => {
        copyCvatImage()
    }, [])

    return (
        loading ?
        <CircularProgress/>
        :
        !copied?
        <Button 
            variant="contained"
            color="primary"
            onClick={copyCvatImage}>
        Copy from CVAT
        </Button>
        :
        ""
    )
}
export default CopyCvatUploader;