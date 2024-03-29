import axios from 'axios';
import Cookies from 'js-cookie';
import PropTypes from 'prop-types';
import React from 'react';
import FlipMove from 'react-flip-move';
import './index.css';


const styles = {
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  flexWrap: "wrap",
  width: "100%"
};

const ERROR = {
  NOT_SUPPORTED_EXTENSION: 'NOT_SUPPORTED_EXTENSION',
  FILESIZE_TOO_LARGE: 'FILESIZE_TOO_LARGE'
}

const preview_maximum = 100;

class ReactImageUploadComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      pictures: [...props.defaultImages],
      files: [],
      fileErrors: []
    };
    this.inputElement = '';
    this.onDropFile = this.onDropFile.bind(this);
    this.onUploadClick = this.onUploadClick.bind(this);
    this.triggerFileUpload = this.triggerFileUpload.bind(this);
    this.uploadFileToServer = this.uploadFileToServer.bind(this);
  }

  componentDidUpdate(prevProps, prevState, snapshot){
    if(prevState.files !== this.state.files){
      this.props.onChange(this.state.files, this.state.pictures);
    }
  }

  /*
   Load image at the beggining if defaultImage prop exists
   */
  componentWillReceiveProps(nextProps){
    if(nextProps.defaultImages !== this.props.defaultImages){
      this.setState({pictures: nextProps.defaultImages});
    }
  }

  /*
	 Check file extension (onDropFile)
	 */
  hasExtension(fileName) {
    const pattern = '(' + this.props.imgExtension.join('|').replace(/\./g, '\\.') + ')$';
    return new RegExp(pattern, 'i').test(fileName);
  }

  /*
   Handle file validation
   */
  onDropFile(e) {
    const files = e.target.files;
    const fileErrors = [];
    const filesName = (this.state.files || []).map(file => file.name);

    // Iterate over all uploaded files
    for (let i = 0; i < files.length; i++) {
      let file = files[i];
      let fileError = {
        name: file.name,
      };
      // Check for duplication
      if (this.props.images && !this.props.images.includes(file.name) || filesName.includes(file.name)){
        continue;
      }
      // Check for file extension
      if (!this.hasExtension(file.name)) {
        fileError = Object.assign(fileError, {
          type: ERROR.NOT_SUPPORTED_EXTENSION
        });
        fileErrors.push(fileError);
        continue;
      }
      // Check for file size
      if(file.size > this.props.maxFileSize) {
        fileError = Object.assign(fileError, {
          type: ERROR.FILESIZE_TOO_LARGE
        });
        fileErrors.push(fileError);
        continue;
      }
      this.readFile(file).then(newFileData => {
        this.uploadFileToServer(newFileData);
      });
    }
    this.setState({fileErrors});
  }

  /*
     Customised function modified on original codebase
     Copyright (c) 2020 Zheng Li
   */
  uploadFileToServer(newFileData) {
      const {singleImage} = this.props;
      const body = new FormData()
      body.append('upload_image', newFileData.file)
      body.append(this.props.idName ? this.props.idName : "upload_id", this.props.upload_id)
      axios({
          method: 'post',
          url: this.props.uploadURL,
          data: body,
          headers: {'Content-Type': 'multipart/form-data', 'X-CSRFToken': Cookies.get('csrftoken') }
      }).then(res => {
          if(res.status === 200){
            const dataURLs = singleImage?[]:this.state.pictures.slice();
            const files = singleImage?[]:this.state.files.slice();
            const filesName = files.map(file => file.name);
            if (!filesName.includes(newFileData.file.name)){
                dataURLs.push(newFileData.dataURL);
                files.push(newFileData.file);
                this.setState({pictures: dataURLs, files: files});
                if (this.props.handleUploaded) this.props.handleUploaded(files.map(file => file.name));
            }
          }
      })
      
  }

  onUploadClick(e) {
    // Fixes https://github.com/JakeHartnell/react-images-upload/issues/55
    e.target.value = null;
  }

  /*
     Read a file and return a promise that when resolved gives the file itself and the data URL
   */
  readFile(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();

      // Read the image via FileReader API and save image result in state.
      reader.onload = function (e) {
        // Add the file name to the data URL
        let dataURL = e.target.result;
        dataURL = dataURL.replace(";base64", `;name=${file.name};base64`);
        resolve({file, dataURL});
      };

      reader.readAsDataURL(file);
    });
  }

  /*
   Remove the image from state
   */
  removeImage(picture) {
    const removeIndex = this.state.pictures.findIndex(e => e === picture);
    const removeImageName = this.state.files[removeIndex].name;
    const filteredPictures = this.state.pictures.filter((e, index) => index !== removeIndex);
    const filteredFiles = this.state.files.filter((e, index) => index !== removeIndex);

    this.setState({pictures: filteredPictures, files: filteredFiles}, () => {
      this.props.onChange(this.state.files, this.state.pictures);
    });
    if (this.props.handleUploaded) this.props.handleUploaded(filteredFiles.map(file => file.name));
    if (this.props.removeURL) {
      const body = new FormData()
      body.append('image_name', removeImageName)
      body.append(this.props.idName ? this.props.idName : "upload_id", this.props.upload_id)
      axios({
          method: 'post',
          url: this.props.removeURL,
          data: body,
          headers: {'Content-Type': 'multipart/form-data', 'X-CSRFToken': Cookies.get('csrftoken')}
      }).then(() => {
          this.props.handleErrorMessage("")
      })
    }
  }

  /*
   Check if any errors && render
   */
  renderErrors() {
    const { fileErrors } = this.state;
    return fileErrors.map((fileError, index) => {
      return (
        <div className={'errorMessage ' + this.props.errorClass} key={index} style={this.props.errorStyle}>
          * {fileError.name} {fileError.type === ERROR.FILESIZE_TOO_LARGE ? this.props.fileSizeError : fileError.type === ERROR.NOT_SUPPORTED_EXTENSION ? this.props.fileTypeError : this.props.fileDuplicateError}
        </div>
      );
    });
  }

  /*
   Render label
   */
  renderLabel() {
    if (this.props.withLabel) {
      return <p className={this.props.labelClass} style={this.props.labelStyles}>{this.props.label}</p>
    }
  }

  /*
   Render preview images
   */
  renderPreview() {
    return (
      <div className="uploadPicturesWrapper">
        <FlipMove enterAnimation="fade" leaveAnimation="fade" style={styles}>
          {this.renderPreviewPictures()}
        </FlipMove>
      </div>
    );
  }

  renderPreviewPictures() {
    return this.state.pictures.length <= preview_maximum ?
    this.state.pictures.map((picture, index) => {
      return (
        <div key={index} className="uploadPictureContainer">
          {/* <div className="deleteImage" onClick={() => this.removeImage(picture)}>X</div> */}
          <div style={{display: 'flex', flexDirection: 'column', width: '100%', overflowWrap: 'anywhere'}}>
            <img src={picture} className="uploadPicture" alt="preview"/>
            <p>{this.state.files[index].name}</p>
          </div>
        </div>
      );
    })
    :
    <p>No preview available over {preview_maximum} images</p>
  }

  /*
   On button click, trigger input file to open
   */
  triggerFileUpload() {
    this.inputElement.click();
  }

  clearPictures() {
    this.setState({pictures: []})
  }

  render() {
    return (
      <div className={"fileUploader " + this.props.className} style={this.props.style}>
        <div className="fileContainer" style={this.props.fileContainerStyle}>
          {this.renderLabel()}
          <div className="errorsContainer">
            {this.renderErrors()}
          </div>
          <button
            type={this.props.buttonType}
            className={"chooseFileButton " + this.props.buttonClassName}
            style={this.props.buttonStyles}
            onClick={this.triggerFileUpload}
          >
            {this.props.buttonText}
          </button>
          <input
            type="file"
            ref={input => this.inputElement = input}
            name={this.props.name}
            multiple={!this.props.singleImage}
            onChange={this.onDropFile}
            onClick={this.onUploadClick}
            accept={this.props.accept}
          />
          { this.props.withPreview ? this.renderPreview() : null }
        </div>
      </div>
    )
  }
}

ReactImageUploadComponent.defaultProps = {
  className: '',
  fileContainerStyle: {},
  buttonClassName: "",
  buttonStyles: {},
  withPreview: false,
  accept: "image/*",
  name: "",
  withIcon: true,
  buttonText: "Choose images",
  buttonType: "button",
  withLabel: true,
  label: "Max file size: 5 MB | File types accepted: .jpg, .gif, .png, .tif",
  labelStyles: {},
  labelClass: "",
  imgExtension: ['.jpg', '.jpeg', '.gif', '.png'],
  maxFileSize: 5242880,
  fileSizeError: " file size is too big",
  fileTypeError: " is not a supported file extension",
  fileDuplicateError: " is a duplicate file",
  errorClass: "",
  style: {},
  errorStyle: {},
  singleImage: false,
  onChange: () => {},
  defaultImages: []
};

ReactImageUploadComponent.propTypes = {
  style: PropTypes.object,
  fileContainerStyle: PropTypes.object,
  className: PropTypes.string,
  onChange: PropTypes.func,
  onDelete: PropTypes.func,
  buttonClassName: PropTypes.string,
  buttonStyles: PropTypes.object,
  buttonType: PropTypes.string,
  withPreview: PropTypes.bool,
  accept: PropTypes.string,
  name: PropTypes.string,
  withIcon: PropTypes.bool,
  buttonText: PropTypes.string,
  withLabel: PropTypes.bool,
  label: PropTypes.string,
  labelStyles: PropTypes.object,
  labelClass: PropTypes.string,
  imgExtension: PropTypes.array,
  maxFileSize: PropTypes.number,
  fileSizeError: PropTypes.string,
  fileTypeError: PropTypes.string,
  fileDuplicateError: PropTypes.string,
  errorClass: PropTypes.string,
  errorStyle: PropTypes.object,
  singleImage: PropTypes.bool,
  defaultImages: PropTypes.array
};

export default ReactImageUploadComponent;
