import React from 'react';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';

export default function Hover({ onHover, children, right=false }) {
    let cn = "__hover_hover";
    if(right) cn += " __hover_right"
    return (
        <div className="__hover">
            <div>{children}</div>
            <div className={cn}>
                <Card>
                    <CardContent>
                        {onHover}
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}