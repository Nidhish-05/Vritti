import logging
from src.processing.sentiment import SentimentPipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_sentiment():
    # 1. Instantiate the Pipeline
    print("=== INITIALIZING FINBERT PIPELINE ===")
    print("(Note: This will download a ~400MB model on the first run. Please wait...)")
    pipeline = SentimentPipeline()
    
    # 2. Sample financial sentences
    test_sentences = [
        "Tesla stock price surges 10% after blowing past quarterly earnings estimates.",
        "Microsoft announces layoffs of 10,000 employees amid economic slowdown.",
        "Apple Inc. plans to release a new color for the iPhone 15 this autumn.",
        "Arbitrary text about weather is neutral."
    ]
    
    # 3. Get scores
    print("\n=== RUNNING INFERENCE ===")
    results = pipeline.score(test_sentences)
    
    # 4. Print results
    for sentence, result in zip(test_sentences, results):
        print(f"\nSentence: '{sentence}'")
        print(f"Sentiment: {result['label'].upper()} (Confidence: {result['score']:.4f})")

if __name__ == "__main__":
    test_sentiment()
