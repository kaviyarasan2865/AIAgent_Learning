# main.py

import google.generativeai as genai
from retriever import DocumentRetriever
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiGenerator:
    def __init__(self):
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_answer(self, question: str, context: str) -> str:
        prompt = f"""You are a helpful AI assistant. Using only the information from the provided context, 
answer the question. If the context doesn't contain relevant information, say so.

Context: {context}

Question: {question}

Provide a clear, focused answer based solely on the context provided."""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"

def main():
    try:
        # Initialize components
        retriever = DocumentRetriever()
        generator = GeminiGenerator()

        while True:
            print("\n💬 Ask a question about your PDFs:")
            question = input(">> ")
            
            if question.lower() in ['quit', 'exit', 'q']:
                break

            # Get relevant documents
            docs = retriever.get_relevant_documents(question)
            if not docs:
                print("⚠️ No relevant documents found. Make sure documents are properly indexed.")
                continue

            # Create context from documents
            context = "\n".join([f"Document {i+1}: {doc.page_content}" 
                               for i, doc in enumerate(docs)])

            # Generate answer
            print("\n🧠 Generating answer...")
            answer = generator.generate_answer(question, context)
            
            print("\n📌 Answer:")
            print(answer)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
