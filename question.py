import psycopg2
import openai
import os
from llama_index.embeddings.openai import OpenAIEmbedding

# --- Setup ---
openai.api_key = os.getenv("OPENAI_API_KEY")
embed_model = OpenAIEmbedding(model="text-embedding-ada-002")
client = openai.OpenAI()
connection_string = "postgresql://yugabyte:password@127.0.0.1:5433/yugabyte"
def ask_question(question, top_k=7):
    # Connect to DB
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    # Get embedding of question
    query_embedding = embed_model.get_query_embedding(question)
    embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"

    # Vector search
    search_sql = """
        SELECT id, article_text, embedding <=> %s AS distance
        FROM vectors
        ORDER BY embedding <=> %s
        LIMIT %s;
    """
    cursor.execute(search_sql, (embedding_str, embedding_str, top_k))
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    if not results:
        return "No matching documents found."

    # Print the first 40 characters of each retrieved chunk
    print("\n🔍 Retrieved context snippets:")
    for _, text, distance in results:
        print(f"- {text[:40]!r} (distance: {distance:.4f})")

    # Build context
    context = "\n\n".join([f"{text}" for (_, text, _) in results])

    # Ask GPT
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions using the provided context."},
            {"role": "user", "content": f"Context:\n{context}"},
            {"role": "user", "content": f"Question: {question}"}
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()

# --- Interactive Loop ---
if __name__ == "__main__":
    try:
        print("Ask me a question (press Ctrl+C to quit):\n")
        while True:
            question = input("❓ Your question: ").strip()
            if not question:
                continue
            answer = ask_question(question)
            print("\n💡 Answer:\n" + answer + "\n")
    except KeyboardInterrupt:
        print("\nGoodbye! 👋")
