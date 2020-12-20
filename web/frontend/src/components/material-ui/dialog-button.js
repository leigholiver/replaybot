import React from 'react';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';

export default function DialogButton({children, submitButton, buttonText, title=null, buttonIcon=null, size=null}) {
  const [open, setOpen] = React.useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <div style={{display: "inline"}}>
      <Button variant="outlined" color="primary" onClick={handleClickOpen} startIcon={buttonIcon} size={size}>
        {buttonText}
      </Button>
      <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
        { title && <DialogTitle id="form-dialog-title">{title}</DialogTitle>}
        <DialogContent>
            {children}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary">
            Cancel
          </Button>
          {submitButton}
        </DialogActions>
      </Dialog>
    </div>
  );
}