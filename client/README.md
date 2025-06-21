
# Layoff Radar Dashboard

A responsive, AI-powered dashboard for analyzing company layoff risks. Built with React, Vite, TypeScript, and Tailwind CSS.

## Features

- **Risk Analysis**: Visual gauge showing layoff risk score (0-100)
- **Factor Analysis**: SHAP-style visualization of contributing factors
- **Trend Tracking**: 30-day sparkline chart showing risk history
- **Dark Mode**: Toggle between light and dark themes
- **Recent Lookups**: Quick access to recently searched companies
- **Responsive Design**: Mobile-first approach with adaptive layouts

## Getting Started

### Prerequisites

- Node.js (version 16 or higher)
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd layoff-radar
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API configuration
```

4. Start the development server:
```bash
npm run dev
```

5. Open your browser and visit `http://localhost:5173`

## API Integration

The dashboard expects a REST API endpoint at `/score/<company>` that returns:

```json
{
  "company": "Tesla",
  "risk": 82,
  "top_factors": [
    {"name": "Executive exits", "value": 0.34},
    {"name": "Layoff-intent news", "value": 0.28},
    {"name": "Funding cushion", "value": -0.05}
  ],
  "history": [
    {"date": "2025-06-11", "risk": 78}
  ],
  "explanation": "High risk mainly because..."
}
```

## Configuration

Set your API base URL in the `.env` file:

```env
VITE_API_BASE_URL=https://your-api-domain.com
```

## Building for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## Technologies Used

- **React** - UI framework
- **Vite** - Build tool and dev server
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Recharts** - Data visualization
- **Radix UI** - Accessible components
- **Lucide React** - Icons

## License

MIT License
