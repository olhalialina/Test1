Cocktail Advisor Chat

Cocktail Advisor Chat is a chat application that leverages FastAPI, FAISS, and LLM to implement a Retrieval-Augmented Generation (RAG) system for providing cocktail recommendations. Users can ask questions about cocktails and receive personalized answers, as well as share their favorite ingredients for future recommendations.

## Features

- **Knowledge Base:** Answers questions about cocktails, for example:
  - What are the 5 cocktails containing lemon?
  - What are the 5 non-alcoholic cocktails containing sugar?
  - What are my favorite ingredients?
- **Advisor:** Recommends cocktails, for example:
  - Recommend 5 cocktails that include my favorite ingredients.
  - Recommend a cocktail similar to "Hot Creamy Bush."
- **LLM Integration:** Utilizes LLMs (e.g., GPT-2 via Hugging Face Transformers) to generate responses.
- **Vector Database (FAISS):** Searches for similar cocktails and stores user data (favorite ingredients) for personalized recommendations.

  Requirements

- **Python 3.8** (It is recommended to use a virtual environment)
- Packages listed in [requirements.txt](requirements.txt):
  - fastapi
  - uvicorn
  - faiss-cpu (or faiss-gpu, if using a GPU)
  - pandas
  - numpy
  - sentence-transformers
  - transformers
  - torch

## Installation and Running

1. **Clone the repository:**

   ```bash
   git clone https://github.com/olhalialina/coctail_advisor_chat
   cd cocktail_advisor_chat

2. **Create a virtual environment (recommended):**

bash   py -3.8 -m venv venv

3 **Activate the virtual environment:**

Windows:
bash    venv\Scripts\activate
Linux/MacOS:
bash    source venv/bin/activate
4 **Install dependencies:**

bash    pip install -r requirements.txt
Place the CSV file containing cocktail data in the data/ directory (the file should be named finalcocktails.csv).

5. **Run the application:**

bash       py -3.8 -m uvicorn app.main:app --reload
The application will be available at http://127.0.0.1:8000.

6. **Additional Information**
API Endpoints:

GET / – Health check for the server.
GET /search – Cocktail search using the FAISS vector database.
POST /chat – Process user messages and generate responses using LLM.
GET /memory – Retrieve the stored favorite ingredients of the user.
Logging is implemented via the utils.py module.

