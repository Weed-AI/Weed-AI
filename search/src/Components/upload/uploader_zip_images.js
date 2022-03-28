import FormControl from '@material-ui/core/FormControl';
import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';
import React from 'react';
import UploaderImages from './uploader_images';
import UploaderUppyZip from './uploader_zip';


const ImageOrZipUploader = (props) => {
    const { stepName, upload_id, images, handleValidation, handleErrorMessage } = props;
    const [uploadImageFormat, setUploadImageFormat] = React.useState("image")
    const handleUploadImageFormat = (event) => {
        setUploadImageFormat(event.target.value)
    };
    const syncImageErrorMessage = updatedFilesName => {
        const missingImages = [...images].filter(image => !updatedFilesName.includes(image));
        props.handleImages(missingImages);
        props.handleMissingImages(missingImages);
    }
    const uploader = stepName !== "images" ?
                    ""
                    :
                    uploadImageFormat == "image" ?
                    <UploaderImages upload_id={upload_id} images={images} handleValidation={handleValidation} handleErrorMessage={handleErrorMessage} syncImageErrorMessage={syncImageErrorMessage}/>
                    :
                    <UploaderUppyZip upload_id={upload_id} images={images} handleValidation={handleValidation} handleErrorMessage={handleErrorMessage} syncImageErrorMessage={syncImageErrorMessage}/>
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
    return [uploader, select];
}
export default ImageOrZipUploader;