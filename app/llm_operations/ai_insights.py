import re
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session
from transformers import pipeline
from app.models import Call

embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
sentiment_pipeline = pipeline("sentiment-analysis")

FILLER_WORDS = {"um", "uh", "like", "you know", "i mean", "so", "actually", "basically"}


class CallInsightsProcessor:
    def __init__(self):
        self.embedding_model = embedding_model
        self.sentiment_pipeline = sentiment_pipeline

    def clean_and_tokenize(self, text: str):
        words = re.findall(r"\b\w+\b", text.lower())
        return [w for w in words if w not in FILLER_WORDS]

    def compute_agent_talk_ratio(self, transcript: str) -> float:
        agent_lines = re.findall(r"Salesperson:(.*?)\n", transcript, re.DOTALL)
        customer_lines = re.findall(r"Recipient:(.*?)\n", transcript, re.DOTALL)

        agent_words = sum(len(self.clean_and_tokenize(line)) for line in agent_lines)
        customer_words = sum(
            len(self.clean_and_tokenize(line)) for line in customer_lines
        )
        total_words = agent_words + customer_words

        return round(agent_words / total_words, 2) if total_words > 0 else 0.0

    def compute_customer_sentiment(self, transcript: str) -> float:
        customer_lines = " ".join(
            re.findall(r"Recipient:(.*?)\n", transcript, re.DOTALL)
        )
        if not customer_lines.strip():
            return 0.0

        sentiments = self.sentiment_pipeline(customer_lines)
        scores = []
        for s in sentiments:
            if s["label"] == "POSITIVE":
                scores.append(1 * s["score"])
            elif s["label"] == "NEGATIVE":
                scores.append(-1 * s["score"])
            else:
                scores.append(0)
        return round(np.mean(scores), 2) if scores else 0.0

    def compute_embeddings(self, transcript: str) -> list:
        return self.embedding_model.encode([transcript])[0].tolist()

    def process_call(self, call: Call):
        if call.transcript is None:
            return None

        embedding = self.compute_embeddings(call.transcript)
        sentiment = self.compute_customer_sentiment(call.transcript)
        talk_ratio = self.compute_agent_talk_ratio(call.transcript)

        return {
            "call_id": call.call_id,
            "embedding": embedding,
            "customer_sentiment": sentiment,
            "agent_talk_ratio": talk_ratio,
        }


def get_recommendations(call_id: str, db: Session):
    target_call = db.query(Call).filter(Call.call_id == call_id).first()
    if not target_call:
        return {"error": "Call not found"}

    other_calls = db.query(Call).filter(Call.call_id != call_id).all()
    if not other_calls:
        return {
            "call_id": call_id,
            "similar_calls": [],
            "nudges": ["No other calls found."],
        }

    corpus = [target_call.transcript] + [call.transcript for call in other_calls]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)

    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    top_indices = similarities.argsort()[::-1][:5]
    top_calls = [other_calls[i] for i in top_indices]
    top_call_ids = [call.call_id for call in top_calls]

    nudges = [
        "Try to ask more open-ended questions.",
        "Pause to let the customer speak more.",
        "Maintain a friendly tone throughout the call.",
    ]

    return {"call_id": call_id, "similar_calls": top_call_ids, "nudges": nudges}
