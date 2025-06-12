# FastAPI Image Upload to Supabase

A simple FastAPI app to upload images to Supabase Storage and log metadata in a Supabase table.

## Deploy

1. Push to GitHub
2. Connect GitHub repo to [Render.com](https://render.com)
3. Set `SUPER_BASE_URL`, `SUPER_BASE_API_KEY`, and `STORAGE_BUCKET` in environment variables
4. Set `MY_SQL_HOST`, `MY_SQL_USERNAME`, `MY_SQL_PASSWORD`, `MY_SQL_DATABASE` and `MY_SQL_PORT` in environment variables

## Test locally

```bash
uvicorn main:app --reload
```

## 🚀 Final Step: Deploy to Render

1. Push this to a new **GitHub repo**
2. Go to [https://render.com](https://render.com)
3. Click **"New Web Service"** → **"Deploy from GitHub"**
4. Select the repo
5. Set the following:
    - **Build command**: `pip install -r requirements.txt`
    - **Start command**: `uvicorn main:app --host=0.0.0.0 --port=10000`
6. Add **Environment Variables**:
    - `SUPER_BASE_URL`
    - `SUPER_BASE_API_KEY` (use service role)
    - `STORAGE_BUCKET` (default: `images`)
    - `MY_SQL_HOST`
    - `MY_SQL_USERNAME`
    - `MY_SQL_PASSWORD`
    - `MY_SQL_DATABASE`
    - `MY_SQL_PORT`

---






