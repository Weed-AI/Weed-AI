import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import Stepper from '@material-ui/core/Stepper';
import Step from '@material-ui/core/Step';
import StepLabel from '@material-ui/core/StepLabel';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import UploaderSingle from './uploader_single';
import UploaderImages from './uploader_images';
import AgContextForm from '../../AgContextForm';
import {toJSON} from '../ui/UploadJsonButton';
import axios from 'axios';
import Cookies from 'js-cookie';

const csrftoken = Cookies.get('csrftoken');

const useStyles = (theme) => ({
  root: {
    width: '100%',
  },
  button: {
    marginRight: theme.spacing(1),
  },
  instructions: {
    marginTop: theme.spacing(1),
    marginBottom: theme.spacing(1),
  },
});

function getSteps(upload_type) {
  return upload_type === 'coco'?
         ['Upload Coco', 'Add Agcontext', 'Upload Images']:
         upload_type === 'weedcoco'?
         ['Upload Weedcoco', 'Upload Images']:
         ['Upload Coco', 'Add Agcontext', 'Upload Images']
}

function getStepContent(step, upload_type, upload_id, images, formData, handleUploadId, handleImages, handleFormData, handleErrorMessage) {
    if (upload_type === 'coco') {
        switch (step) {
            case 0:
              return <UploaderSingle upload_id={upload_id} images={images} handleUploadId={handleUploadId} handleImages={handleImages} handleErrorMessage={handleErrorMessage}/>;
            case 1:
              return (
                <React.Fragment>
                    <AgContextForm formData={formData} onChange={e => {
                        handleFormData(e.formData)
                        handleErrorMessage("init")
                    }} />
                    <textarea style={{width: "100%", height: "5em"}} value={toJSON(formData)} ></textarea>
                    <React.Fragment>
                        <button onClick={e => handleSaveToPC(formData)}>Download</button>
                    </React.Fragment>
                </React.Fragment>
              );
            case 2:
              return <UploaderImages upload_id={upload_id} images={images}/>;
            default:
              return 'Unknown step';
        }
    } else if (upload_type === 'weedcoco') {
        switch (step) {
            case 0:
              return <UploaderSingle upload_id={upload_id} images={images} handleUploadId={handleUploadId} handleImages={handleImages} handleErrorMessage={handleErrorMessage}/>;
            case 1:
              return <UploaderImages upload_id={upload_id} images={images}/>;
            default:
              return 'Unknown step';
        }
    } else {
        switch (step) {
            case 0:
              return <UploaderSingle upload_id={upload_id} images={images} handleUploadId={handleUploadId} handleImages={handleImages} handleErrorMessage={handleErrorMessage}/>;
            case 1:
              return <AgContextForm formData={formData} onChange={e => handleFormData(e.formData)} />;
            case 2:
              return <UploaderImages upload_id={upload_id} images={images}/>;
            default:
              return 'Unknown step';
        }
    }
}

const handleSaveToPC = (payload) => {
    const fileData = toJSON(payload);
    const blob = new Blob([fileData], {type: "application/json"});
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.download = `AgContext.json`;
    link.href = url;
    link.click();
}

class UploadStepper extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            activeStep: 0,
            skip_mapping: {'weedcoco': -1, 'coco': -1},
            skipped: new Set(),
            steps: getSteps(this.props.upload_type),
            upload_id: 0,
            images: [],
            ag_context: {},
            error_message: "init"
        }
        this.isStepOptional = this.isStepOptional.bind(this);
        this.isStepSkipped = this.isStepSkipped.bind(this);
        this.handleUploadId = this.handleUploadId.bind(this);
        this.handleImages = this.handleImages.bind(this);
        this.handleFormData = this.handleFormData.bind(this);
        this.handleErrorMessage = this.handleErrorMessage.bind(this);
        this.handleNext = this.handleNext.bind(this);
        this.handleBack = this.handleBack.bind(this);
        this.handleSkip = this.handleSkip.bind(this);
        this.handleReset = this.handleReset.bind(this);
        this.handleUploadAgcontexts = this.handleUploadAgcontexts.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAgContextExempt = this.handleAgContextExempt.bind(this);
    }

    isStepOptional(step, upload_type) {
        return this.state.skip_mapping[upload_type] === step;
    };

    isStepSkipped(step) {
        return this.state.skipped.has(step);
    };

    handleUploadId(upload_id) {
        this.setState({upload_id: upload_id});
    }

    handleImages(images) {
        this.setState({images: images});
    }

    handleFormData(formData) {
        this.setState({ag_context: formData});
    }

    handleErrorMessage(message) {
        this.setState({error_message: message});
    }

    handleNext() {
        if (this.state.activeStep === this.state.steps.length - 1){
            this.handleSubmit();
            this.props.handleClose();
            this.handleReset();
        }
        else {
            let newSkipped = this.state.skipped;
            let activeStep = this.state.activeStep;
            if (this.isStepSkipped(activeStep)) {
                newSkipped = new Set(newSkipped.values());
                newSkipped.delete(activeStep);
            }
            this.setState(prevState => {return {activeStep: prevState.activeStep + 1}});
            this.setState({skipped: newSkipped});
            this.handleErrorMessage("init")
        }
    };

    handleBack(){
        this.setState(prevState => {return {activeStep: prevState.activeStep - 1}});
        this.handleErrorMessage("init")
    };

    handleSkip(){
        if (!this.isStepOptional(this.state.activeStep, this.props.upload_type)) {
            // You probably want to guard against something like this,
            // it should never occur unless someone's actively trying to break something.
            throw new Error("You can't skip a step that isn't optional.");
        }
        this.setState(prevState => {return {activeStep: prevState.activeStep + 1}});
        this.setState(prevState => {
            const newSkipped = new Set(prevState.skipped.values());
            newSkipped.add(this.state.activeStep);
            return {skipped: newSkipped};
        })
    };

    handleReset(){
        this.setState({activeStep: 0})
    };

    handleUploadAgcontexts(){
        const baseURL = new URL(window.location.origin);
        axios({
            method: 'post',
            url: baseURL + "api/upload_agcontexts/",
            data: {
                "upload_id": this.state.upload_id,
                "ag_contexts": this.state.ag_context
            },
            headers: {'X-CSRFToken': csrftoken }
        }).then(res => {
            console.log(res)
            this.handleErrorMessage("")
            this.handleNext()
        })
        .catch(err => {
            console.log(err)
            this.handleErrorMessage("Invalid input for AgContext")
        })
    }

    handleSubmit(){
        const baseURL = new URL(window.location.origin);
        const body = new FormData()
        body.append('upload_id', this.state.upload_id)
        axios({
            method: 'post',
            url: baseURL + "api/submit_deposit/",
            data: body,
            headers: {'Content-Type': 'multipart/form-data', 'X-CSRFToken': csrftoken }
        })
    }

    handleAgContextExempt(){
        return this.state.activeStep === 1 && this.props.upload_type === 'coco'
    }

    render(){
        const { classes } = this.props;
        return (
            <div className={classes.root}>
            <Stepper activeStep={this.state.activeStep}>
                {this.state.steps.map((label, index) => {
                const stepProps = {};
                const labelProps = {};
                if (this.isStepOptional(index, this.props.upload_type)) {
                    labelProps.optional = <Typography variant="caption">Optional</Typography>;
                }
                if (this.isStepSkipped(index)) {
                    stepProps.completed = false;
                }
                return (
                    <Step key={label} {...stepProps}>
                    <StepLabel {...labelProps}>{label}</StepLabel>
                    </Step>
                );
                })}
            </Stepper>
            <div>
                <Typography className={classes.instructions}>
                    {getStepContent(this.state.activeStep, this.props.upload_type, this.state.upload_id, this.state.images, this.state.ag_context, this.handleUploadId, this.handleImages, this.handleFormData, this.handleErrorMessage)}
                </Typography>
                {this.state.error_message.length > 0 && this.state.error_message !== 'init' ? <p style={{color: 'red', float: 'right', marginTop: '0.5em'}}>{this.state.error_message}</p> : ""}
                <div>
                    <Button disabled={this.state.activeStep === 0} onClick={this.handleBack} className={classes.button}>
                        Back
                    </Button>
                    {this.isStepOptional(this.state.activeStep, this.props.upload_type)
                    && (
                        <Button
                        variant="contained"
                        color="primary"
                        onClick={this.handleSkip}
                        className={classes.button}
                        disabled={this.state.error_message.length > 0 && this.state.error_message !== "init"}
                        >
                        Skip
                        </Button>
                    )}
        
                    <Button
                        variant="contained"
                        color="primary"
                        onClick={this.handleAgContextExempt() ? this.handleUploadAgcontexts : this.handleNext}
                        className={classes.button}
                        disabled={this.state.error_message.length > 0 && this.state.activeStep !== this.state.steps.length - 1 && !this.handleAgContextExempt()}
                    >
                        {this.state.activeStep === this.state.steps.length - 1 ? 'Submit' : 'Next'}
                    </Button>
                </div>
            </div>
            </div>
        );
    }
};

export default withStyles(useStyles)(UploadStepper);

