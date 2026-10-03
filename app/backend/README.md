# Backend API Week 5

API FastAPI nap pipeline `models/week4_final_candidate.joblib` va ba threshold trong `configs/week4_frozen_evaluation.json`. API khong huan luyen lai model.

## Cai dat va chay

Tu thu muc goc repo:

```powershell
python -m pip install -r requirements.txt -r app/backend/requirements.txt
python -m uvicorn app.backend.main:app --host 127.0.0.1 --port 8000
```

Kiem tra health tai `http://127.0.0.1:8000/api/health` va OpenAPI tai `http://127.0.0.1:8000/docs`.

## Ket noi frontend

Tao `web/.env.local`:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_USE_MOCK_API=false
```

Sau do chay frontend bang `npm run dev` trong thu muc `web`.

Co the doi danh sach origin bang bien moi truong `CHURN_ALLOWED_ORIGINS`, phan tach boi dau phay. Mac dinh chi cho phep Vite local tren `localhost:5173` va `127.0.0.1:5173`.
