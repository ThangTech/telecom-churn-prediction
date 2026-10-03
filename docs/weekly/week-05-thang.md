# Week 5 - Thang - Backend API va tich hop web

## Pham vi

Trien khai backend FastAPI theo contract frontend cua Son. Backend chi nap pipeline Week 4 da dong bang, khong huan luyen lai va khong truy cap tap test.

## Noi dung da lam

- Endpoint `GET /api/health` xac nhan model da nap va so feature.
- Endpoint `POST /api/churn-score` nhan object `features` long va `capacity_mode` LOW, MEDIUM hoac HIGH.
- Giu nguyen ten 13 cot, bao gom cac ten co hai dau cach.
- Tu choi cot thieu/thua, boolean, chuoi, NaN/vo cuc, so am, so le cho bien integer va category ngoai mien.
- Doc ba threshold tu frozen config; tra probability, predicted_churn, priority_group, model_version va request_id.
- CORS mac dinh chi cho frontend Vite local; co the cau hinh bang `CHURN_ALLOWED_ORIGINS`.
- Cap nhat API contract va cau hinh frontend mau de goi API that.

## Kiem thu

```powershell
python -m unittest tests.test_thang_week5_api -v
cd web
npm run lint
npm run test
npm run build
```

Test API bao phu health, ba capacity mode, schema 13 feature, du lieu sai, response contract va CORS. Fixture la du lieu minh hoa tu API contract, khong phai ban ghi test.
