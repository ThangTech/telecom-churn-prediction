# Week 6 - Thang - Tai lap va ban giao

## Pham vi

Ra soat huong dan cai dat, khoa moi truong dung voi model Week 4, chay smoke test inference/API va toan bo kiem thu. Khong mo lai vong tuning va khong danh gia lai test.

## Noi dung da lam

- Them `requirements-lock.txt` voi Python package dung voi moi truong tao artifact Week 4.
- Them `scripts/verify_release.py` de kiem tra version, Week 4 audit, model load, OpenAPI va mot request minh hoa.
- Them `scripts/test_release.ps1` de chay release smoke test, toan bo Python test, frontend lint/test/build.
- Cap nhat README va viet huong dan ban giao theo ke hoach 6 tuan.
- Xac nhan fixture smoke test khong lay tu tap test va script khong doc nhan test.

## Tieu chi dat

- `python scripts/verify_release.py` in `status: PASS`.
- Toan bo Python test dat, khong co test bi bo qua trong moi truong release.
- Frontend lint PASS, 6 file test voi 13 test case PASS va production build PASS.
- API health tra `feature_count=13`; E2E dung API that, khong co nhan `DU LIEU MO PHONG`.

Chi tiet lenh va cach doc ket qua nam trong `HUONG_DAN_KIEM_THU_VA_BAN_GIAO.md`.
