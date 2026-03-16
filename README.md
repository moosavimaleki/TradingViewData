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
| 📄 [2026-03-16T13-43-23Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-16T13-43-23Z.md) | ❌ `failed` | `2026-03-16` `17:13:23` |
| 📄 [2026-03-16T07-41-46Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-16T07-41-46Z.md) | ✅ `success` | `2026-03-16` `11:11:46` |
| 📄 [2026-03-16T03-20-58Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-16T03-20-58Z.md) | ✅ `success` | `2026-03-16` `06:50:58` |
| 📄 [2026-03-15T18-51-48Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-15T18-51-48Z.md) | ✅ `success` | `2026-03-15` `22:21:48` |
| 📄 [2026-03-15T13-09-15Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-15T13-09-15Z.md) | ✅ `success` | `2026-03-15` `16:39:15` |
| 📄 [2026-03-15T07-08-23Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-15T07-08-23Z.md) | ✅ `success` | `2026-03-15` `10:38:23` |
| 📄 [2026-03-15T03-18-49Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-15T03-18-49Z.md) | ✅ `success` | `2026-03-15` `06:48:49` |
| 📄 [2026-03-14T18-50-49Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-14T18-50-49Z.md) | ✅ `success` | `2026-03-14` `22:20:49` |
| 📄 [2026-03-14T13-08-02Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-14T13-08-02Z.md) | ✅ `success` | `2026-03-14` `16:38:02` |
| 📄 [2026-03-14T06-59-16Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-14T06-59-16Z.md) | ✅ `success` | `2026-03-14` `10:29:16` |

<!-- RUN_TABLE_END -->
