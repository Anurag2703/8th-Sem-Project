# Install necessary packages (run this once)
# !pip install flask transformers torch pandas nltk nest_asyncio

# Apply fixes for Jupyter notebook async compatibility
import nest_asyncio
nest_asyncio.apply()

# Imports
from flask import Flask, Response, request, render_template
from transformers import AutoModelForCausalLM, AutoTokenizer
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import torch

# Download VADER lexicon for sentiment analysis
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# Load Indian Folklore dataset
folklore_df = pd.read_csv('Indian_Folklore.csv', encoding='ISO-8859-1')

# Strip whitespace from column names
folklore_df.columns = [col.strip() for col in folklore_df.columns]

# Load pre-trained chatbot model
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# Define emotion keywords
emotion_keywords = {"sad", "happy", "angry", "joyful", "upset", "depressed", "excited", "fearful"}

# Flask app setup
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("chat.html")  # Ensure this file exists in your templates folder

@app.route("/get", methods=["POST"])
def chat():
    msg = request.form["msg"]
    input_text = msg.lower()
    response_text = get_chat_response(input_text)
    return Response(response_text, content_type='text/plain')

def analyze_sentiment(text):
    sentiment = sia.polarity_scores(text)
    if sentiment['compound'] >= 0.05:
        return 'positive'
    elif sentiment['compound'] <= -0.05:
        return 'negative'
    else:
        return 'neutral'

def suggest_folklore(sentiment):
    required_columns = [
        "Story Heading",
        "Body Of Story",
        "Moral Of Story",
        "Bhagavad Gita Reference"
    ]
    
    if not all(col in folklore_df.columns for col in required_columns):
        return {
            "heading": "Missing data",
            "story": "One or more expected columns are not present in the dataset.",
            "moral": "",
            "reference": ""
        }

    sample = folklore_df.sample().iloc[0]
    return {
        "heading": sample["Story Heading"].strip(),
        "story": sample["Body Of Story"].strip(),
        "moral": sample["Moral Of Story"].strip(),
        "reference": sample["Bhagavad Gita Reference"].strip()
    }

def get_chat_response(text):
    if any(word in text for word in emotion_keywords):
        sentiment = analyze_sentiment(text)
        folklore = suggest_folklore(sentiment)

        return (
            f"You're feeling {sentiment}.\n\n"
            f"🧚‍♂ Folklore: {folklore['heading']}\n"
            f"Story: {folklore['story']}\n"
            f"Moral: {folklore['moral']}\n"
            f"Gita Reference: {folklore['reference']}"
        )
    else:
        user_input_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors='pt')
        response_ids = model.generate(user_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
        bot_response = tokenizer.decode(response_ids[:, user_input_ids.shape[-1]:][0], skip_special_tokens=True)
        return bot_response

# Start Flask app in Jupyter
app.run(port=5000)