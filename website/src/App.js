import './App.css';
import { useState } from "react";
import axios from "axios";
import Result from './components/Result';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import Select from '@mui/material/Select';
import Button from '@mui/material/Button';
import MenuItem from '@mui/material/MenuItem';

function App() {
  const [text, setText] = useState(false);
  const [presence, setPresence] = useState(false);
  const [loadedModel, setLoadedModel] = useState("");
  const [api, setApi] = useState(false);
  const [model, setModel] = useState("maccrobat");

  async function getData(text) {
    try {
       let res = await axios({
            url: 'http://127.0.0.1:5000/apply',
            method: 'POST',
            data: [{
              model: model,
              text: text
            }],
            headers: {
                'Content-Type': 'application/json',
            }
        })
        return res.data
    }
    catch (err) {
        console.error(err);
    }
}
  

    const handleChange = (event) => {
      setText(event.target.value);
    }
    const modelChange = (event) => {
      setModel(event.target.value);
      if(loadedModel === event.target.value) {
        setPresence(true)
      } else {
      setPresence(false)
      }
    }
    
    const clicked = (text) => {
      getData(text).then(res => setApi(res)).finally(setPresence(true))
      setLoadedModel(model)
    }


  return (
    <div className="App">
      <header className="App-header">
        <a href={`/admin`} id='references'>Add data</a>
        <h2>NER Model App</h2>
        <FormControl fullWidth>
          <InputLabel id="model">Model</InputLabel>
          <Select
            labelId="model"
            id="model"
            value={model}
            label="Model"
            onChange={e => modelChange(e)}
          >
            <MenuItem value={"maccrobat"}>Maccrobat</MenuItem>
            <MenuItem value={"simple"}>Simple</MenuItem>
            <MenuItem value={"mes"}>MES-Twitter</MenuItem>
          </Select>
        </FormControl>

      <label>Enter text: </label>
      <textarea name="body" onChange={(e) => handleChange(e)}/>
      <Button onClick={() => clicked(text)}>Apply NLP</Button>
      {
        presence && 
        <Result aitext={api.text} aients={api.ents} aitokens={api.tokens} model={model}/>
      }
      </header>
    </div>
  );
}

export default App;
