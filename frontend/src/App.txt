import React, { useState } from 'react';
import './App.css';

function App() {
  const [inputText, setInputText] = useState('');
  const [responseText, setResponseText] = useState('');

  const handleSubmit = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/greet/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputText }),
      });

      const data = await res.json();
      console.log('レスポンス:', data);
      setResponseText(data.response);
    } catch (err) {
      console.error('エラー:', err);
      setResponseText('エラーが発生しました');
    }
  };

  return (
    <div className="App">
      <h1>翻訳フォーム</h1>
      <input
        type="text"
        value={inputText}
        onChange={e => setInputText(e.target.value)}
        placeholder="文字を入力"
      />
      <button onClick={handleSubmit}>送信</button>
      <p>応答: {responseText}</p>
    </div>
  );
}

export default App;
