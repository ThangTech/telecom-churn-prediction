# Week 4 - Thang - Kiem chung mo hinh va danh gia cuoi

## Pham vi

Son da hoan thanh phan tich loi, bieu do va tao artifact danh gia Week 4. De tranh lap lai cong viec va tranh mo them vong lua chon sau khi test da duoc mo, phan cua Thang tap trung vao kiem chung doc lap cac quyet dinh da dong bang.

## Noi dung da lam

- Kiem tra candidate `B1_C10`, 13 feature, `class_weight=None` va seed 42 khop frozen config.
- Kiem tra ba threshold LOW, MEDIUM, HIGH khop giua config, bao cao validation, bao cao test va frontend.
- Kiem tra checksum cua raw data, split manifest, model va bao cao test.
- Kiem tra lai precision, recall va F1 tu TN/FP/FN/TP da cong bo.
- Sua ma nguon tai lap pipeline de `Status` duoc xu ly nhu categorical, dung voi pipeline Week 4 da luu.
- Khong doc lai nhan test, khong goi lai `predict_proba` tren test va khong thay doi model/threshold/metric.

## Ket qua

Chay:

```powershell
python scripts/verify_week4_thang.py
python -m unittest tests.test_thang_week4 -v
```

Ket qua mong doi: audit `PASS`; hai test cua Thang dat. Bao cao may doc duoc nam tai `reports/week4-thang-verification.json`.

Ket qua test da dong bang cua nhom van la 630 mau, AP 0.798105, PR_AUC 0.796582, ROC_AUC 0.949951, Brier 0.062798 va F1 0.728972 tai threshold MEDIUM 0.3431830803885034. Day la ket qua Son da danh gia mot lan; audit nay chi kiem tra artifact va phep tinh da cong bo.
