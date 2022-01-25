import React from 'react';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import UploaderImages from './uploader_images';
import UploaderZip from './uploader_zip';


const ImageOrZipUploader = (props) => {
    const { stepName, upload_id, images, handleValidation, handleErrorMessage } = props;
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
                            <MenuItem value="cvat">Load images from CVAT</MenuItem>
                        </Select>
                    </FormControl>
                    : ""
    return [uploader, select];
}
export default ImageOrZipUploader;