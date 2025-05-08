# rag_example
rag example with yugabyte

see blog at https://www.yugabyte.com/blog/using-yugabytedb-to-power-a-rag-pipeline/

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

<pre>
python3.9 -m venv aiblog
pip install llama-index
source aiblog/bin/activate
cd aiblog
pip install llama-index
pip install psycopg2
export OPENAI_API_KEY='your openAI key'

# in ./aiblog/rag_example/data I have a file about "paul_graham"
# you could put any textual data that in ./aiblog/data
# that you want to suppliment the LLM retrieval with
</pre>

I only needed llama-index and psycopg2 packages but you can install my full enviroment with

<pre>pip install -r requirements.txt</pre>

git clone https://github.com/kyle-hailey/rag_example.git
cd rag_example

edit insert.py and question.py and 
modify the connection_string for your database

<pre>connection_string = "postgresql://yugabyte:password@127.0.0.1:5433/yugabyte"</pre>


Insert embeddings in Yugabyte from ./data

<pre>python insert.py</pre>

query the LLM with context from the embeddings

<pre>python question.py</pre>


<pre>$ python insert.py
✅ Successfully connected to the database.

📄 Loading documents...
📦 Loaded 1 documents.

🔍 Vectorizing documents...
✅ Vectorization complete.

📥 4170 chars | "What I Worked On February 2021 Before" | [0.0041,
📥 4325 chars | "All that seemed left for philosophy were" |[0.0197,
📥 4193 chars | "Its brokenness did, as so often happens," |[0.0065,
📥 4339 chars | "If he even knew about the strange classe" [-0.0068,
📥 4291 chars | "The students and faculty in the painting" [-0.0073,
📥 4329 chars | "I wanted to go back to RISD, but I was n" |[0.0019,
📥 4261 chars | "But alas it was more like the Accademia" | [0.0065,
📥 4293 chars | "After I moved to New York I became her d" [-0.0001,
📥 4319 chars | "Now we felt like we were really onto som" [-0.0179,
📥 4258 chars | "In its time, the editor was one of the b" [-0.0091,
📥 4181 chars | "A company with just a handful of employe" |[0.0008,
📥 4244 chars | "I stuck it out for a few more months, th" |[0.0073,
📥 4292 chars | "But about halfway through the summer I r" |[0.0034,
📥 4456 chars | "One of the most conspicuous patterns I'v" [-0.0037,
📥 4454 chars | "Horrified at the prospect of having my i" |[0.0007,
📥 4235 chars | "We'd use the building I owned in Cambrid" |[0.0128,
📥 4128 chars | "It was originally meant to be a news agg" |[0.0031,
📥 4161 chars | "It had already eaten Arc, and was in the" |[0.0125,
📥 4381 chars | "Then in March 2015 I started working on" |[-0.0092,
📥 4352 chars | "I remember taking the boys to the coast" | [0.0182,
📥 4472 chars | "But when the software is an online store" [-0.0007,
📥 1805 chars | "[17] Another problem with HN was a bizar" | [0.005,
🎉 Done inserting all data.</pre>


<pre>% python question.py
Ask me a question (press Ctrl+C to quit):

❓ Your question: tell me about paul graham

🔍 Retrieved context snippets:
- 'Over the next several years  Paul Graham' (distance: 0.1471)
- 'The article is about Paul Graham\n\nWhat  ' (distance: 0.1513)
- 'Paul Graham certainly did. So at the end' (distance: 0.1523)
- 'They either lived long ago or were myste' (distance: 0.1530)
- 'But the most important thing  Paul Graha' (distance: 0.1583)
- 'You can do something similar on a map of' (distance: 0.1621)
- 'When  Paul Graham was dealing with some ' (distance: 0.1628)

💡 Answer:

Paul Graham is a writer, programmer, and entrepreneur. He has written numerous essays on various topics, some of which were reprinted as a book titled "Hackers & Painters". He has also worked on spam filters and has a passion for painting. He was known for hosting dinners for a group of friends every Thursday night, teaching him how to cook for groups. 

Before college, Graham mainly focused on writing and programming. He wrote short stories and tried programming on the IBM 1401. He later got a microcomputer and started programming more seriously, writing simple games and a word processor. In college, he initially planned to study philosophy but switched to AI. 

Graham also worked on a new dialect of Lisp, called Arc, and gave a talk at a Lisp conference about how they'd used Lisp at Viaweb. This talk gained significant attention online, leading him to realize the potential of online essays. 

In 2003, Graham met Jessica Livingston at a party. She was in charge of marketing at a Boston investment bank and later compiled a book of interviews with startup founders. In 2005, Graham and Livingston, along with Robert and Trevor, decided to start their own investment firm, which became Y Combinator. 

Graham also worked on several different projects, including the development of the programming language Arc and the creation of the online platform Hacker News. In 2012, he decided to hand over Y Combinator to Sam Altman and retire.</pre>

