// Navbar Component - Application Navigation Header
// This component provides the main navigation bar for the LinkedIn Web Crawler application

// Import React library for component creation
import React from "react";

// Navbar functional component - no props needed for this simple navigation
const Navbar = () => {
  return (
    // Navigation element with blue background, white text, and vertical padding
    <nav className="bg-blue-500 text-white py-4">
      {/* Container with responsive centering and flexbox layout */}
      <div className="container mx-auto flex justify-between items-center">
        {/* Application title/logo - positioned on the left */}
        <h1 className="text-xl font-bold">LinkedIn Crawler</h1>

        {/* Future navigation items could go here (right side) */}
        {/* Examples: user menu, settings, help, etc. */}
        <div className="hidden md:flex space-x-4">
          {/* Placeholder for navigation links */}
          {/* <a href="#" className="hover:underline">About</a> */}
          {/* <a href="#" className="hover:underline">Help</a> */}
        </div>
      </div>
    </nav>
  );
};

// Export the component as default export
export default Navbar;
