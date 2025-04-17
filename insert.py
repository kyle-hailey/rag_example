from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.schema import Document

import openai
import psycopg2

connection_string = "postgresql://yugabyte:password@127.0.0.1:5433/yugabyte"

# Try to connect and give feedback
try:
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()
    print("✅ Successfully connected to the database.\n")
except Exception as e:
    print("❌ Failed to connect to the database.")
    print("Error:", e)
    exit(1)

# Load documents and create index
print("📄 Loading documents...")
documents = SimpleDirectoryReader("./data").load_data()
print(f"📦 Loaded {len(documents)} documents.\n")

print("🔍 Vectorizing documents...")
index = VectorStoreIndex.from_documents(documents)
print("✅ Vectorization complete.\n")

# Insert documents with clean feedback
for doc_id, doc in index.docstore.docs.items():
    embedding = index._embed_model.get_text_embedding(doc.text)
    embedding_str = "[" + ",".join(map(str, embedding)) + "]"

    insert_sql = """
        INSERT INTO vectors (id, article_text, embedding)
        VALUES (%s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
    """

    try:
        cursor.execute(insert_sql, (doc_id, doc.text, embedding_str))
        conn.commit()

        text_snippet = doc.text[:40].replace("\n", " ").strip()
        print(f"📥 {len(doc.text):4d} chars | \"{text_snippet}\" | { [round(v, 4) for v in embedding[:5]] }")
    except Exception as e:
        print(f"❌ Failed to insert row: {e}")

print("\n🎉 Done inserting all data.")

cursor.close()
conn.close()

