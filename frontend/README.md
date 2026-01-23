# LinkedIn Web Crawler Frontend

<!-- Project Title and Description -->
A modern React-based frontend interface for the LinkedIn Web Crawler application, built with Vite for fast development and optimized production builds.

## Overview

<!-- Brief description of what this frontend does -->
This frontend provides a user-friendly web interface for the LinkedIn Web Crawler backend API. Users can input LinkedIn profile URLs, initiate crawling operations, and view extracted data in a clean, responsive interface.

## Technology Stack

<!-- List of key technologies used -->
- **React 19** - Modern JavaScript library for building user interfaces
- **Vite 6** - Fast build tool and development server
- **Tailwind CSS 4** - Utility-first CSS framework for styling
- **Axios** - HTTP client for API communication
- **React Router** - Client-side routing
- **ESLint** - Code linting and formatting

## Features

<!-- Key features of the frontend -->
- **Responsive Design** - Works on desktop and mobile devices
- **Real-time Updates** - Live status updates during crawling operations
- **Clean UI** - Modern interface with Tailwind CSS styling
- **Error Handling** - User-friendly error messages and loading states
- **Fast Development** - Hot Module Replacement (HMR) with Vite

## Prerequisites

<!-- System requirements -->
- Node.js 18.0.0 or higher
- npm 9.0.0 or higher
- Backend API running (see main project README)

## Installation

<!-- Step-by-step installation instructions -->
1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

4. **Open browser**
   - Navigate to `http://localhost:5173`
   - The application will automatically reload on code changes

## Available Scripts

<!-- Explanation of npm scripts -->
- `npm run dev` - Start development server with hot reload
- `npm run build` - Build for production (output in `dist/` folder)
- `npm run preview` - Preview production build locally
- `npm run lint` - Run ESLint for code quality checks
- `npm run type-check` - Run TypeScript type checking (if applicable)

## Project Structure

<!-- File organization explanation -->
```
frontend/
├── public/                 # Static assets
├── src/
│   ├── components/         # Reusable React components
│   │   ├── Navbar.jsx      # Navigation component
│   │   └── ProfileTable.jsx # Data display component
│   ├── App.jsx             # Main application component
│   ├── main.jsx            # Application entry point
│   └── assets/             # Component-specific assets
├── index.html              # HTML template
├── package.json            # Dependencies and scripts
├── vite.config.js          # Vite configuration
├── tailwind.config.js      # Tailwind CSS configuration
├── postcss.config.js       # PostCSS configuration
├── eslint.config.js        # ESLint configuration
└── README.md               # This file
```

## Development

<!-- Development guidelines -->
### Code Style
- Follow React best practices
- Use functional components with hooks
- Maintain consistent naming conventions
- Run `npm run lint` before committing

### Adding New Components
1. Create component in `src/components/`
2. Import and use in `App.jsx`
3. Follow existing component patterns

### API Integration
- Use Axios for HTTP requests
- Handle loading states and errors
- Update UI based on API responses

## Building for Production

<!-- Production build instructions -->
```bash
# Create optimized production build
npm run build

# Preview production build
npm run preview
```

The build artifacts will be stored in the `dist/` directory.

## Configuration

<!-- Configuration files explanation -->
- **Vite Config** (`vite.config.js`) - Build tool configuration
- **Tailwind Config** (`tailwind.config.js`) - CSS framework settings
- **ESLint Config** (`eslint.config.js`) - Code quality rules
- **PostCSS Config** (`postcss.config.js`) - CSS processing

## Browser Support

<!-- Supported browsers -->
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

<!-- Contribution guidelines -->
1. Follow the existing code style
2. Test your changes thoroughly
3. Run linting before submitting
4. Update documentation as needed

## Troubleshooting

<!-- Common issues and solutions -->
### Common Issues
- **Port already in use**: Change port in `vite.config.js`
- **API connection failed**: Ensure backend is running
- **Build errors**: Check Node.js version compatibility

### Getting Help
- Check the main project README for backend setup
- Review browser console for errors
- Ensure all dependencies are installed

---

<!-- Footer with project info -->
*Part of the LinkedIn Web Crawler project - See main README for full documentation*
