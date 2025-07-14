# RecipEase

## 📝 Project Summary

**RecipEase** is a full-stack application that helps users generate and categorize recipes using intelligent agents. Users can input preferences or constraints (like dietary needs), and the system will return tailored recipes along with explanations and saved queries. Those saved queries will run on a daily basis, making the user able to find the best recipes over time.

---

## ⚙️ Setup

### Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the FastAPI server:
   ```bash
   uvicorn api.main:app
   ```

### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

---

## 🚀 Usage

- Visit the frontend (e.g., `http://localhost:8080`) to interact with the app.
- Submit a query describing your food preferences and dietary needs ("Create New Query" button at the top).
- Follow background job status to see your query status. 
- Access your queries and see their relevant content (new content for each query gets generated daily by a cron job).
- See a summary of all recipes ever created by different queries.
---

## 💡 Examples

- “I want a pasta recipe that’s gluten-free.”
- “Show me vegetarian breakfast ideas that use oats.”

---

## 📁 Folder Structure

### Backend

```
backend/
├── agent_flow/
│   ├── agents/
│   │   ├── categorize_agent.py
│   │   ├── db_saver.py
│   │   └── recipe_modifier_agent.py
│   ├── custom_types/
│   │   └── agent_types.py
│   ├── helpers/
│   │   └── db_utils.py
│   ├── agent_flow.py
│   └── setup.py
├── api/
│   ├── helpers/
│   │   ├── exports.py
│   │   └── utils.py
│   ├── routers/
│   │   ├── queries.py
│   │   └── recipes.py
│   └── main.py
├── shared/
│   ├── db.py
│   └── models.py
├── requirements.txt
```

### Frontend

```
frontend/
├── public/
├── src/
│   ├── api/
│   │   ├── api-functions.ts
│   │   └── endpoints.ts
│   ├── atoms/
│   │   └── bgJobAtom.ts
│   ├── components/
│   │   ├── context/
│   │   │   └── global-atom-store.ts
│   │   ├── Queries/
│   │   │   ├── CreateNewQueryModal.tsx
│   │   │   ├── QueriesPage.tsx
│   │   │   ├── QueryCard.tsx
│   │   │   └── QueryPage.tsx
│   │   ├── Recipe/
│   │   │   ├── RecipeCard.tsx
│   │   │   ├── RecipeList.tsx
│   │   │   ├── RecipeModal.tsx
│   │   │   └── RecipesPage.tsx
│   │   └── shared/
│   │       ├── InfoTag.tsx
│   │       └── TextBox.tsx
|   |   |__AboutPage.tsx
|   │   ├── BgJobPanel.tsx
|   │   ├── ErrorFallback.tsx
|   │   ├── NotFoundPage.tsx
│   ├── constants/
│   │   └── routes.tsx
│   ├── context/
│   │   └── UserContext.tsx
│   ├── types/
│   │   ├── BackendTypes.ts
│   │   └── TableTypes.tsx
│   ├── utils/
│   │   └── dates.ts
│   ├── App.css
│   └── main.tsx
├── package.json
├── tsconfig.json
└── vite.config.ts
|__ biome.json
|__ .. other general react files
```

---
