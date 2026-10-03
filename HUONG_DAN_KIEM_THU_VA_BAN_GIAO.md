# Huong dan kiem thu va ban giao do an churn

Tai lieu nay dung de Thang cai dat, kiem tra va demo dung pham vi trong `Ke_hoach_6_tuan_do_an_churn.docx`. Quy trinh khong tuning lai model va khong danh gia lai test.

## 1 Pham vi theo file ke hoach

| Tuan | Phan cua Thang | Minh chung trong repo |
|---|---|---|
| 4 | Chot model va threshold bang validation; chap nhan danh gia test cuoi | `configs/week4_frozen_evaluation.json`, `reports/week4_test_final.csv`, `scripts/verify_week4_thang.py` |
| 5 | API nap pipeline, validation input, ket noi frontend | `app/backend/`, `tests/test_thang_week5_api.py`, `docs/frontend-api-contract.md` |
| 6 | Moi truong sach, tai lap, kiem tra ma nguon va ban giao | `requirements-lock.txt`, `scripts/verify_release.py`, `scripts/test_release.ps1` |

Son phu trach phan tich loi, bieu do, frontend va bao cao. Khong tao lai cac phan nay trong nhanh Thang.

## 2 Tao moi truong sach tren Windows

Yeu cau: Python 3.11.9, Node.js 20 tro len va Git. Khong dung thu muc `.venv` chep tu may khac.

```powershell
cd D:\telecom-churn-prediction
py -3.11 -m venv .venv-release
.\.venv-release\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-lock.txt
cd web
npx --yes npm@10.9.4 ci
cd ..
```

Neu `py -3.11` khong ton tai, cai Python 3.11.9 truoc khi tiep tuc. Model duoc tao bang scikit-learn 1.9.1; khong nen demo voi version khac vi joblib se canh bao khong tuong thich.

## 3 Kiem tra tu dong chuan

```powershell
.\.venv-release\Scripts\Activate.ps1
.\scripts\test_release.ps1
```

Ket qua dat:

- Release verification: `status` la `PASS`, tat ca `checks` la `true`.
- Python: tat ca test `OK`, khong co `skipped`.
- Frontend: lint khong co loi; 6 test files va 13 test cases dat; Vite build thanh cong.
- Khong co `InconsistentVersionWarning` khi nap model.

## 4 Chay web demo tu dau den cuoi

Terminal 1:

```powershell
.\.venv-release\Scripts\Activate.ps1
python -m uvicorn app.backend.main:app --host 127.0.0.1 --port 8000
```

Terminal 2:

```powershell
cd web
Copy-Item .env.example .env.local
npm run dev -- --host 127.0.0.1
```

Mo `http://127.0.0.1:5173/predict`, nhap fixture minh hoa:

| Feature | Gia tri |
|---|---:|
| Call Failure | 1 |
| Complains | 0 |
| Subscription Length | 24 |
| Charge Amount | 2 |
| Seconds of Use | 1000 |
| Frequency of use | 80 |
| Frequency of SMS | 12 |
| Distinct Called Numbers | 20 |
| Age Group | 3 |
| Tariff Plan | 1 |
| Status | 1 |
| Age | 35 |
| Customer Value | 42.75 |

Chon MEDIUM va bam du doan. Ket qua dat khi:

- Trang khong hien nhan `DU LIEU MO PHONG`.
- Threshold la `0.343183` va probability nam trong 0 den 100 phan tram.
- Ket qua classification khop phep so sanh probability voi threshold.
- Terminal backend ghi `POST /api/churn-score` voi HTTP 200.

Gia tri probability cua fixture nay la smoke test, khong phai metric danh gia va khong phai du lieu khach hang that.

## 5 Doi chieu ket qua Week 4

Khong chay lai tuning hay chon threshold. Chay:

```powershell
python scripts/verify_week4_thang.py
```

Ket qua chuan da dong bang:

| Chi so test | Gia tri |
|---|---:|
| So mau | 630 |
| AP | 0.798105 |
| PR AUC | 0.796582 |
| ROC AUC | 0.949951 |
| Brier | 0.062798 |
| Precision | 0.678261 |
| Recall | 0.787879 |
| F1 | 0.728972 |
| TN FP FN TP | 494 37 21 78 |

Threshold primary MEDIUM la `0.3431830803885034`, duoc chon tu validation. Script chi kiem tra artifact va phep tinh da luu; khong doc lai nhan test.

## 6 Test loi dau vao API

Trong OpenAPI `http://127.0.0.1:8000/docs`, thu bo mot feature, them `Churn`, gui Age am hoac Age Group bang 6. Ket qua dung la HTTP 422 voi `code` bang `INVALID_FEATURE_VALUE` hoac `INVALID_REQUEST`.

API chi nhan dung 13 feature; khong nhan `Churn`, `row_id`, ten, so dien thoai hoac dia chi.

## 7 Checklist truoc khi ban giao

- Git working tree sach va ba commit Week 4, 5, 6 tach rieng.
- `reports/week4-thang-verification.json` va `reports/week6-thang-release-verification.json` deu PASS.
- API va frontend chay tren hai terminal; mock tat.
- Demo bang fixture minh hoa, khong lay dong trong train, validation hoac test.
- Khong sua model/threshold sau khi xem ket qua test.
- Bao cao cua Son trich dung metric va gioi han trong model card.
- Ca Thang va Son deu giai thich duoc 9 thang quan sat, 3 thang du doan, AP khac PR AUC, threshold theo cong suat va gioi han du lieu.
