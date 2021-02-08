import React from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import Dropzone from 'react-dropzone-uploader';
const yaml = require('js-yaml');

export default function UploadJsonButton({ onClose, initialValue, downloadName }) {
  const [open, setOpen] = React.useState(false);
  const [value, setValue] = React.useState(initialValue || '');
  const [errors, setErrors] = React.useState([]);
  const textAreaRef = React.createRef();

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleOkay = () => {
    onClose(value);
    handleClose()
  };

  const saveToPC = () => {
    const blob = new Blob([value], {type: "application/json"});
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.download = (downloadName || "form") + ".json";
    link.href = url;
    link.click();
  }

  const getTextArea = () => {
    return textAreaRef.current.getElementsByTagName('textarea')[0];
  }

  const handleCopy = (event) => {
    getTextArea().select();
    document.execCommand("copy");
  }

  const handleDownload = (event) => {
    saveToPC(value);
  }

  const handleDropzoneChangeStatus = (fileWithMeta, status) => {
    if (status !== 'done')
      return;
    const reader = new FileReader();
    const ta = getTextArea();
    setErrors([]);
    reader.onload = (e) => {
      try {
        const doc = yaml.load(e.target.result, {
          filename: fileWithMeta.meta.name,
          // TODO: handle onWarning to show messages
        })
        console.log(doc);
        const jsonDoc = JSON.stringify(doc, null, 2)
        setValue(jsonDoc);
        // HACK: this is bad ReactJS. What's the right way to do it?
        ta.value = jsonDoc;
      } catch (e) {
        setErrors(errors.concat([e.reason]));
        return;
      }
    }
    reader.readAsText(fileWithMeta.file)
  }


  return (
    <div>
      <Button variant="outlined" color="default" onClick={handleClickOpen}>
        Upload and Download Form Contents
      </Button>
      <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
        <DialogTitle id="form-dialog-title">Edit Form as JSON</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Upload from disk, or Copy/Paste JSON content below.
          </DialogContentText>
          { errors.length ? (
              <React.Fragment>
              <h3>Upload Errors:</h3>
              <ul>
              { errors.map((errorMessage) => (<li className="error"> { errorMessage } </li>)) }
              </ul>
              </React.Fragment>
            ) : []
          }
          <Dropzone
            onChangeStatus={handleDropzoneChangeStatus}
            maxFiles={1}
            multiple={false}
            maxSizeBytes={10 ** 7}
            canCancel={false}
            inputContent="Drop a JSON or YAML file"
            styles={{
              dropzone: { width: 400, height: 100 },
              dropzoneActive: { borderColor: 'green' },
            }}
          />
          <TextField
            autoFocus
            ref={textAreaRef}
            margin="dense"
            label="JSON data"
            defaultValue={initialValue}
            multiline={true}
            onChange={(e) => {setValue(e.target.value);}}
            fullWidth
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleDownload}>
            Download JSON
          </Button>
          <Button onClick={handleCopy}>
            Copy
          </Button>
        </DialogActions>
        <DialogActions>
          <Button onClick={handleClose}>
            Cancel
          </Button>
          <Button onClick={handleOkay}>
            Set Form
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

