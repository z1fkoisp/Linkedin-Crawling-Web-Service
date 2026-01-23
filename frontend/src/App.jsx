// LinkedIn Web Crawler Frontend - Main Application Component
// This is the root React component that handles the main application logic

// Import React hooks for state management
import React, { useState } from "react";
// Import custom components
import Navbar from "./components/Navbar";
import ProfileTable from "./components/ProfileTable";
// Import HTTP client for API communication
import axios from "axios";

// Main App component - functional component using arrow function syntax
const App = () => {
  // State for storing user input URLs (textarea content)
  const [urls, setUrls] = useState("");
  // State for storing crawled profile data from API
  const [profiles, setProfiles] = useState([]);
  // State for managing loading state during API calls
  const [loading, setLoading] = useState(false);

  // Function to handle the crawl operation when button is clicked
  const handleCrawl = async () => {
    // Set loading state to true to show loading indicator
    setLoading(true);

    // Process the textarea input: split by newlines and trim whitespace
    const profileUrls = urls.split("\n").map((url) => url.trim());

    try {
      // Make POST request to backend API with profile URLs
      const response = await axios.post("http://localhost:8000/crawl", {
        profiles: profileUrls,
      });

      // Update profiles state with API response data
      setProfiles(response.data.profiles);
    } catch (error) {
      // Log error to console for debugging
      console.error("Error fetching profiles:", error);

      // Show user-friendly error message
      alert("Failed to fetch profiles. Check the console for more details.");
    } finally {
      // Always set loading to false when operation completes
      setLoading(false);
    }
  };

  // JSX return - component's render output
  return (
    // Main container with full height and gray background
    <div className="min-h-screen bg-gray-100">
      {/* Navigation bar component */}
      <Navbar />

      {/* Main content container with responsive layout */}
      <div className="container mx-auto py-10">
        {/* Input form section - white card with shadow */}
        <div className="bg-white shadow-md rounded-lg p-6">
          {/* Main heading */}
          <h1 className="text-2xl font-bold mb-4">LinkedIn Web Crawler</h1>

          {/* Textarea for URL input */}
          <textarea
            // Full width, padding, border, and focus styles
            className="w-full p-4 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            // Number of visible rows
            rows="5"
            // Placeholder text for user guidance
            placeholder="Enter LinkedIn profile URLs, one per line"
            // Controlled component - value from state
            value={urls}
            // Update state on user input
            onChange={(e) => setUrls(e.target.value)}
          />

          {/* Crawl button */}
          <button
            // Handle click event
            onClick={handleCrawl}
            // Styling with conditional disabled state
            className="mt-4 w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
            // Disable button while loading
            disabled={loading}
          >
            {/* Conditional text based on loading state */}
            {loading ? "Crawling..." : "Start Crawling"}
          </button>
        </div>

        {/* Profile table component to display results */}
        <ProfileTable profiles={profiles} />
      </div>
    </div>
  );
};

// Export the component as default export
export default App;
