// ProfileTable Component - Displays crawled LinkedIn profile data
// This component renders the results of the web crawling operation in a table format

// Import React library for component creation
import React from "react";

// ProfileTable functional component
// Props: profiles - array of profile objects from the API response
const ProfileTable = ({ profiles }) => {
  // Conditional rendering: don't show table if no profiles data
  if (!profiles.length) {
    return null;
  }

  // Main component render
  return (
    // Container div with margin, white background, shadow, and rounded corners
    <div className="mt-10 bg-white shadow-md rounded-lg p-6">
      {/* Section heading */}
      <h2 className="text-xl font-bold mb-4">Crawled Profiles</h2>

      {/* HTML table with full width and border styling */}
      <table className="w-full border-collapse border border-gray-200">
        {/* Table header */}
        <thead>
          <tr>
            {/* Header cells for each data column */}
            <th className="border px-4 py-2">Name</th>
            <th className="border px-4 py-2">Title</th>
            <th className="border px-4 py-2">Location</th>
            <th className="border px-4 py-2">URL</th>
          </tr>
        </thead>

        {/* Table body with dynamic rows */}
        <tbody>
          {/* Map over profiles array to create table rows */}
          {profiles.map((profile, index) => (
            // Each row needs a unique key for React's reconciliation
            <tr key={index}>
              {/* Table cells with profile data, fallback to "N/A" if missing */}
              <td className="border px-4 py-2">{profile.name || "N/A"}</td>
              <td className="border px-4 py-2">{profile.title || "N/A"}</td>
              <td className="border px-4 py-2">{profile.location || "N/A"}</td>

              {/* URL cell with clickable link */}
              <td className="border px-4 py-2">
                <a
                  // Link to the original LinkedIn profile
                  href={profile.url}
                  // Open in new tab for better UX
                  target="_blank"
                  // Security attribute to prevent referrer leakage
                  rel="noopener noreferrer"
                  // Styling for the link
                  className="text-blue-500 hover:underline"
                >
                  Profile Link
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

// Export the component as default export
export default ProfileTable;
