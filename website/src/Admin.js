import './Admin.css';
import { useState, useEffect } from "react";
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { FormControl, FormLabel, Grid } from '@mui/material';


function Admin() {
  const [text, setText] = useState(false);
  const [ftext, setFText] = useState(false);
  const [words, setWords] = useState({});
  const [addedWords, setAddedWords] = useState({});

  useEffect(() => {
    console.log("Words", words);
  },[ftext, words]);

  const handleChange = (event) => {
    setText(event.target.value);
  }

  function handleData() {
    let temp = {}
    const temparray = text.split(/ /g);
    let idx = false;
    let lastidx = 0;
    temparray.map((w,id) => {
      let subtext = text;
      let content = {};
      if (lastidx !== 0) {
        subtext = subtext.substring(lastidx)
      }
      const getStartEnd = (str, sub) => [str.indexOf(sub), str.indexOf(sub) + sub.length - 1]
      if (Object.keys(temp).length === 0) {
        idx = 0;
      } else {
        idx = Object.keys(temp).length
      }
      w = w.replace(/[^a-zA-Z0-9 ]/g, '');
      let indexes = getStartEnd(subtext, w)
      content['word'] = w;
      content['start'] = indexes[0] + lastidx
      content['end'] = indexes[1] + lastidx
      lastidx = content['end']
      content['clicked'] = false
      temp[idx] = content
  });
    setWords(temp)
    setFText(text)
  }

  function addWord(idx) {
    addedWords[idx] = words[idx]
    let coppiedWords = {...words};
    coppiedWords[idx].clicked = true;
    setWords(words => ({...coppiedWords}))
  }

  function wordMapping() {
    return (
    <>
      <p>Add words</p>
      <Grid item xs="auto">
        {Object.entries(words).map( ([key, value]) =>{
          if (!value.clicked) return <Button onClick={()=>addWord(key)} sx={{color:"red"}}>{value.word}</Button>
        })}
      </Grid>
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
            <Button onClick={(words) => handleData()}>Submit text</Button>
        </FormControl>
        {!(Object.keys(words).length === 0) && wordMapping()}
      </body>
    </div>
  );
}

export default Admin;
