import UploadDialog from '../upload/upload_dialog';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import React, { useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';


const useStyles = makeStyles((theme) => ({
    uploadSelect: {
        display: 'flex',
        alignItems: 'center',
    },
    formControl: {
        marginRight: theme.spacing(2),
        minWidth: 200,
    }
}))

export default function DatasetList(props) {
  const classes = useStyles();
  const [upload_type, setUploadType] = useState("");

  function handleChange(event){
    setUploadType(event.target.value)
  };

  return (
    <div className={classes.uploadSelect}>
        <FormControl className={classes.formControl}>
            <Select
            value={upload_type}
            displayEmpty
            onChange={handleChange}
            >
                <MenuItem value="" disabled>
                    Select annotation format
                </MenuItem>
                <MenuItem value="weedcoco">WeedCOCO</MenuItem>
                <MenuItem value="coco">COCO</MenuItem>
                <MenuItem value="voc">VOC</MenuItem>
                <MenuItem value="masks">Segmentation masks</MenuItem>
                <MenuItem value="cvat">Annotation</MenuItem>
            </Select>
        </FormControl>
        <UploadDialog handleUploadStatus={props.retrieveUploadStatus} upload_type={upload_type} upload_mode={props.upload_mode}/>
    </div>
  )
}