# main.py

from retriever import load_chroma_retriever
from generator import LocalAnswerGenerator

def rag_pipeline():
    # Step 1: Load retriever from Chroma DB
    retriever = load_chroma_retriever()

    # Step 2: Load local LLM-based answer generator
    generator = LocalAnswerGenerator()

    # Step 3: Ask user a question
    print("\n💬 Ask a question about your PDFs:")
    question = input(">> ")

    # Step 4: Retrieve relevant documents
    docs = retriever.get_relevant_documents(question)
    if not docs:
        print("⚠️ No relevant documents found.")
        return

    # Step 5: Create a context from top documents
    context = "\n".join([doc.page_content for doc in docs[:4]])

    # Step 6: Generate answer using local LLM
    print("\n🧠 Generating answer...")
    answer = generator.generate_answer(question, context)

    # Step 7: Show the answer
    print("\n📌 Answer:")
    print(answer)

if __name__ == "__main__":
    rag_pipeline()
