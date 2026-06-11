# Project: AI-Enhanced Chrome Bookmark Manager (MCP)

## 📋 Executive Summary
A three-phased implementation of a personal knowledge management system that transforms static Chrome bookmarks into a semantically searchable, AI-organized database. This project leverages the **Model Context Protocol (MCP)** to bridge the gap between local browser data and Large Language Models (LLMs).

---

## 🏗️ Architecture & Plan

### Phase 1: The "Audit & Clean" (The MVP)
**Goal:** Create a human-readable map of current "bookmark debt" and enable AI-driven reorganization.
* **Method:** Build a standalone Python MCP server that interacts directly with the local Chrome `Bookmarks` JSON file.
* **Key Mechanic:** Handle the "File Locking" challenge by checking for active Chrome processes and bypassing the internal MD5 checksum by deleting the `checksum` key and `.bak` files during writes.
* **Outcome:** The LLM generates a Master Markdown file representing the folder structure, allowing the user to "reorganize via text."

### Phase 2: Semantic Memory (Vector Search)
**Goal:** Solve the "findability" problem using content-based search rather than just title matching.
* **Tech Stack:** * **Vector DB:** ChromaDB (Local-first storage).
    * **Scraper:** `Crawl4AI` or `BeautifulSoup` to extract page text.
    * **Embeddings:** `sentence-transformers` (Local) or OpenAI/Google (API).
* **Logic:** The MCP server crawls bookmarked URLs in the background, summarizes them, and stores the vectors.
* **Outcome:** Users can query the LLM: *"Find that React tool I saved last year for state management,"* even if "React" isn't in the title.

### Phase 3: The "Live Watcher" (Chrome Extension)
**Goal:** Automation and real-time synchronization.
* **Method:** A lightweight Chrome Extension acting as the "Hands" for the Python "Brain."
* **Listeners:** Uses `chrome.bookmarks.onCreated` to trigger immediate indexing of new bookmarks.
* **Omnibox Integration:** Register a keyword (e.g., `@find`) to surface semantic search results directly in the browser address bar.

---

## 🛠️ Implementation Strategy

### 1. The "Day 1" POC Checklist
- [ ] **Environment:** Set up a Python environment with the `mcp` SDK.
- [ ] **File Access:** Write a script to locate the Chrome Profile path (Windows/Mac) and parse the JSON.
- [ ] **CRUD Operations:** Implement a "Write" tool that kills the Chrome process, modifies the JSON, and clears the checksum.
- [ ] **Verification:** Successfully add one bookmark to the "Bookmark Bar" via an LLM command.

### 2. Distribution Plan (The "2-Week" Polish)
* **Packaging:** Use `PyInstaller` to create an executable so users don't need a Python environment.
* **Publishing:** * **GitHub/Smithery.ai:** To make the MCP server discoverable by the AI community.
    * **PyPI:** For developer-level installation (`pip install chrome-bookmark-mcp`).
* **Config:** Move hardcoded paths to a `config.yaml` to support different Chrome Profiles and Operating Systems.

---

## ⚠️ Technical Notes & Constraints
* **Chrome Sync:** Be aware that manual file manipulation may trigger sync conflicts if Chrome is active on other devices; the "Write" operations are best handled locally and then pushed to the cloud by Chrome itself upon restart.
* **Privacy:** Keep the architecture "Local-First." By using local vector databases (ChromaDB), user browsing data never leaves their machine unless sent to an LLM for summarization.