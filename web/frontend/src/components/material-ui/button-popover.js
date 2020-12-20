import React from 'react';
import Popover from '@material-ui/core/Popover';
import Button from '@material-ui/core/Button';

export default function ButtonPopover({text, children}) {
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const open = Boolean(anchorEl);
  const id = open ? 'simple-popover' : undefined;

  return (
    <div style={{padding: "0.1rem"}}>
        <Button aria-describedby={id} 
            variant="outlined"
            color="primary" 
            size="small"
            onClick={handleClick}
        >
            { text }
        </Button>
        <Popover
            id={id}
            open={open}
            anchorEl={anchorEl}
            onClose={handleClose}
            anchorOrigin={{
            vertical: 'bottom',
            horizontal: 'center',
            }}
            transformOrigin={{
            vertical: 'top',
            horizontal: 'center',
            }}
        >
            {children}
        </Popover>
    </div>
  );
}