# 🎤 Voice-to-Issue

Convert voice recordings into GitHub issues automatically using AI-powered speech recognition and intelligent issue parsing.

## ✨ Features

- 🎙️ **Voice Recording**: Web-based voice recording with real-time audio controls
- 🤖 **AI-Powered Parsing**: Uses Claude AI to intelligently parse voice transcriptions into structured GitHub issues
- 📝 **Automatic Issue Creation**: Creates properly formatted GitHub issues with titles, descriptions, and labels
- 💻 **Fallback Text Input**: Text input option for accessibility and when voice recording isn't available
- 📱 **Mobile Responsive**: Works seamlessly on desktop and mobile devices
- 🔄 **Claude Code Integration**: Full GitHub Actions integration for automated development workflow

## 🚀 Quick Start

### 1. Clone and Install

```bash
git clone https://github.com/bobby-langley-personal/voice-to-issue.git
cd voice-to-issue
pip install -r requirements.txt
```

### 2. Environment Setup

Copy the environment template and configure your API keys:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# GitHub Configuration
GITHUB_TOKEN=your_github_token_here

# AI Configuration  
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional: Speech-to-Text Service
SPEECH_API_KEY=your_speech_service_api_key_here
```

### 3. Repository Secrets

For GitHub Actions integration, add these secrets to your repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add the following repository secrets:
   - `ANTHROPIC_API_KEY`: Your Claude API key
   - `GH_PAT`: Your GitHub Personal Access Token

### 4. Create Claude Label

1. Go to **Issues** → **Labels**
2. Create a new label named `claude`
3. This allows Claude Code to automatically respond to issues

### 5. Run the Application

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Access the application at: http://localhost:8000

## 🏗️ Architecture

### Core Components

- **`main.py`**: FastAPI application with voice upload and issue creation endpoints
- **`voice_processor.py`**: Speech-to-text conversion with configurable service backends
- **`issue_creator.py`**: GitHub API integration with AI-powered issue parsing
- **`templates/index.html`**: Modern web interface with voice recording capabilities

### API Endpoints

- `GET /`: Main voice recording interface
- `POST /upload-voice`: Process voice recordings and create issues
- `POST /text-to-issue`: Create issues from text input (fallback)
- `GET /health`: Application health check

## 🎯 Usage

### Web Interface

1. Open the application in your browser
2. Enter your GitHub repository (e.g., `username/repo-name`)
3. Optionally add context information
4. **Record Voice**: Click "Start Recording" and describe your issue
5. **Review**: Listen to your recording using the built-in audio player
6. **Submit**: Click "Create Issue from Recording" to generate the GitHub issue

### Text Fallback

If voice recording isn't available or preferred:

1. Scroll to the "Or Type Your Issue" section
2. Enter your issue description in the text area
3. Click "Create Issue from Text"

## 🔧 Configuration

### Speech-to-Text Services

The application supports multiple speech-to-text services. Configure your preferred service in `voice_processor.py`:

- OpenAI Whisper API
- Google Cloud Speech-to-Text
- Azure Speech Services
- AWS Transcribe

### AI Issue Parsing

Issue parsing uses Claude AI to convert voice transcriptions into structured GitHub issues:

- **Smart Title Generation**: Creates concise, descriptive titles
- **Formatted Descriptions**: Structures content with proper markdown
- **Intelligent Labeling**: Automatically applies relevant labels (bug, feature, enhancement)
- **Context Integration**: Incorporates additional context provided by users

## 🔒 Security

- API keys are stored as environment variables
- GitHub tokens use minimal required permissions
- Audio files are processed in memory (not stored on disk)
- All API communications use secure HTTPS

## 🚀 Deployment

### Heroku

```bash
# Create Heroku app
heroku create your-voice-to-issue-app

# Set environment variables
heroku config:set GITHUB_TOKEN=your_token_here
heroku config:set ANTHROPIC_API_KEY=your_key_here

# Deploy
git push heroku main
```

### Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤖 Claude Code Integration

This repository includes full Claude Code integration:

- **Automatic Issue Handling**: Responds to `@claude` mentions in issues
- **Pull Request Management**: Creates PRs for code changes
- **Workflow Automation**: Handles testing, linting, and deployment

### Using Claude Code

1. Create an issue and mention `@claude`
2. Add the `claude` label to issues for automatic processing
3. Claude will respond with code changes, bug fixes, or feature implementations

## 📊 Development

### Local Development

```bash
# Install development dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn main:app --reload

# Run tests (when available)
pytest
```

### Project Structure

```
voice-to-issue/
├── main.py                     # FastAPI application
├── voice_processor.py          # Speech-to-text processing
├── issue_creator.py            # GitHub API integration
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── templates/
│   └── index.html             # Web interface
└── .github/workflows/
    └── claude.yml             # Claude Code workflow
```

## 🐛 Troubleshooting

### Common Issues

**Microphone Access Denied**
- Check browser permissions for microphone access
- Ensure you're using HTTPS (required for microphone access)
- Try refreshing the page and allowing microphone access

**API Errors**
- Verify your GitHub token has appropriate permissions
- Check that your Anthropic API key is valid and has credits
- Ensure repository name format is correct (`owner/repo`)

**Speech Recognition Issues**
- Speak clearly and avoid background noise
- Check your microphone is working properly
- Try the text input fallback if voice recognition fails

### Debug Mode

Enable debug mode by setting `DEBUG=True` in your `.env` file for detailed error messages.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request with a clear description

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Claude AI**: For intelligent issue parsing and content generation
- **FastAPI**: For the robust web framework
- **GitHub API**: For seamless issue creation and management
- **Modern Web APIs**: For browser-based voice recording capabilities

---

**Generated with [Claude Code](https://claude.ai/code)**
