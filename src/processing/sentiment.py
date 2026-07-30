import logging
from transformers import pipeline, pipelines

logger = logging.getLogger(__name__)

class SentimentPipeline:
    """
    Class to wrap the FinBERT NLP model and perform sentiment inference on news headlines.
    """

    def __init__(self):

        #Starting message
        logger.info("FinBERT is loading...")
        
        #Initialising NLP model pipeline
        self.nlp = pipeline(task="sentiment-analysis", model="ProsusAI/finbert")
        

    def score(self, texts: list[str], batch_size: int = 16) -> list[dict]:
        """
        Runs sentiment analysis on a list of texts and returns a list of dictionaries
        containing the sentiment labels and scores.

        Args:
            texts: List of strings (headlines/descriptions) to analyze.
            batch_size: The batch size for Hugging Face inference.
        Returns:
            List of dicts, where each dict looks like:
            {'label': 'positive' | 'negative' | 'neutral', 'score': float}
        """

        #Guard clause: To check if the texts list is empty 
        if not texts:
            
            logger.error("Empty text list")
            return []
        
        else:

            try:

                #Running the FinBERT model and storing sentiment labels (NEGATIVE, NEUTRAL, POSITIVE) in form of dictionaries
                results = self.nlp(texts, batch_size=batch_size, truncation=True, max_length=512)

                #Returning results dictionary
                return results

            except Exception as e:

                #Logging error
                logger.error(e)

                #Returning a null score dictionary for all labels so that the program keeps running smoothly
                return [{'label': 'neutral', 'score':0.0} for _ in range(len(texts))]
       
    

