# generator.py

from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

class LocalAnswerGenerator:
    def __init__(self, model_name="google/flan-t5-base"):
        print("Loading local model...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.generator = pipeline("text2text-generation", model=self.model, tokenizer=self.tokenizer)

    def generate_answer(self, question, context):
        """
        Generate an answer from context using the question.
        """
        prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
        response = self.generator(prompt, max_length=256, do_sample=False)[0]['generated_text']
        return response
