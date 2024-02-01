import './Admin.css';
import { useState } from "react";
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { FormControl, FormLabel, Grid } from '@mui/material';


function Admin() {
  const [text, setText] = useState(false);
  const [ftext, setFText] = useState(false);
  const [words, setWords] = useState([]);
  
  function clickcallback(w) {
    console.log("Clicked ", w)
    setWords([...words, w])
    console.log(words)
  };

  const handleChange = (event) => {
    setText(event.target.value);
    console.log(text)
  }

  const handleRemoveItem = (idx) => {
    const temp = [...words];
    temp.splice(idx,1);
    setWords(temp);
} 

  function clickablewords(paragraph, clickcallback) {
    const words = paragraph.split(/ /g);
    return (
      <>
        {words.map(w => 
      <span id='word' onClick={() => clickcallback(w.replace(/[^a-zA-Z0-9 ]/g, ''))}>{w.replace(/[^a-zA-Z0-9 ]/g, '')} </span>
        )}
      </>
      )
  }


  return (
    <div className="Admin">
      <header className="Admin-header">
        <a href={`/`} id='references'>Main page</a>
      </header>
      <body className="Admin-body">
        <FormControl>
            <FormLabel sx={{color:"white"}}>Text</FormLabel>
            <TextField sx={{ input: { color: 'white' } }} onChange={e => handleChange(e)}></TextField>
            <Button onClick={() => setFText(text)}>Submit text</Button>
            {ftext && <p>Select word(s) to add a label:</p>}
            {ftext && clickablewords(text, clickcallback)}
        </FormControl>
        <br/>
        <br/>
        {ftext && <p>Click to remove word(s) from selected:</p>}
        <Grid container spacing={0} alignItems="center" justifyContent="center">
        {ftext && ftext.map((word,idx) => 
        <>
          <Grid key={idx} item xs="auto">
            <Button onClick={() => handleRemoveItem(idx)} sx={{color:"red"}}>{word}</Button>
          </Grid>
        </>
        )}
        </Grid>
      </body>
    </div>
  );
}

export default Admin;
