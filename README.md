# TradingViewData

این پروژه برای جمع‌آوری و به‌روزرسانی دیتای بازار از TradingView ساخته شده است.

## ✨ نمای کلی
- منبع داده: `TradingView`
- خروجی: فایل‌های سالانه `Parquet`
- هدف: نگهداری دیتای سبک، قابل‌همگام‌سازی و قابل‌به‌روزرسانی

## 📥 دریافت داده

- Google Drive (دیتای اصلی):
  - https://drive.google.com/drive/folders/189HIU2eouf3Ftzil_0Nmm1fk1yAgs61B?usp=sharing

## 🗂️ ساختار ذخیره‌سازی

- مسیر فایل‌ها به‌صورت سالانه ذخیره می‌شود:
  - `data/tradingview/{BROKER}/{TIMEFRAME}/{SYMBOL}/{RUN_YEAR}.parquet`

## ⏱️ زمان‌بندی اجرا

- هر ۳ ساعت: اجرای `minor` (فقط تایم‌فریم‌های رنج: `10R`, `100R`, `1000R`)
- هر ۶ ساعت: اجرای `major` (همه تایم‌فریم‌ها + گزارش کامل)

<!-- RUN_TABLE_START -->
## 🕒 آخرین اجراها

| گزارش | وضعیت | زمان اجرا (تهران) |
|---|---|---|
| 📄 [2026-10-01T22-33-45Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-01T22-33-45Z.md) | ✅ `success` | `2026-10-02` `02:03:45` |
| 📄 [2026-10-01T12-55-24Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-01T12-55-24Z.md) | ✅ `success` | `2026-10-01` `16:25:24` |
| 📄 [2026-10-01T05-25-44Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-01T05-25-44Z.md) | ✅ `success` | `2026-10-01` `08:55:44` |
| 📄 [2026-09-30T22-06-43Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-30T22-06-43Z.md) | ✅ `success` | `2026-10-01` `01:36:43` |
| 📄 [2026-09-30T12-20-19Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-30T12-20-19Z.md) | ✅ `success` | `2026-09-30` `15:50:19` |
| 📄 [2026-09-30T05-10-54Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-30T05-10-54Z.md) | ✅ `success` | `2026-09-30` `08:40:54` |
| 📄 [2026-09-29T22-06-59Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-29T22-06-59Z.md) | ✅ `success` | `2026-09-30` `01:36:59` |
| 📄 [2026-09-29T12-34-48Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-29T12-34-48Z.md) | ✅ `success` | `2026-09-29` `16:04:48` |
| 📄 [2026-09-29T05-22-54Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-29T05-22-54Z.md) | ✅ `success` | `2026-09-29` `08:52:54` |
| 📄 [2026-09-28T23-08-26Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-28T23-08-26Z.md) | ✅ `success` | `2026-09-29` `02:38:26` |

<!-- RUN_TABLE_END -->
