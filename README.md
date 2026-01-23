# LinkedIn Web Crawler

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18.3.1-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)

A comprehensive web scraping tool designed to extract publicly available data from LinkedIn profiles and company pages. Built with Python backend using Selenium and BeautifulSoup, and a modern React frontend for easy interaction.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)

## Overview

The LinkedIn Web Crawler is a full-stack application that automates the extraction of publicly available information from LinkedIn. It provides both a programmatic API and a user-friendly web interface for managing crawl operations.

The system consists of:
- **Backend API**: FastAPI-based REST service handling crawl requests and data processing
- **Web Crawler**: Selenium-powered scraper with anti-detection measures
- **Frontend Interface**: React application for initiating crawls and viewing results

## Features

### Core Functionality
- **Profile Scraping**: Extract detailed information from LinkedIn user profiles
- **Company Page Scraping**: Gather data from LinkedIn company pages
- **Batch Processing**: Handle multiple URLs in a single request
- **Real-time Results**: Immediate feedback through the web interface

### Data Extraction
- **User Profiles**:
  - Full name
  - Current job title
  - Location
  - Profile URL
- **Company Pages**:
  - Company name
  - Industry
  - Headquarters
  - Overview/description

### Technical Features
- **Anti-Bot Protection**: Headless browser operation with randomized delays
- **Error Handling**: Robust error management and retry mechanisms
- **JSON Output**: Structured data format for easy integration
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Technologies Used

### Backend
- **Python 3.8+**: Core programming language
- **FastAPI**: Modern, fast web framework for building APIs
- **Selenium**: Browser automation for web scraping
- **BeautifulSoup4**: HTML parsing and data extraction
- **Uvicorn**: ASGI server for FastAPI

### Frontend
- **React 18**: User interface library
- **Vite**: Fast build tool and development server
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API communication
- **React Router**: Client-side routing

### Development Tools
- **Chrome WebDriver**: Browser automation
- **ESLint**: JavaScript linting
- **PostCSS**: CSS processing

## Prerequisites

Before running this application, ensure you have the following installed:

### System Requirements
- **Python 3.8 or higher**
- **Node.js 16 or higher**
- **Google Chrome browser**
- **Git** (for cloning the repository)

### Python Dependencies
- fastapi
- uvicorn
- selenium
- beautifulsoup4

### Node.js Dependencies
- react
- react-dom
- axios
- tailwindcss
- vite

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/kartikgurnani/Linkedin-Crawling-Web-Service.git
cd Linkedin-Crawling-Web-Service
```

### 2. Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Chrome WebDriver:
   - Download from [ChromeDriver](https://chromedriver.chromium.org/)
   - Ensure it's in your system PATH

### 3. Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

## Configuration

### LinkedIn Credentials

The application requires LinkedIn login credentials to access profile data. Create environment variables or a `.env` file in the backend directory:

```bash
LINKEDIN_USERNAME=your_linkedin_email@example.com
LINKEDIN_PASSWORD=your_linkedin_password
```

**Security Note**: Never commit credentials to version control. Use environment variables or secure credential management.

### Optional Configuration

- **Headless Mode**: The crawler runs in headless Chrome by default
- **Rate Limiting**: Built-in delays prevent detection
- **Proxy Support**: Can be configured in `crawler.py` for enhanced anonymity

## Usage

### Running the Application

1. **Start the Backend**:
   ```bash
   cd backend
   python main.py
   ```
   The API will be available at `http://localhost:8000`

2. **Start the Frontend** (in a new terminal):
   ```bash
   cd frontend
   npm run dev
   ```
   The web interface will be available at `http://localhost:5173`

### Using the Web Interface

1. Open your browser and navigate to `http://localhost:5173`
2. Enter LinkedIn profile URLs (one per line) in the text area
3. Click "Start Crawling" to begin the process
4. View results in the table below

### Example URLs

```
https://www.linkedin.com/in/johndoe
https://www.linkedin.com/in/janesmith
https://www.linkedin.com/company/example-company
```

## API Documentation

### POST /crawl

Initiate a crawling operation for multiple LinkedIn profiles.

**Request Body:**
```json
{
  "profiles": [
    "https://www.linkedin.com/in/username1",
    "https://www.linkedin.com/in/username2"
  ]
}
```

**Response:**
```json
{
  "profiles": [
    {
      "name": "John Doe",
      "title": "Software Engineer",
      "location": "San Francisco, CA",
      "url": "https://www.linkedin.com/in/username1"
    },
    {
      "name": "Jane Smith",
      "title": "Product Manager",
      "location": "New York, NY",
      "url": "https://www.linkedin.com/in/username2"
    }
  ]
}
```

**Error Response:**
```json
{
  "detail": "Error message describing the issue"
}
```

## Project Structure

```
Linkedin-Crawling-Web-Service/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py          # Application configuration
│   │   ├── crawler.py         # Main crawling logic
│   │   ├── credentials.py     # Credential management
│   │   ├── routes.py          # API route definitions
│   │   └── utils.py           # Utility functions
│   ├── main.py                # Application entry point
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── public/                # Static assets
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── Navbar.jsx
│   │   │   └── ProfileTable.jsx
│   │   ├── App.jsx            # Main application component
│   │   ├── index.jsx          # Application entry point
│   │   ├── main.jsx           # React root
│   │   └── assets/            # Static assets
│   ├── package.json           # Node.js dependencies
│   ├── vite.config.js         # Vite configuration
│   ├── tailwind.config.js     # Tailwind CSS configuration
│   └── postcss.config.js      # PostCSS configuration
├── static/                    # Screenshots and images
├── LICENSE                    # MIT License
└── README.md                  # This file
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -am 'Add new feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint configuration for JavaScript/React
- Add tests for new features
- Update documentation as needed
- Ensure cross-platform compatibility

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

**Important Legal Notice:**

This tool is intended for educational and research purposes only. LinkedIn's Terms of Service prohibit unauthorized scraping of their platform. The use of this software to scrape LinkedIn data may violate LinkedIn's terms and conditions, and could potentially infringe on copyright laws or other applicable regulations.

**By using this software, you agree to:**
- Use it only on publicly available LinkedIn profiles
- Respect LinkedIn's robots.txt file
- Not use the scraped data for commercial purposes without permission
- Comply with all applicable laws and regulations

The developers of this project are not responsible for any misuse or legal consequences arising from the use of this software. Always ensure compliance with LinkedIn's terms of service and applicable laws before using this tool.

---


