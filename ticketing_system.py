from flask import Flask, request, jsonify
import pandas as pd

from flask_socketio import SocketIO
app = Flask(__name__)
socketio = SocketIO(app)


import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download NLTK resources (only needed once)
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('vader_lexicon')

# Create a dummy dataset
data = {
    'Description': [
        "I'm experiencing connectivity issues with my internet.",
        "The software is crashing frequently after the latest update.",
        "I have a question about my recent bill.",
        "The printer is not responding to print commands.",
        "I accidentally deleted some important files. Can they be recovered?",
        "The website is displaying error 404 when I try to access my account.",
        "I need assistance setting up my new email account.",
        "The application is freezing and becoming unresponsive.",
        "I received an error message 'Out of memory' while working on a project.",
        "My computer is overheating and shutting down unexpectedly."
    ],
    'Category': [
        "Technical",
        "Technical",
        "Billing",
        "Technical",
        "Technical",
        "Technical",
        "Technical",
        "Technical",
        "Technical",
        "Technical"
    ],
    'Urgency': [
        "High",
        "Medium",
        "Low",
        "High",
        "High",
        "Medium",
        "Low",
        "High",
        "High",
        "High"
    ],
    'Resolution': [
        "Reboot your modem and router and check for loose cables.",
        "Roll back the software update or reinstall the previous version.",
        "Contact our billing department at billing@example.com for assistance.",
        "Check the printer connections and restart both the printer and the computer.",
        "Use data recovery software to attempt to recover the deleted files.",
        "Clear your browser cache and cookies, or try accessing the website from a different browser.",
        "Follow the step-by-step guide on our website for setting up your email account.",
        "Close unnecessary applications and update the software to the latest version.",
        "Close unnecessary programs and consider upgrading your RAM if the issue persists.",
        "Clean the dust from your computer's vents and ensure proper airflow."
    ]
}

# Convert the dictionary to a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv('past_tickets.csv', index=False)

# Load dataset containing past tickets and their resolutions
tickets_df = pd.read_csv('past_tickets.csv')

class TicketAnalyzer:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.sid = SentimentIntensityAnalyzer()
        self.tfidf_vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(tickets_df['Description'])

    def preprocess_text(self, text):
        tokens = word_tokenize(text.lower())
        processed_tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token not in self.stop_words]
        return ' '.join(processed_tokens)

    def analyze_sentiment(self, text):
        sentiment_score = self.sid.polarity_scores(text)['compound']
        return sentiment_score

    def categorize_and_prioritize_ticket(self, description, urgency):
        # Preprocess description
        processed_text = self.preprocess_text(description)
        
        # Analyze sentiment
        sentiment_score = self.analyze_sentiment(description)

        # Perform TF-IDF vectorization
        description_vector = self.tfidf_vectorizer.transform([processed_text])
        
        # Calculate cosine similarity between input ticket and past tickets
        similarities = cosine_similarity(description_vector, self.tfidf_matrix)

        # Find the most similar past ticket
        most_similar_idx = similarities.argmax()
        category = tickets_df.iloc[most_similar_idx]['Category']
        resolution = tickets_df.iloc[most_similar_idx]['Resolution']

        # Prioritize based on urgency and sentiment
        if urgency == 'High' or sentiment_score < 0:
            priority = 'High Priority'
        else:
            priority = 'Normal Priority'

        return category, priority, resolution

# Example usage (assuming user input is received from the form)
@app.route('/resolveTicket', methods=['POST'])
def resolve_ticket():
    # Extract data from the form
    ticket_data = request.json
    description = ticket_data.get('description')
    urgency = ticket_data.get('urgency')

    # Perform ticket resolution based on description
    ticket_analyzer = TicketAnalyzer()
    category, priority, resolution = ticket_analyzer.categorize_and_prioritize_ticket(description, urgency)

    # Log the resolution on the server side
    print('Resolution:', resolution)

    # Send resolution to WebSocket server
    socketio.emit('resolution', resolution)

    # Return a generic response indicating that the ticket is being processed
    return jsonify({'message': 'Your ticket has been submitted and will be processed shortly.'})



if __name__ == '__main__':
    app.run(port=8000)
