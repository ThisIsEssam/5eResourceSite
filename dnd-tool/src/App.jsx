import React from 'react';
import ReactDOM from 'react-dom/client'
import NPCCreator from './components/NPCCreator';
import 'bulma/css/bulma.min.css';

ReactDOM.createRoot(document.getElementById('app')).render(
  <React.StrictMode>
    <NPCCreator />
  </React.StrictMode>
);
