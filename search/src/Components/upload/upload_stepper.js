// import React from 'react';
// import { withStyles } from '@material-ui/core/styles';
// import Stepper from '@material-ui/core/Stepper';
// import Step from '@material-ui/core/Step';
// import StepLabel from '@material-ui/core/StepLabel';
// import Button from '@material-ui/core/Button';
// import Typography from '@material-ui/core/Typography';
// import UploaderSingle from './uploader_single';
// import UploaderMultiple from './uploader_multiple';


// const useStyles = (theme) => ({
//   root: {
//     width: '100%',
//   },
//   button: {
//     marginRight: theme.spacing(1),
//   },
//   instructions: {
//     marginTop: theme.spacing(1),
//     marginBottom: theme.spacing(1),
//   },
// });

// function getSteps() {
//   return ['Upload Weedcoco', 'Add Agcontext', 'Upload Images'];
// }

// function getStepContent(step, upload_id, images, handleUploadId, handleImages) {
//   switch (step) {
//     case 0:
//       return <UploaderSingle upload_id={upload_id} images={images} handleUploadId={handleUploadId} handleImages={handleImages}/>;
//     case 1:
//       return 'Placeholder for a Agcontext form';
//     case 2:
//       return <UploaderMultiple upload_id={upload_id} images={images}/>;
//     default:
//       return 'Unknown step';
//   }
// }

// class UploadStepper extends React.Component {

//     constructor() {
//         super();
//         this.state = {
//             activeStep: 0,
//             skipped: new Set(),
//             steps: getSteps(),
//             upload_id: 0,
//             images: [],
//         }
//         this.isStepOptional = this.isStepOptional.bind(this);
//         this.isStepSkipped = this.isStepSkipped.bind(this);
//         this.handleUploadId = this.handleUploadId.bind(this);
//         this.handleImages = this.handleImages.bind(this);
//         this.handleNext = this.handleNext.bind(this);
//         this.handleBack = this.handleBack.bind(this);
//         this.handleSkip = this.handleSkip.bind(this);
//         this.handleReset = this.handleReset.bind(this);
//     }

//     isStepOptional(step) {
//         return step === 1;
//     };

//     isStepSkipped(step) {
//         return this.state.skipped.has(step);
//     };

//     handleUploadId(upload_id) {
//         this.setState({upload_id: upload_id});
//     }

//     handleImages(images) {
//         this.setState({images: images});
//     }

//     handleNext() {
//         let newSkipped = this.state.skipped;
//         let activeStep = this.state.activeStep;
//         if (this.isStepSkipped(activeStep)) {
//             newSkipped = new Set(newSkipped.values());
//             newSkipped.delete(activeStep);
//         }
//         this.setState(prevState => {return {activeStep: prevState.activeStep + 1}});
//         this.setState({skipped: newSkipped});
//     };

//     handleBack(){
//         this.setState(prevState => {return {activeStep: prevState.activeStep - 1}});
//     };

//     handleSkip(){
//         if (!this.isStepOptional(this.state.activeStep)) {
//             // You probably want to guard against something like this,
//             // it should never occur unless someone's actively trying to break something.
//             throw new Error("You can't skip a step that isn't optional.");
//         }
//         this.setState(prevState => {return {activeStep: prevState.activeStep + 1}});
//         this.setState(prevState => {
//             const newSkipped = new Set(prevState.skipped.values());
//             newSkipped.add(this.state.activeStep);
//             return {skipped: newSkipped};
//         })
//     };

//     handleReset(){
//         this.setState({activeStep: 0})
//     };

//     render(){
//         const { classes } = this.props;
//         return (
//             <div className={classes.root}>
//             <Stepper activeStep={this.state.activeStep}>
//                 {this.state.steps.map((label, index) => {
//                 const stepProps = {};
//                 const labelProps = {};
//                 if (this.isStepOptional(index)) {
//                     labelProps.optional = <Typography variant="caption">Optional</Typography>;
//                 }
//                 if (this.isStepSkipped(index)) {
//                     stepProps.completed = false;
//                 }
//                 return (
//                     <Step key={label} {...stepProps}>
//                     <StepLabel {...labelProps}>{label}</StepLabel>
//                     </Step>
//                 );
//                 })}
//             </Stepper>
//             <div>
//                 {this.state.activeStep === this.state.steps.length ? (
//                 <div>
//                     <Typography className={classes.instructions}>
//                     All steps completed - you&apos;re finished
//                     </Typography>
//                     <Button onClick={this.handleReset} className={classes.button}>
//                     Reset
//                     </Button>
//                 </div>
//                 ) : (
//                 <div>
//                     <Typography className={classes.instructions}>{getStepContent(this.state.activeStep, this.state.upload_id, this.state.images, this.handleUploadId, this.handleImages)}</Typography>
//                     <div>
//                     <Button disabled={this.state.activeStep === 0} onClick={this.handleBack} className={classes.button}>
//                         Back
//                     </Button>
//                     {this.isStepOptional(this.state.activeStep) && (
//                         <Button
//                         variant="contained"
//                         color="primary"
//                         onClick={this.handleSkip}
//                         className={classes.button}
//                         >
//                         Skip
//                         </Button>
//                     )}
        
//                     <Button
//                         variant="contained"
//                         color="primary"
//                         onClick={this.handleNext}
//                         className={classes.button}
//                     >
//                         {this.state.activeStep === this.state.steps.length - 1 ? 'Finish' : 'Next'}
//                     </Button>
//                     </div>
//                 </div>
//                 )}
//             </div>
//             </div>
//         );
//     }
// };

// export default withStyles(useStyles)(UploadStepper);


import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import Stepper from '@material-ui/core/Stepper';
import Step from '@material-ui/core/Step';
import StepLabel from '@material-ui/core/StepLabel';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import UploaderSingle from './uploader_single';
import UploaderImages from './uploader_images';
import axios from 'axios'


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

function getSteps() {
  return ['Upload Weedcoco', 'Add Agcontext', 'Upload Images'];
}

function getStepContent(step, upload_id, images, handleUploadId, handleImages) {
  switch (step) {
    case 0:
      return <UploaderSingle upload_id={upload_id} images={images} handleUploadId={handleUploadId} handleImages={handleImages}/>;
    case 1:
      return 'Placeholder for a Agcontext form';
    case 2:
      return <UploaderImages upload_id={upload_id} images={images}/>;
    default:
      return 'Unknown step';
  }
}

class UploadStepper extends React.Component {

    constructor() {
        super();
        this.state = {
            activeStep: 0,
            skipped: new Set(),
            steps: getSteps(),
            upload_id: 0,
            images: [],
        }
        this.isStepOptional = this.isStepOptional.bind(this);
        this.isStepSkipped = this.isStepSkipped.bind(this);
        this.handleUploadId = this.handleUploadId.bind(this);
        this.handleImages = this.handleImages.bind(this);
        this.handleNext = this.handleNext.bind(this);
        this.handleBack = this.handleBack.bind(this);
        this.handleSkip = this.handleSkip.bind(this);
        this.handleReset = this.handleReset.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    isStepOptional(step) {
        return step === 1;
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
        }
    };

    handleBack(){
        this.setState(prevState => {return {activeStep: prevState.activeStep - 1}});
    };

    handleSkip(){
        if (!this.isStepOptional(this.state.activeStep)) {
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

    handleSubmit(){
        const baseURL = new URL(window.location.origin);
        const body = new FormData()
        body.append('upload_id', this.state.upload_id)
        axios({
            method: 'post',
            url: baseURL + "api/submit_deposit/",
            data: body,
            headers: {'Content-Type': 'multipart/form-data' }
        })
    }

    render(){
        const { classes } = this.props;
        return (
            <div className={classes.root}>
            <Stepper activeStep={this.state.activeStep}>
                {this.state.steps.map((label, index) => {
                const stepProps = {};
                const labelProps = {};
                if (this.isStepOptional(index)) {
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
                <Typography className={classes.instructions}>{getStepContent(this.state.activeStep, this.state.upload_id, this.state.images, this.handleUploadId, this.handleImages)}</Typography>
                <div>
                <Button disabled={this.state.activeStep === 0} onClick={this.handleBack} className={classes.button}>
                    Back
                </Button>
                {this.isStepOptional(this.state.activeStep) && (
                    <Button
                    variant="contained"
                    color="primary"
                    onClick={this.handleSkip}
                    className={classes.button}
                    >
                    Skip
                    </Button>
                )}
    
                <Button
                    variant="contained"
                    color="primary"
                    onClick={this.handleNext}
                    className={classes.button}
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

