import React from 'react';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogContent from '@material-ui/core/DialogContent';
import LoginComponent from '../auth/login';
import RegisterComponent from '../auth/register';

export default function AuthPrompt(props) {
  const [open, setOpen] = React.useState(false);
  const [prompt, setPrompt] = React.useState('login');

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleLogin = () => {
    setPrompt('login');
    handleClickOpen();
  };

  const handleRegister = () => {
    setPrompt('register');
    handleClickOpen();
  };

  return (
    <div>
      <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}>
        Please&nbsp;
        <Button variant="outlined" color="primary" onClick={handleLogin}>
            Sign In
        </Button>
        &nbsp;or&nbsp;
        <Button variant="outlined" color="primary" onClick={handleRegister}>
            Sign up
        </Button>
      </div>
      <Dialog open={open} onClose={handleClose}>
        <DialogContent>
          {prompt === 'register' ? <RegisterComponent handleClose={handleClose}/> : <LoginComponent handleLogin={props.handleLogin} handleClose={handleClose}/>}
        </DialogContent>
      </Dialog>
    </div>
  );
}