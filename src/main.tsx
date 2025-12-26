import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'


// GLOBAL ERROR HANDLER FOR DEBUGGING
window.onerror = function (message, source, lineno, colno, error) {
  const root = document.getElementById('root');
  if (root) {
    root.innerHTML = `
      <div style="padding: 20px; color: red; font-family: monospace; background: white;">
        <h1>Application Crashed</h1>
        <p><strong>Error:</strong> ${message}</p>
        <p><strong>Source:</strong> ${source}:${lineno}:${colno}</p>
        <p><strong>Stack:</strong> ${error?.stack}</p>
      </div>
    `;
  }
};

try {
  createRoot(document.getElementById('root')!).render(
    <StrictMode>
      <App />
    </StrictMode>,
  )
} catch (e) {
  console.error("Render failed", e);
  document.body.innerHTML = `<h1 style="color:red">Render Fatal: ${e}</h1>`;
}
