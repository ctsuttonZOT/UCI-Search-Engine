# UCI Search Engine
A Python-based Search Engine project to search UCI web pages.

This README will show you how to set it up and run it locally.

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/ctsuttonZOT/UCI-Search-Engine.git
cd UCI-Search-Engine
```

### 2. Backend Setup (Flask)
Navigate to the backend folder
```bash
cd app/server
```

Install dependencies from requirements.txt
```bash
pip install -r requirements.txt
```

Run the Flask server
```bash
python -m flask --app server run
```

### 3. Frontend Setup (React/Next.js)
Open a new terminal and navigate to the frontend

```bash
cd app/client/cs-121
```

Install dependencies
```bash
npm install
```

Start the development server
```bash
npm run dev
```
The frontend will be available at http://localhost:3000

### 4. Usage
Type a query and submit. Using a Boolean AND keyword search and TF-IDF-inspired ranking, you will be served the top 5 results from a collection of 60k+ UCI web pages.

<img width="1918" height="910" alt="image" src="https://github.com/user-attachments/assets/fbc57ea4-4687-48b3-b85c-a8a8955517d7" />


*Keep in mind, these pages were crawled a couple of years ago, so some of them may no longer exist.*
