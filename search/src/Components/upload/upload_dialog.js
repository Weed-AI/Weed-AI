import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import MuiDialogContent from '@material-ui/core/DialogContent';
import MuiDialogTitle from '@material-ui/core/DialogTitle';
import IconButton from '@material-ui/core/IconButton';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import CloseIcon from '@material-ui/icons/Close';
import EditIcon from '@material-ui/icons/Edit';
import axios from 'axios';
import React from 'react';
import UploadSteper from './upload_stepper';

const styles = (theme) => ({
  root: {
    margin: 0,
    padding: theme.spacing(2),
  },
  closeButton: {
    position: 'absolute',
    right: theme.spacing(1),
    top: theme.spacing(1),
    color: theme.palette.grey[500],
  },
  uploadButton: {
    height: '3em',
    fontWeight: 600,
    backgroundColor: '#4490db',
    color: 'white'
  },
});

const DialogTitle = withStyles(styles)((props) => {
  const { children, classes, onClose, ...other } = props;
  return (
    <MuiDialogTitle disableTypography className={classes.root} {...other}>
      <Typography variant="h6">{children}</Typography>
      {onClose ? (
        <IconButton aria-label="close" className={classes.closeButton} onClick={onClose}>
          <CloseIcon />
        </IconButton>
      ) : null}
    </MuiDialogTitle>
  );
});

const DialogContent = withStyles((theme) => ({
  root: {
    padding: theme.spacing(2),
    width: '40vw',
    minWidth: '32em',
  },
}))(MuiDialogContent);

export default function UploadDialog(props) {
  const classes = styles;
  const upload_mode = props.upload_mode;
  const [open, setOpen] = React.useState(false);
  const baseURL = new URL(window.location.origin);
  const [preset, setPreset] = React.useState({});

  const handleClickOpen = async () => {
    if (upload_mode == "edit") {
      let res = await axios.get(baseURL + `api/editing_init/${props.upload_id}`)
      setPreset(res.data)
    }
    setOpen(true);
  };
  const handleClose = () => {
    setOpen(false);
    if (props.upload_mode === 'upload') props.handleUploadStatus();
  };

  return (
    <React.Fragment>
      {
          upload_mode !== 'edit'
          ?
          <Button className={classes.uploadButton} variant="contained" onClick={handleClickOpen}>
            `Begin ${upload_mode}`
          </Button>
          :
          <Button onClick={handleClickOpen}>
            <EditIcon fontSize='small'/>
          </Button>
      }
      <Dialog maxWidth='md' onClose={handleClose} aria-labelledby="upload-dialog-title" open={open} disableBackdropClick={true}>
        <DialogTitle id="upload-dialog-title" onClose={handleClose}>
        </DialogTitle>
        <DialogContent>
            <UploadSteper handleClose={handleClose} upload_type={props.upload_type} preset={preset} upload_mode={upload_mode}/>
        </DialogContent>
      </Dialog>
    </React.Fragment>
  );
}
