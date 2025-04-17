# rag_example
rag example with yugabyte

see blog at https://www.kylehailey.com/post/rag-with-yugabyte


Create a Yugabyte database here: https://cloud.yugabyte.com/

using the last available version 2.25.1 and enabled the vector extention and created a table for the vector embeddings:

<pre>CREATE EXTENSION vector;

CREATE TABLE vectors (
    id           TEXT PRIMARY KEY,
    article_text TEXT,
    embedding    VECTOR(1536)
);

CREATE INDEX NONCONCURRENTLY ON vectors USING ybhnsw (embedding vector_cosine_ops);
</pre>

see: [Yugabyte Vector Docs](https://docs.yugabyte.com/preview/explore/ysql-language-features/pg-extensions/extension-pgvector/)

<pre><
python3.9 -m venv aiblog
pip install llama-index
source aiblog/bin/activate
cd aiblog
pip install llama-index
pip install psycopg2
OPENAI_API_KEY='your openAI key'

# in ./aiblog/data I have a file about "paul_graham"
# you could put any textual data that in ./aiblog/data
# that you want to suppliment the LLM retrieval with
</pre>

I omly needed llama-index and psycopg2 packages but you can install my full enviroment with

<pre>pip install -r requirements.txt</pre>

git clone https://github.com/kyle-hailey/rag_example.git
cd rag_example

Insert embeddings in Yugabyte from ./data

<pre>python insert.py</pre>

query the LLM with context from the embeddings

<pre>python question.py</pre>



