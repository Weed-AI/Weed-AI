import React from 'react';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import UploaderImages from './uploader_images';
import UploaderZip from './uploader_zip';
import Button from '@material-ui/core/Button';
import axios from 'axios';
import Cookies from 'js-cookie';


const ImageOrZipUploader = (props) => {
    const baseURL = new URL(window.location.origin);
    const { stepName, upload_id, cvat_task_id, images, handleValidation, handleErrorMessage } = props;
    const [uploadImageFormat, setUploadImageFormat] = React.useState("image")
    const handleUploadImageFormat = (event) => {
        setUploadImageFormat(event.target.value)
    };
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
            }
        })
        .catch(err => {
            handleErrorMessage(err.responseText);
            handleValidation(false)
        })
    }
    const uploader = stepName !== "images" ?
                    ""
                    :
                    uploadImageFormat == "image" ?
                    <UploaderImages upload_id={upload_id} images={images} handleValidation={handleValidation} handleErrorMessage={handleErrorMessage} syncImageErrorMessage={syncImageErrorMessage}/>
                    :
                    <UploaderZip upload_id={upload_id} images={images} handleValidation={handleValidation} handleErrorMessage={handleErrorMessage} syncImageErrorMessage={syncImageErrorMessage}/>
    const select = stepName === "images" ?
                    <FormControl>
                        <Select
                        value={uploadImageFormat}
                        displayEmpty
                        onChange={handleUploadImageFormat}
                        >
                            <MenuItem value="" disabled>
                                Select upload format
                            </MenuItem>
                            <MenuItem value="image">Upload Image Files</MenuItem>
                            <MenuItem value="zip">Upload Images in Zip</MenuItem>
                        </Select>
                    </FormControl>
                    : ""
    const copy_cvat = cvat_task_id !== 0 ?
                    <Button 
                        variant="contained"
                        color="primary"
                        style={{float: 'right'}}
                        onClick={copyCvatImage}>
                    Copy from CVAT
                    </Button>
                    : ""
    return [uploader, select, copy_cvat];
}
export default ImageOrZipUploader;