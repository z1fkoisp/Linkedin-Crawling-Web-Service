// LinkedIn Web Crawler Frontend - Vite Entry Point
// This is the main entry point file created by Vite for React applications
// It sets up the React application and mounts it to the DOM

// Import StrictMode component for development checks and warnings
import { StrictMode } from 'react'
// Import createRoot function for React 18+ concurrent features
import { createRoot } from 'react-dom/client'
// Import global CSS styles (Tailwind and custom styles)
import './index.css'
// Import the main App component
import App from './App.jsx'

// Create a React root container and render the application
// This replaces the older ReactDOM.render() method
createRoot(document.getElementById('root')).render(
  // Wrap the app in StrictMode for additional development checks
  // StrictMode helps identify potential problems and unsafe practices
  <StrictMode>
    {/* Render the main App component */}
    <App />
  </StrictMode>,
)
