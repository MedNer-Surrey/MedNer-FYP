import './App.css';
import { useState } from "react";
import axios from "axios";
import Result from './components/Result';


function App() {
  const [text, setText] = useState(false);
  const [presence, setPresence] = useState(false);
  const [api, setApi] = useState(false);

  async function getData(text) {
    try {
       let res = await axios({
            url: 'http://127.0.0.1:5000/profile?text=' + text,
            method: 'get',
            timeout: 8000,
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
    
    const clicked = (text) => {
      console.log("Clicked and text is " + text);
      getData(text).then(res => setApi(res)).finally(setPresence(true))
    }


  return (
    <div className="App">
      <header className="App-header">
      <label>Enter text: </label>
      <textarea name="body" onChange={(e) => handleChange(e)}/>
      <button onClick={() => clicked(text)}>Apply NLP</button>
      {
        presence && 
        <Result aitext={api.text} aients={api.ents} aitokens={api.tokens}/> // CREATE COMPONENT FOR NLP TEXT AND ADD IT HERE
      }
      </header>
    </div>
  );
}

export default App;
