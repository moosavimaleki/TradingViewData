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
| 📄 [2026-07-24T13-59-45Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-24T13-59-45Z.md) | ✅ `success` | `2026-07-24` `17:29:45` |
| 📄 [2026-07-24T08-35-39Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-24T08-35-39Z.md) | ✅ `success` | `2026-07-24` `12:05:39` |
| 📄 [2026-07-24T03-25-43Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-24T03-25-43Z.md) | ✅ `success` | `2026-07-24` `06:55:43` |
| 📄 [2026-07-23T14-20-54Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-23T14-20-54Z.md) | ✅ `success` | `2026-07-23` `17:50:54` |
| 📄 [2026-07-23T08-39-48Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-23T08-39-48Z.md) | ✅ `success` | `2026-07-23` `12:09:48` |
| 📄 [2026-07-23T03-30-46Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-23T03-30-46Z.md) | ✅ `success` | `2026-07-23` `07:00:46` |
| 📄 [2026-07-22T19-35-47Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-22T19-35-47Z.md) | ✅ `success` | `2026-07-22` `23:05:47` |
| 📄 [2026-07-22T14-11-25Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-22T14-11-25Z.md) | ✅ `success` | `2026-07-22` `17:41:25` |
| 📄 [2026-07-22T08-38-05Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-22T08-38-05Z.md) | ❌ `failed` | `2026-07-22` `12:08:05` |
| 📄 [2026-07-22T03-24-42Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-22T03-24-42Z.md) | ✅ `success` | `2026-07-22` `06:54:42` |

<!-- RUN_TABLE_END -->
