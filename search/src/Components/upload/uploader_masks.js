import React, { useState } from "react";
import ReactImageUploadComponent from './react-images-upload/index';
import { makeStyles } from '@material-ui/core/styles';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import Button from '@material-ui/core/Button';
import axios from 'axios';
import Cookies from 'js-cookie';
import {jsonSchemaTitle} from '../error/utils';


const useStyles = makeStyles({
    submit: {
        display: 'flex',
        float: 'right',
        alignItems: 'baseline'
    },
    formControl: {
        marginRight: '1em',
        minWidth: 100,
    },
});

const UploaderMasks = props => {
  const [pictures, setPictures] = useState([]);

  const onDrop = picture => {
    setPictures(picture);
  };

  const baseURL = new URL(window.location.origin);
  const classes = useStyles();

  return (
      <React.Fragment>
          <ReactImageUploadComponent
            {...props}
            withPreview={true}
            onChange={onDrop}
            imgExtension={[".gif", ".png"]}
            maxFileSize={10485760}
            label={"Max file size: 10 MB | File types accepted: .gif, .png"}
            uploadURL={baseURL + 'api/upload_mask/'}
            removeURL={baseURL + 'api/remove_mask/'}
        />
        <div className={classes.submit}>
            <FormControl className={classes.formControl}>
                <Select
                value={props.image_ext}
                displayEmpty
                inputProps={{ 'aria-label': 'Without label' }}
                onChange={e => {props.handleImageExtension(e.target.value)}}
                >
                    <MenuItem value="">
                        <em>Image Extension</em>
                    </MenuItem>
                    <MenuItem value={"jpg"}>jpg</MenuItem>
                    <MenuItem value={"png"}>png</MenuItem>
                </Select>
            </FormControl>
            <Button variant="contained"
                    color="primary"
                    disabled={!(props.image_ext && pictures.length)}
                    onClick={() => {

                        const body = new FormData()
                        body.append('mask_id', props.upload_id)
                        body.append('image_ext', props.image_ext)
                        axios({
                            method: 'post',
                            url: baseURL + "api/submit_mask/",
                            data: body,
                            headers: {'Content-Type': 'multipart/form-data', 'X-CSRFToken': Cookies.get('csrftoken')}
                        }).then(res => {
                            res = res.data
                            props.handleUploadId(res.upload_id)
                            props.handleImages(res.images)
                            props.handleCategories(res.categories)
                            props.handleValidation(true)
                            props.handleErrorMessage("")
                        }).catch(err => {
                            const res = err.response
                            props.handleValidation(false)
                            try {
                                res = JSON.parse(res.data)
                                props.handleErrorMessage(jsonSchemaTitle(res), res)
                            } catch (e) {
                                props.handleErrorMessage(res.data)
                            }
                        })
                    }}>Submit
            </Button>
        </div>
      </React.Fragment>
        
  );
};

export default UploaderMasks;
