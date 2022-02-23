import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import Stepper from '@material-ui/core/Stepper';
import Step from '@material-ui/core/Step';
import StepLabel from '@material-ui/core/StepLabel';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import UploaderSingle from './uploader_single';
import UploaderVoc from './uploader_voc';
import UploaderMasks from './uploader_masks';
import CategoryMapper from './uploader_category_mapper';
import CvatRetriever from './uploader_cvat';
import CopyCvatUploader from './uploader_copy_cvat';
import ErrorMessage from '../error/display';
import AgContextForm from '../forms/AgContextForm';
import UploadJsonButton from '../forms/UploadJsonButton';
import MetadataForm from '../forms/MetadataForm';
import axios from 'axios';
import Cookies from 'js-cookie';
import cloneDeep from 'lodash/cloneDeep';
import {jsonSchemaTitle} from '../error/utils';
import ImageOrZipUploader from './uploader_zip_images';
import CardSelector from '../generic/card_selector';


const baseURL = new URL(window.location.origin);

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
  imageFormatSelection: {
    margin: theme.spacing(1),
  },
});

const typeData = [
  {
    "id": "weedcoco",
    "name": "WeedCOCO",
    "description": <Typography>Weed-AI's custom extension of MS COCO with everything included.</Typography>
  },
  {
    "id": "coco",
    "name": "MS COCO",
    "description": <Typography>MS COCO format for classification, bounding boxes or segmentation.</Typography>
  },
  {
    "id": "voc",
    "name": "Pascal VOC",
    "description": <Typography>Pascal VOC's XML annotation format for bounding boxes.</Typography>
  },
  {
    "id": "masks",
    "name": "Mask PNGs",
    "description": <Typography>Colour coded mask images for segmentation.</Typography>
  },
]
const stepsByType = {
    "coco": [
        {title: "Select Format", type: "select-type"},
        {title: "Upload Coco", type: "coco-upload"},
        {title: "Categories", type: "categories"},
        {title: "Add Agcontext", type: "agcontext"},
        {title: "Add Metadata", type: "metadata"},
        {title: "Upload Images", type: "images"}
    ],
    "weedcoco": [
        {title: "Select Format", type: "select-type"},
        {title: "Upload Weedcoco", type: "weedcoco-upload"},
        {title: "Upload Images", type: "images"}
    ],
    "voc": [
        {title: "Select Format", type: "select-type"},
        {title: "Upload VOC", type: "voc-upload"},
        {title: "Categories", type: "categories"},
        {title: "Add Agcontext", type: "agcontext"},
        {title: "Add Metadata", type: "metadata"},
        {title: "Upload Images", type: "images"}
    ],
    "masks": [
        {title: "Select Format", type: "select-type"},
        {title: "Upload Masks", type: "masks-upload"},
        {title: "Categories", type: "categories"},
        {title: "Add Agcontext", type: "agcontext"},
        {title: "Add Metadata", type: "metadata"},
        {title: "Upload Images", type: "images"}
    ],
    "cvat": [
        {title: "Select CVAT Task", type: "cvat"},
        {title: "Categories", type: "categories"},
        {title: "Add Agcontext", type: "agcontext"},
        {title: "Add Metadata", type: "metadata"},
        {title: "Copy CVAT Images", type: "copy_cvat"}
    ]
}

class UploadStepper extends React.Component {

    constructor(props) {
        super(props);
        const upload_type = props.upload_type || "weedcoco";
        this.state = {
            activeStep: 0,
            skip_mapping: {'weedcoco': -1, 'coco': -1},
            skipped: new Set(),
            upload_id: 0,
            cvat_task_id: 0,
            voc_id: Math.random().toString(36).slice(-8),
            mask_id: Math.random().toString(36).slice(-8),
            image_ext: '',
            images: [],
            categories: [],
            ag_context: {},
            metadata: {},
            error_message: "",
            error_message_details: "",
            ... this.getUploadTypeState(upload_type),
        }
        this.isStepOptional = this.isStepOptional.bind(this);
        this.isStepSkipped = this.isStepSkipped.bind(this);
        this.handleUploadId = this.handleUploadId.bind(this);
        this.handleCvatTaskId = this.handleCvatTaskId.bind(this);
        this.handleImageExtension = this.handleImageExtension.bind(this);
        this.handleImages = this.handleImages.bind(this);
        this.handleCategories = this.handleCategories.bind(this);
        this.handleUpdateCategories = this.handleUpdateCategories.bind(this);
        this.handleAgContextsFormData = this.handleAgContextsFormData.bind(this);
        this.handleMetadataFormData = this.handleMetadataFormData.bind(this);
        this.handleErrorMessage = this.handleErrorMessage.bind(this);
        this.handleNext = this.handleNext.bind(this);
        this.handleBack = this.handleBack.bind(this);
        this.handleSkip = this.handleSkip.bind(this);
        this.handleReset = this.handleReset.bind(this);
        this.handleUploadAgcontexts = this.handleUploadAgcontexts.bind(this);
        this.handleUploadMetadata = this.handleUploadMetadata.bind(this);
        this.handleMoveVoc = this.handleMoveVoc.bind(this);
        this.handleMoveMask = this.handleMoveMask.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleTusUpload = this.handleTusUpload.bind(this);
        this.nextHandler = this.nextHandler.bind(this);
        this.handleValidation = this.handleValidation.bind(this);
        this.getStepContent = this.getStepContent.bind(this);
    }

    setUploadType(upload_type) {
        this.setState(this.getUploadTypeState(upload_type));
    }

    getUploadTypeState(upload_type) {
        return {
            upload_type: upload_type,
            steps: stepsByType[upload_type].map(step => step.title),
            stepValid: stepsByType[upload_type].reduce(
                (steps, step) => {
                    return {...steps, [step.type]: step.type == "select-type"}
                }, {}
            ),
        }
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

    handleCvatTaskId(cvat_task_id) {
        this.setState({cvat_task_id: cvat_task_id});
    }

    handleImageExtension(image_ext) {
        this.setState({image_ext: image_ext})
    }

    handleImages(images) {
        this.setState({images: images});
    }

    handleCategories(categories) {
        this.setState({categories: cloneDeep(categories)});
    }

    handleAgContextsFormData(formData) {
        this.setState({ag_context: formData});
    }

    handleMetadataFormData(formData) {
        this.setState({metadata: formData});
    }

    handleErrorMessage(message, details="") {
        this.setState({error_message: message, error_message_details: details});
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
            this.handleErrorMessage("")
        }
    };

    handleBack(){
        this.setState(prevState => {return {activeStep: prevState.activeStep - 1}});
        this.handleErrorMessage("")
    };

    handleSkip(){
        if (!this.isStepOptional(this.state.activeStep, this.state.upload_type)) {
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

    handleUpdateCategories(){
        axios({
            method: 'post',
            url: baseURL + "api/update_categories/",
            data: {
                "upload_id": this.state.upload_id,
                "categories": this.state.categories
            },
            headers: {'X-CSRFToken': Cookies.get('csrftoken') }
        }).then(res => {
            console.log(res)
            this.handleErrorMessage("")
            this.handleNext()
        })
        .catch(err => {
            this.handleValidation(false)
            const data = err.response.data
            if (typeof data === "object") this.handleErrorMessage(jsonSchemaTitle(data), data);
            else this.handleErrorMessage(data || "Server error saving categories")
        })
    }

    handleUploadAgcontexts(){
        axios({
            method: 'post',
            url: baseURL + "api/upload_agcontexts/",
            data: {
                "upload_id": this.state.upload_id,
                "ag_contexts": this.state.ag_context
            },
            headers: {'X-CSRFToken': Cookies.get('csrftoken') }
        }).then(res => {
            console.log(res)
            this.handleErrorMessage("")
            this.handleNext()
        })
        .catch(err => {
            console.log(err)
            const data = err.response.data
            if (typeof data === "object") this.handleErrorMessage(jsonSchemaTitle(data), data);
            else this.handleErrorMessage(data || "Server error saving AgContext")
        })
    }

    handleUploadMetadata(){
        axios({
            method: 'post',
            url: baseURL + "api/upload_metadata/",
            data: {
                "upload_id": this.state.upload_id,
                "metadata": this.state.metadata
            },
            headers: {'X-CSRFToken': Cookies.get('csrftoken') }
        }).then(res => {
            console.log(res)
            this.handleErrorMessage("")
            this.handleNext()
        })
        .catch(err => {
            console.log(err)
            this.handleValidation(false)
            this.handleErrorMessage("Failed to submit metadata")
        })
    }

    handleMoveMask(){
        const body = new FormData()
        body.append('upload_id', this.state.upload_id)
        body.append('mask_id', this.state.mask_id)
        axios({
            method: 'post',
            url: baseURL + "api/move_mask/",
            data: body,
            headers: {'X-CSRFToken': Cookies.get('csrftoken') }
        }).then(res => {
            console.log(res)
            this.handleErrorMessage("")
            this.handleNext()
        })
        .catch(err => {
            console.log(err)
            this.handleValidation(false)
            this.handleErrorMessage("Failed to move mask")
        })
    }

    handleMoveVoc(){
        const body = new FormData()
        body.append('upload_id', this.state.upload_id)
        body.append('voc_id', this.state.voc_id)
        axios({
            method: 'post',
            url: baseURL + "api/move_voc/",
            data: body,
            headers: {'X-CSRFToken': Cookies.get('csrftoken') }
        }).then(res => {
            console.log(res)
            this.handleErrorMessage("")
            this.handleNext()
        })
        .catch(err => {
            console.log(err)
            this.handleValidation(false)
            this.handleErrorMessage("Failed to move voc")
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
            headers: {'Content-Type': 'multipart/form-data', 'X-CSRFToken': Cookies.get('csrftoken') }
        })
    }

    handleValidation(status){
        const currentStep = stepsByType[this.state.upload_type][this.state.activeStep].type
        this.setState(prevState => {
            const newState = {stepValid: {...prevState.stepValid}}
            newState.stepValid[currentStep] = status
            return newState
        })
    }

    handleTusUpload(files){
        console.log(`handleTusUpload ${files}`);

    }

    getStepContent() {
        const step = stepsByType[this.state.upload_type][this.state.activeStep].type
        switch (step) {
            case "select-type":
                return <div>
                    <Typography gutterBottom variant="subtitle1" component="div">
                      Select an input annotation format:
                    </Typography>
                    <CardSelector cardData={typeData} selected={this.state.upload_type} handleSelect={(upload_type) => this.setUploadType(upload_type)} />
                  </div>
            case "coco-upload":
            case "weedcoco-upload":
                const schema = step == "coco-upload" ? "coco" : "weedcoco"
                return <UploaderSingle upload_id={this.state.upload_id} images={this.state.images} handleUploadId={this.handleUploadId} handleImages={this.handleImages} handleCategories={this.handleCategories} handleValidation={this.handleValidation} handleErrorMessage={this.handleErrorMessage} schema={schema}/>
            case "voc-upload":
                return <UploaderVoc handleUploadId={this.handleUploadId} handleImages={this.handleImages} handleCategories={this.handleCategories} handleValidation={this.handleValidation} handleErrorMessage={this.handleErrorMessage} voc_id={this.state.voc_id}/>
            case "masks-upload":
                return <UploaderMasks upload_id={this.state.mask_id} handleUploadId={this.handleUploadId} image_ext={this.state.image_ext} handleImageExtension={this.handleImageExtension} handleImages={this.handleImages} handleCategories={this.handleCategories} handleValidation={this.handleValidation} handleErrorMessage={this.handleErrorMessage}/>
            case "categories":
                return <CategoryMapper categories={cloneDeep(this.state.categories)} handleCategories={this.handleCategories} handleValidation={this.handleValidation} handleErrorMessage={this.handleErrorMessage}/>
            case "agcontext":
                return (
                    <React.Fragment>
                        <AgContextForm formData={this.state.ag_context} handleValidation={this.handleValidation} onChange={e => {
                            this.handleAgContextsFormData(e.formData)
                            this.handleErrorMessage("")
                        }} />
                        <UploadJsonButton initialValue={this.state.ag_context} downloadName="agcontext" onClose={(value) => {this.handleAgContextsFormData(value)}} />
                    </React.Fragment>
                )
            case "metadata":
                return (
                    <React.Fragment>
                        <MetadataForm formData={this.state.metadata} handleValidation={this.handleValidation} onChange={e => {
                            this.handleMetadataFormData(e.formData)
                            this.handleErrorMessage("")
                        }} />
                        <UploadJsonButton initialValue={this.state.metadata} downloadName="dataset-meta" onClose={(value) => {this.handleMetadataFormData(value)}} />
                    </React.Fragment>
                )
            case "images":
                return <ImageOrZipUploader stepName={step} upload_id={this.state.upload_id} cvat_task_id={this.state.cvat_task_id} images={this.state.images} handleValidation={this.handleValidation} handleErrorMessage={this.handleErrorMessage} />
            case "cvat":
                return <CvatRetriever handleUploadId={this.handleUploadId} handleCvatTaskId={this.handleCvatTaskId} handleImages={this.handleImages} handleCategories={this.handleCategories} handleValidation={this.handleValidation} handleErrorMessage={this.handleErrorMessage} />
            case "copy_cvat":
                return <CopyCvatUploader upload_id={this.state.upload_id} cvat_task_id={this.state.cvat_task_id} images={this.state.images} handleValidation={this.handleValidation} handleErrorMessage={this.handleErrorMessage} />
            default:
                return ''
        }
    }

    nextHandler(step) {
        switch (step) {
            case "voc-upload":
                return this.handleMoveVoc
            case "masks-upload":
                return this.handleMoveMask
            case "categories":
                return this.handleUpdateCategories
            case "agcontext":
                return this.handleUploadAgcontexts
            case "metadata":
                return this.handleUploadMetadata
            default:
                return this.handleNext
        }
    }

    render(){
        const { classes } = this.props;
        const stepName = stepsByType[this.state.upload_type][this.state.activeStep].type;
        return (
            <div className={classes.root}>
            <Stepper activeStep={this.state.activeStep}>
                {this.state.steps.map((label, index) => {
                const stepProps = {};
                const labelProps = {};
                if (this.isStepOptional(index, this.state.upload_type)) {
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
                <div className={classes.instructions}>
                    {this.getStepContent()}
                </div>
                <ErrorMessage error={this.state.error_message} details={this.state.error_message_details}/>
                <div>
                    <Button disabled={this.state.activeStep === 0} onClick={this.handleBack} className={classes.button}>
                        Back
                    </Button>
                    {this.isStepOptional(this.state.activeStep, this.state.upload_type)
                    && (
                        <Button
                        variant="contained"
                        color="primary"
                        onClick={this.handleSkip}
                        className={classes.button}
                        disabled={this.state.error_message.length > 0}
                        >
                        Skip
                        </Button>
                    )}

                    <Button
                        variant="contained"
                        color="primary"
                        onClick={this.nextHandler(stepName)}
                        className={classes.button}
                        disabled={!this.state.stepValid[stepName]}
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

