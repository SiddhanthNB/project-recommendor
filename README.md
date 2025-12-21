AI/ML Project Recommender
=========================
Live app: https://project-ideas-recommender.streamlit.app/

Generate small, buildable AI/ML project concepts with real data sources, view them in a Streamlit UI, and log batches to Google Sheets for later reference.

Overview
--------
- CoreNest-powered ideas: Calls the CoreNest `/completions` API with curated prompts to fetch 5 structured project suggestions (title, description, stack, steps, data source links).
- Streamlit UI: Minimal front-end to generate, browse, and refresh project batches. Provides a one-click handoff link to ChatGPT with the current idea prefilled.
- Ledger (optional): Batches can be appended to a Google Sheet for long-term storage/audit; the code is wired but currently disabled in the UI.

How it works
------------
1. User clicks "Generate ideas" -> Streamlit triggers a CoreNest completion using `utils/prompts/system_prompt.txt` and `utils/prompts/user_prompt.txt`.
2. The response is rendered in markdown via `utils/streamlit/templates/idea.md`, with stack/steps/data sources formatted for readability.
3. (Optional) The batch can be appended to a Google Sheet. The append step is queued after render to avoid blocking the UI; the actual call is currently commented in the UI but the helper code is ready.
4. "Generate more ideas" replaces the batch with a fresh set.

Key files
---------
- `utils/streamlit/gui.py`: Streamlit application (UI flow, idea rendering, and post-render sheet-append hook).
- `utils/helpers/corenest.py`: CoreNest client to call `/completions` with local prompts.
- `utils/helpers/sheets.py`: Google Sheets client utilities (header + append rows).
- `utils/streamlit/templates/idea.md`: Markdown template for rendering a single idea.
- `utils/prompts/system_prompt.txt`, `utils/prompts/user_prompt.txt`: Prompt content sent to CoreNest.
- `utils/migrations/mongo_to_sheets.py`: One-time migration helper to move legacy Mongo docs into Sheets.

Environment variables
---------------------
- `CORENEST_API_URL` (required): Base URL for CoreNest API.
- `CORENEST_SECRET_KEY` (required): Bearer token for CoreNest.
- `GOOGLE_SPREADSHEET_ID` (required): Target spreadsheet ID.
- `GOOGLE_SHEET_NAME` (optional, default `AI/ML Ideas`): Target sheet/tab name.
- `GOOGLE_SERVICE_ACCOUNT_JSON` (required): One-line JSON for the service account used to write to Sheets.
- Legacy Mongo vars (`MONGO_CLUSTER_URI`, `MONGO_DATABASE_NAME`, `MONGO_COLLECTION_NAME`) are optional and only used by the migration script.

Running locally
---------------
1. Install dependencies: `pip install -r requirements.txt` (or `uv sync`).
2. Set environment variables (see above).
3. Start the UI: `streamlit run main.py`.
4. (Optional) Migrate legacy Mongo docs to Sheets: `inv one_time_tasks.migrate-mongo-docs-into-gsheets`.

Notes
-----
- CoreNest is expected to return `{ "result": { "content": [...] } }`. If the envelope changes, update `utils/helpers/corenest.py`.
- The app is session-only for display; the ledger is append-only by design.
