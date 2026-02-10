# Skylark Drone Operations Agent

An intelligent assignment and operations management system for drone fleet coordination. Built with FastAPI and integrated with Google Sheets for real-time pilot and drone data.

## Features

- **Smart Assignment**: Automatically match pilots and drones to missions based on skills, certifications, and location
- **Status Management**: Update pilot availability and assignments in real-time
- **Urgent Reassignment**: Handle critical missions by intelligently reassigning available pilots
- **Web UI**: Clean, responsive interface for operator interactions
- **Google Sheets Integration**: Live data sync with Google Sheets

## Quick Start (Local)

### 1. Prerequisites

- Python 3.9+
- Google Sheets API credentials (service account JSON)
- Git

### 2. Setup

```bash
# Clone or download the project
cd skylark-agent

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.\.venv\Scripts\Activate.ps1
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Google Sheets Credentials

**Option A: Environment Variable (Recommended)**
```bash
# PowerShell
$env:GOOGLE_CREDENTIALS = Get-Content credentials.json -Raw
python -m uvicorn app:app --reload

# Bash/Linux/Mac
export GOOGLE_CREDENTIALS=$(cat credentials.json)
python -m uvicorn app:app --reload
```

**Option B: Credentials File**
Place your `credentials.json` in the project root directory.

### 4. Run Locally

```bash
python -m uvicorn app:app --reload
```

Open http://127.0.0.1:8000/ in your browser.

## Deployment

### Deploy to Vercel (Recommended)

See [DEPLOY_VERCEL.md](DEPLOY_VERCEL.md) for detailed step-by-step instructions.

**Quick Summary**:
1. Push code to GitHub
2. Connect repo to Vercel
3. Add `GOOGLE_CREDENTIALS` environment variable
4. Deploy!

### Other Hosting Options

- **Render**: Similar process to Vercel
- **Fly.io**: Docker-based deployment
- **AWS Lambda**: Zappa for serverless FastAPI

## Project Structure

```
skylark-agent/
├── app.py                    # FastAPI application & web UI
├── coordinator.py            # Main business logic
├── matcher.py               # Pilot & drone matching logic
├── sheets.py                # Google Sheets integration
├── conflict_detector.py      # Conflict detection
├── requirements.txt          # Python dependencies
├── vercel.json              # Vercel configuration
├── api/index.py             # Vercel serverless entry point
├── .env.example             # Environment variables template
├── DEPLOY_VERCEL.md         # Vercel deployment guide
└── credentials.json         # (Not in repo) Google API key
```

## API Endpoints

### GET `/`
Returns the web UI interface.

### POST `/chat`
Main chat/command interface.

**Request**:
```json
{
  "message": "your command here"
}
```

**Response**:
```json
{
  "response": "result or action performed"
}
```

**Example Commands**:
- `assign PRJ001` – Find pilots and drones for a project
- `mark Sneha as Available` – Update pilot status
- `urgent Bangalore` – Perform urgent reassignment

## Configuration

### Environment Variables

- `GOOGLE_CREDENTIALS`: Full JSON contents of your Google service account key (required)

See `.env.example` for template.

## Troubleshooting

### "KeyError: GOOGLE_CREDENTIALS"
- Set the environment variable before running
- For Vercel: Add to project Settings → Environment Variables

### Module import errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`

### Google Sheets connection issues
- Verify the service account email is added to your Google Sheet with Editor permission
- Confirm sheet names match exactly (case-sensitive)

## Development

### Adding New Features

1. **New matching logic**: Edit `matcher.py`
2. **New coordinator methods**: Edit `coordinator.py`
3. **New UI components**: Edit HTML in `app.py` route `/`

### Testing

```bash
# Run server in debug mode
python -m uvicorn app:app --reload --log-level debug
```

## License

MIT License - feel free to use and modify.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review [DEPLOY_VERCEL.md](DEPLOY_VERCEL.md) for deployment issues
3. Verify Google Sheets API credentials and permissions
