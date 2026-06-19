# RAG System Testing Guide

## Overview
You now have a complete RAG (Retrieval-Augmented Generation) system! Here's how to test it.

---

## Test Scripts Available

### 1. **Full Pipeline Test** (test_query.py)
Tests the complete flow: Load → Chunk → Embed → Store → Search

```bash
python3 test_query.py
```

**What it does:**
- ✅ Loads 57 documents from your Google Drive
- ✅ Creates 314 chunks
- ✅ Embeds 10 chunks (limited for testing)
- ✅ Stores in Qdrant database
- ✅ Tests 3 example queries
- ⏱️ Takes ~30-60 seconds

**Output:**
```
Documents loaded: 57
Chunks created: 314
Chunks embedded: 10
Results for 3 test queries with similarity scores
```

---

### 2. **Interactive Search** (interactive_search.py)
Test with YOUR OWN queries interactively

```bash
python3 interactive_search.py
```

**What it does:**
- 📌 Enter any query you want
- 🔍 Gets top 5 most relevant results
- 📄 Shows similarity score for each result
- 🔄 Keep searching until you type "exit"

**Example Usage:**
```
📌 Enter your query: What about travel in Rome?

✅ Found 5 results:

RESULT 1 ✅
Similarity: 0.8234
File: travel reddit data
Type: google_sheet
Content: 4/10/2026 1:37:29 | solotravel | Kindly help me review this one day solo female traveller itinerary in Rome | ...
```

**Advanced: Get more results**
```
📌 Enter your query: What about fashion? | 10

# Returns top 10 results instead of 5
```

---

## How to Use

### First Time Setup
```bash
# 1. Run the full pipeline test
python3 test_query.py

# This loads everything and creates the vector database
```

### Then: Test Your Own Queries
```bash
# 2. Use interactive search
python3 interactive_search.py

# Keep running and test different queries
```

---

## Example Queries to Try

Based on your data (travel, fashion, reddit posts):

1. **General Questions:**
   - "What is the main topic?"
   - "Summarize the documents"
   - "What are the key points?"

2. **Travel Questions:**
   - "Tell me about Rome"
   - "How do I plan a trip to India?"
   - "What is backpacking?"
   - "Solo travel tips"

3. **Fashion Questions:**
   - "How to optimize ecommerce?"
   - "What about search functionality?"
   - "Tell me about conversion optimization"

4. **Specific Questions:**
   - "What is the Green Building project?"
   - "How does predictive search work?"
   - "Describe the homepage optimization"

---

## Understanding Results

Each result shows:

```
RESULT 1 ✅
Similarity: 0.8234          ← How similar to your query (0-1)
File: Fashion Commerce      ← Which document it came from
Type: google_sheet          ← Type of document
Content: [preview...]       ← First 500 characters
```

### Similarity Score Interpretation:
- **✅ 0.70 - 1.00** = Excellent match
- **⚠️ 0.50 - 0.70** = Good match
- **❌ 0.00 - 0.50** = Poor match

---

## Next Steps

### If You Want More Data:
Modify `test_query.py` line 58:
```python
chunks_to_embed = chunks[:10]  # Change 10 to something else
```

Example:
```python
chunks_to_embed = chunks[:50]   # Embed first 50 chunks
chunks_to_embed = chunks        # Embed ALL chunks (takes longer)
```

### If You Want Better Quality:
Use all 314 chunks instead of just 10:
```python
# In test_query.py, change:
chunks_to_embed = chunks[:10]   # Limited
# To:
chunks_to_embed = chunks        # All chunks
```

**⚠️ Warning:** This will make many API calls (314 × Gemini API) and take ~10 minutes

### If You Want to Save Money:
Use local embeddings instead of Gemini API:

```bash
pip3 install sentence-transformers
```

Then modify `embedder.py` to use local model (I can help with this!)

---

## Troubleshooting

### "Collection already exists"
```
gyaan already exists
```
This is fine! The database was created from a previous run.

### "No results found"
- Your query might be too specific
- Try simpler queries like "documents" or "information"
- Run with more chunks: `chunks_to_embed = chunks` (instead of `chunks[:10]`)

### "ModuleNotFoundError: No module named..."
Install missing dependencies:
```bash
pip3 install python-dotenv qdrant-client google-genai langchain-text-splitters
```

### Slow performance
- First run is slow (downloading models)
- Qdrant search is usually fast (<1 second)
- Embedding is slow (API calls) - this is normal!

---

## Project Structure

```
gyaan/
├── document_loader.py      ← Loads from Google Drive
├── chunker.py              ← Splits text into chunks
├── embedder.py             ← Converts to vectors (Gemini)
├── qdrant_manager.py       ← Stores and searches vectors
├── test_query.py           ← Full pipeline test ⭐
├── interactive_search.py   ← Interactive query tester ⭐
├── qdrant_data/            ← Vector database (created automatically)
└── ...
```

---

## Complete Flow

```
1. test_query.py runs:
   ↓
2. Loads 57 docs from Google Drive
   ↓
3. Creates 314 chunks
   ↓
4. Embeds first 10 chunks with Gemini API
   ↓
5. Stores vectors in Qdrant (./qdrant_data/)
   ↓
6. Tests 3 queries and shows results
   ↓
7. You can now use interactive_search.py

interactive_search.py:
   ↓
8. Takes your query
   ↓
9. Converts to vector using Gemini API
   ↓
10. Searches Qdrant for similar vectors
   ↓
11. Shows top 5 most relevant chunks
```

---

## Tips & Tricks

**Get more results:**
```
📌 Enter your query: travel | 10
```
(Returns top 10 instead of 5)

**Try specific queries:**
- Use keywords from your documents
- Example: "Rome" works better than "Where should I go?"

**Look at similarity scores:**
- Helps you understand what worked
- Low scores (0.5-0.6) = Your query doesn't match well

**Check which file matched:**
- Shows which Google Doc/Sheet/Slide gave the result
- Helps you find the original source

---

## What's Next?

1. ✅ **Complete:** Load documents ✓
2. ✅ **Complete:** Chunk documents ✓
3. ✅ **Complete:** Embed with Gemini ✓
4. ✅ **Complete:** Store in Qdrant ✓
5. ✅ **Complete:** Search with similarity ✓
6. 🔄 **Optional:** Add LLM to generate answers (ChatGPT, Claude, etc.)

---

## Questions?

- Check the code comments in each file
- Read the complete documentation above
- Look at the output messages - they explain what's happening!

Happy searching! 🚀
