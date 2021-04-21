import React, { useState } from "react";
import ReactImageUploadComponent from './react-images-upload/index'


const UploaderImages = props => {
  const [pictures, setPictures] = useState([]);

  const onDrop = picture => {
    setPictures(picture);
  };

  const baseURL = new URL(window.location.origin);

  return (
        <ReactImageUploadComponent
            {...props}
            withPreview={true}
            onChange={onDrop}
            imgExtension={[".jpg", ".gif", ".png", ".jpeg", ".tif", ".tiff"]}
            maxFileSize={10485760}
            uploadURL={baseURL + 'api/upload_image/'}
        />
  );
};

export default UploaderImages;
