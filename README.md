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
| 📄 [2026-07-21T14-08-21Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-21T14-08-21Z.md) | ✅ `success` | `2026-07-21` `17:38:21` |
| 📄 [2026-07-21T08-38-51Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-21T08-38-51Z.md) | ✅ `success` | `2026-07-21` `12:08:51` |
| 📄 [2026-07-21T03-26-09Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-21T03-26-09Z.md) | ✅ `success` | `2026-07-21` `06:56:09` |
| 📄 [2026-07-20T19-50-02Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-20T19-50-02Z.md) | ✅ `success` | `2026-07-20` `23:20:02` |
| 📄 [2026-07-20T14-22-26Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-20T14-22-26Z.md) | ✅ `success` | `2026-07-20` `17:52:26` |
| 📄 [2026-07-20T09-27-38Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-20T09-27-38Z.md) | ✅ `success` | `2026-07-20` `12:57:38` |
| 📄 [2026-07-20T03-46-53Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-20T03-46-53Z.md) | ✅ `success` | `2026-07-20` `07:16:53` |
| 📄 [2026-07-19T19-15-09Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-19T19-15-09Z.md) | ✅ `success` | `2026-07-19` `22:45:09` |
| 📄 [2026-07-19T13-39-00Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-19T13-39-00Z.md) | ✅ `success` | `2026-07-19` `17:09:00` |
| 📄 [2026-07-19T08-28-06Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-19T08-28-06Z.md) | ✅ `success` | `2026-07-19` `11:58:06` |

<!-- RUN_TABLE_END -->
