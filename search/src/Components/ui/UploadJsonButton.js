import React from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';

export default function UploadJsonButton({ onClose, initialValue }) {
  const [open, setOpen] = React.useState(false);
  const [value, setValue] = React.useState(initialValue || '');

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

  return (
    <div>
      <Button variant="outlined" color="primary" onClick={handleClickOpen}>
        Upload
      </Button>
      <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
        <DialogTitle id="form-dialog-title">Upload JSON/YAML</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Paste content below.
          </DialogContentText>
          <TextField
            autoFocus
            margin="dense"
            label="JSON data"
            value={value}
            multiline={true}
            onChange={(e) => {setValue(e.target.value);}}
            fullWidth
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary">
            Cancel
          </Button>
          <Button onClick={handleOkay} color="primary">
            Okay
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

