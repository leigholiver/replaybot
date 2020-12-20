import React from 'react';

import Input from '@material-ui/core/Input';
import ListItemText from '@material-ui/core/ListItemText';
import Select from '@material-ui/core/Select';
import Checkbox from '@material-ui/core/Checkbox';
import MenuItem from '@material-ui/core/MenuItem';

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
    PaperProps: {
        style: {
            maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
            width: 250,
        },
    },
};

export function select(labelId, value, setValue, options = [], multiple = true, emptyOption = null) {
    return (
        <Select labelId={labelId} input={<Input />} multiple={multiple} value={value} MenuProps={MenuProps}
            onChange={(e) => {
                e.preventDefault();
                if(multiple) setValue(e.target.value)
                else
                    setValue(e.target.value)
            }}
            renderValue={selected => {
                const fullOpts = [emptyOption].concat(options);
                return fullOpts.filter((opt) => opt && selected.includes(opt.id)).map(option => option.name).join(", ");
            }}
        >
            {emptyOption && listItem(emptyOption.id, emptyOption.name, value)}
            {options.map(option => option !== null? listItem(option.id, option.name, value) : "?")}
        </Select>
    );
}

function listItem(id, name, value) {
    return (<MenuItem key={id} value={id}>
        <Checkbox color="primary" checked={value === id || (Array.isArray(value) && value.includes(id))} /> <ListItemText primary={name} />
    </MenuItem>);
}