// LinkedIn Web Crawler Frontend - Application Entry Point
// This file is the main entry point for the React application
// It sets up React, imports global styles, and renders the App component

// Import React library - core functionality for building components
import React from "react";
// Import ReactDOM for rendering React components to the DOM
import ReactDOM from "react-dom/client";
// Import global CSS styles (Tailwind CSS and custom styles)
import "./index.css";
// Import the main App component
import App from "./App";

// Create a React root and render the application
// This is the modern way to render React 18+ applications
ReactDOM.createRoot(document.getElementById("root")).render(
  // StrictMode helps identify potential problems in the application
  // It activates additional checks and warnings for its descendants
  <React.StrictMode>
    {/* Render the main App component */}
    <App />
  </React.StrictMode>
);
