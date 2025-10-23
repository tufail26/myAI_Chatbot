# 🤖 My AI Chatbot

A Streamlit-based chat interface that uses Google's Gemini API to create an interactive AI chatbot experience.

## Features

- 🚀 Modern, clean interface built with Streamlit
- 🔒 Secure API key management
- 💬 Interactive chat interface
- 🔄 Persistent chat history within sessions
- ⚡ Real-time responses from Gemini API
- 🛡️ Error handling and rate limiting protection

## Prerequisites

- Python 3.6 or higher
- A Gemini API key (Get it from [Google AI Studio](https://aistudio.google.com/app/apikey))

## Installation

1. Clone this repository:
```bash
git clone https://github.com/tufail26/myAI_Chatbot.git
cd myAI_Chatbot
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

There are two ways to configure your Gemini API key:

1. **Recommended: Using Streamlit Secrets**
   - Create a `.streamlit/secrets.toml` file
   - Add your API key:
     ```toml
     GEMINI_API_KEY = "your-api-key-here"
     ```

2. **Alternative: Input at Runtime**
   - Enter your API key directly in the web interface when prompted

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically `http://localhost:8501`)

3. If you haven't configured the API key in secrets, enter it when prompted

4. Start chatting with the AI!

## Project Structure

- `app.py` - Main Streamlit application interface
- `chatbot_backend.py` - Backend class for Gemini API integration
- `requirements.txt` - Project dependencies
- `.streamlit/secrets.toml` - (Optional) Configuration file for API key

## Technical Details

The chatbot uses:
- Gemini API version: 2.5-flash-preview-09-2025
- Temperature: 0.9
- Max Output Tokens: 2048
- Built-in retry mechanism with exponential backoff for rate limiting

## Security Notes

- Never commit your API key to version control
- Prefer using Streamlit secrets over runtime input for API key management
- The application includes basic error handling and input validation

## License

[MIT License](LICENSE)

## Contributing

Feel free to open issues or submit pull requests for improvements!

## Author

[@tufail26](https://github.com/tufail26)