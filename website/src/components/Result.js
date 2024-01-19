import * as React from 'react';
import PropTypes from 'prop-types';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

var colorsJson = require('../styling/colors.json');

function CustomTabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

CustomTabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.number.isRequired,
  value: PropTypes.number.isRequired,
};

function a11yProps(index) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}

function Result({aitext, aients, aitokens, model}) {
  const [value, setValue] = React.useState(0);
  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

function getTokens() {
  console.log(aients);
};

function returnColor(clName) {
  return colorsJson[model][clName]
}

  return (
    <Box sx={{ width: '100%' }}>
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={value} onChange={handleChange} aria-label="basic tabs example">
          <Tab label="Text" {...a11yProps(0)} />
          <Tab label="Tokens" {...a11yProps(1)} />
          <Tab onClick={() => getTokens()} label="Entities" {...a11yProps(2)} />
        </Tabs>
      </Box>
      <CustomTabPanel value={value} index={0}>
        {aitext}
      </CustomTabPanel>
      {/*THIS IS THE TOKENS*/}
      <CustomTabPanel value={value} index={1}>
        <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell align="center">Token Text</TableCell>
              <TableCell align="center">Start Index</TableCell>
              <TableCell align="center">End index</TableCell>
            </TableRow>
          </TableHead>
          { aitokens &&<TableBody>
          {aitokens.map((token, i) => ( 
            <TableRow key={token.id}> 
              <TableCell component="th" scope="row"> 
                {token.id} 
              </TableCell> 
              <TableCell align="center"> 
                {aitext.split(" ")[token.id]}
              </TableCell> 
              <TableCell align="center"> 
                {token.start}
              </TableCell> 
              <TableCell align="center"> 
                {token.end} 
              </TableCell> 
            </TableRow>  
                        ))
              }
          </TableBody> }
        </Table>
      </TableContainer>
      </CustomTabPanel> 
      <CustomTabPanel value={value} index={2}>
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell onClick={() => getTokens()}>ID</TableCell>
              <TableCell align="center">Text</TableCell>
              <TableCell align="center">Label</TableCell>
              <TableCell align="center">Start index</TableCell>
              <TableCell align="center">End index</TableCell>
            </TableRow>
          </TableHead>
          { aients &&<TableBody>
          {aients.map((ents, i) => ( 
            <TableRow sx={{backgroundColor: () => returnColor(ents.label)}} key={i}> 
              <TableCell component="th" scope="row"> 
                {i} 
              </TableCell> 
              <TableCell align="center"> 
                {aitext.substring(ents.start, ents.end)}
              </TableCell> 
              <TableCell align="center"> 
                {ents.label}
              </TableCell> 
              <TableCell align="center"> 
                {ents.start} 
              </TableCell> 
              <TableCell align="center"> 
                {ents.end} 
              </TableCell> 
            </TableRow> 
                        ))
              }
          </TableBody> }
        </Table>
      </TableContainer>
      </CustomTabPanel>
    </Box>
  );
  }
  
  export default Result;