import React, { useState } from "react";
import ReactImageUploadComponent from './react-images-upload/index';


const UploaderImages = props => {
  const [pictures, setPictures] = useState([]);

  const onDrop = picture => {
    setPictures(picture);
  };

  const syncImageErrorMessage = updatedFilesName => {
    const missingImagesAmount = props.images.length - updatedFilesName.length;
    const missingImages = [...props.images].filter(image => !updatedFilesName.includes(image));
    if (missingImagesAmount == 0 && new Set(missingImages).size === 0) {
        props.handleValidation(true);
        props.handleErrorMessage("");
    } else {
        props.handleValidation(false);
        props.handleErrorMessage(`${missingImagesAmount} ${missingImagesAmount > 1 ? "images" : "image"} missing`, {error_type: "image", missingImages: missingImages});
    }
  }

  const baseURL = new URL(window.location.origin);

  return (
        <ReactImageUploadComponent
            {...props}
            idName={"upload_id"}
            withPreview={true}
            onChange={onDrop}
            imgExtension={[".jpg", ".gif", ".png", ".jpeg", ".tif", ".tiff"]}
            maxFileSize={10485760}
            label={"Max file size: 10 MB | File types accepted: .jpg, .gif, .png, .jpeg, .tif, .tiff"}
            uploadURL={baseURL + 'api/upload_image/'}
            handleUploaded={syncImageErrorMessage}
        />
  );
};

export default UploaderImages;
