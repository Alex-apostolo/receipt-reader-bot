# Receipt Reader Bot

A Telegram bot that helps users analyze and track their expenses using AI. The bot can process receipt information, extract relevant details, and automatically update Google Sheets with expense data.

## Features

- 🤖 AI-powered receipt analysis using OpenAI's GPT models
- 🔐 Secure Google OAuth integration with function calling for spreadsheet updates
- 📊 Automatic expense tracking in Google Sheets
- 💬 Interactive Telegram interface

## Architecture

### Tech Stack

- **Backend**: Python with FastAPI
- **AI/ML**:
  - OpenAI GPT for receipt analysis and function calling
- **Database**: Firebase Firestore
- **Authentication**:
  - Telegram Bot API
  - Google OAuth 2.0
- **Cloud Platform**: Google Cloud Run
- **Storage**: Google Cloud Storage (for temporary receipt storage)

### System Design

The application is designed with the following considerations:

1. **Concurrent Request Handling**:

   - FastAPI's async capabilities for handling multiple requests
   - Firebase Firestore for concurrent data access
   - Stateless design for horizontal scaling

2. **Rate Limiting and Quotas**:

   - OpenAI API rate limiting handled through request queuing
   - Google API quotas managed through proper error handling

3. **Read-Heavy Workload**:

   - Firebase Firestore optimized for read operations
   - Caching layer for frequently accessed data
   - Efficient data structure design for quick retrieval

4. **Scalability**:

   - Containerized deployment on Google Cloud Run
   - Automatic scaling based on traffic
   - Stateless architecture for easy scaling
   - Distributed request handling across multiple instances
   - Load balancing for optimal resource utilization
   - Efficient resource allocation during peak times
   - Automatic instance scaling based on CPU and memory usage

5. **Security Considerations**:

   - All sensitive credentials are stored in Google Cloud Secret Manager
   - Firebase security rules for data access control
   - Secure OAuth flow for Google integration
   - Temporary file cleanup after processing

## Setup Instructions

### Prerequisites

- Python 3.11+
- Google Cloud Platform account
- Telegram Bot Token
- OpenAI API key
- Firebase project

### Environment Variables

Create a `.env` file with the following variables:

```env
TELEGRAM_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=your_redirect_uri
WEBHOOK_URL=your_webhook_url
```

### Local Development

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

### Deployment

The application is deployed on Google Cloud Run. To deploy:

1. Build and push the container:

   ```bash
   gcloud builds submit
   ```

2. The deployment will automatically:
   - Build the Docker container
   - Push it to Google Container Registry
   - Deploy to Cloud Run
   - Configure secrets and environment variables

## Project Structure

```
receipt-reader-bot/
├── app/
│   ├── agents/         # AI agents for receipt processing
│   ├── handlers/       # Request handlers
│   ├── models/         # Data models
│   ├── services/       # Business logic and external services
│   ├── tools/          # Utility functions
│   ├── utils/          # Helper functions
│   ├── config.py       # Configuration
│   ├── main.py         # Application entry point
│   └── telegram_bot.py # Telegram bot implementation
├── temp_receipts/      # Temporary storage for receipt images
├── Dockerfile          # Container configuration
├── requirements.txt    # Python dependencies
└── cloudbuild.yaml     # Cloud Build configuration
```

## License

MIT License
