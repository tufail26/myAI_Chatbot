import requests
import json
import time

class GeminiChatbot:
    """
    A class to interact with the Gemini API, modified to be stateless
    and handle chat history from an external source (like Streamlit).
    """
    def __init__(self, api_key):
        """
        Initializes the chatbot with the API key.
        """
        if not api_key:
            raise ValueError("API key cannot be empty")
            
        self.api_key = api_key
        # Updated to a current model
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent"
    
    def send_message(self, chat_history, max_retries=3):
        """
        Send the entire chat history to Gemini and get a response.
        
        Args:
            chat_history (list): A list of message objects, where each object
                                 has "role" ("user" or "model") and "parts".
                                 e.g., [{"role": "user", "parts": [{"text": "Hello"}]}]
            max_retries (int): Number of times to retry on rate limiting.
        
        Returns:
            str: The bot's response text or an error message.
        """
        try:
            url = f"{self.base_url}?key={self.api_key}"
            
            headers = {
                "Content-Type": "application/json"
            }
            
            # The payload now takes the entire chat history
            payload = {
                "contents": chat_history,
                "generationConfig": {
                    "temperature": 0.9,
                    "topK": 1,
                    "topP": 1,
                    "maxOutputTokens": 2048
                }
            }
            
            # Implement exponential backoff for retries
            for i in range(max_retries):
                response = requests.post(url, headers=headers, json=payload)
                
                if response.status_code == 429:
                    # Rate limited, wait and retry
                    wait_time = 2 ** i
                    print(f"Rate limited. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                
                # Check for other errors
                response.raise_for_status() # Raises an HTTPError for bad responses
                
                data = response.json()
                
                # Extract the response text
                if "candidates" in data and len(data["candidates"]) > 0:
                    candidate = data["candidates"][0]
                    # Check for safety ratings
                    if "finishReason" in candidate and candidate["finishReason"] == "SAFETY":
                        return "Sorry, I couldn't generate a response due to safety settings."
                    
                    if "content" in candidate and "parts" in candidate["content"] and len(candidate["content"]["parts"]) > 0:
                        bot_response = candidate["content"]["parts"][0]["text"]
                        return bot_response
                
                # Handle cases where no response is generated
                return "Sorry, I couldn't generate a response. The API returned an empty candidate list."

            return "Error: The request was rate-limited multiple times. Please try again later."

        except requests.exceptions.HTTPError as http_err:
            try:
                error_data = response.json()
                message = error_data.get('error', {}).get('message', 'Unknown HTTP error')
                return f"Error: {message}"
            except json.JSONDecodeError:
                return f"HTTP Error: {http_err}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"
