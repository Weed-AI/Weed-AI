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
            imgExtension={[".jpg", ".gif", ".png", ".gif"]}
            maxFileSize={5242880}
            uploadURL={baseURL + 'api/upload_image/'}
        />
  );
};

export default UploaderImages;