import React from "react";
import Icon from "@material-ui/core/Icon";
import { makeStyles } from "@material-ui/styles";

const useStyles = makeStyles({
    imageIcon: {
      height: "100%",
      width: "100%"
    },
    iconRoot: {
      textAlign: "center",
      width: "2rem",
      height: "2rem"
    }
  });

export function SvgIcon({path, alt="Icon"}) {
    const classes = useStyles();
    return (
        <Icon classes={{root: classes.iconRoot}}>
            <img className={classes.imageIcon} src={path} alt={alt} />
        </Icon>
    );
}
