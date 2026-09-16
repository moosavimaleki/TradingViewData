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
| 📄 [2026-09-16T16-37-59Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-16T16-37-59Z.md) | ✅ `success` | `2026-09-16` `20:07:59` |
| 📄 [2026-09-16T11-17-44Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-16T11-17-44Z.md) | ✅ `success` | `2026-09-16` `14:47:44` |
| 📄 [2026-09-16T04-27-20Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-16T04-27-20Z.md) | ✅ `success` | `2026-09-16` `07:57:20` |
| 📄 [2026-09-15T21-08-31Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-15T21-08-31Z.md) | ✅ `success` | `2026-09-16` `00:38:31` |
| 📄 [2026-09-15T16-45-02Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-15T16-45-02Z.md) | ✅ `success` | `2026-09-15` `20:15:02` |
| 📄 [2026-09-15T11-31-37Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-15T11-31-37Z.md) | ❌ `failed` | `2026-09-15` `15:01:37` |
| 📄 [2026-09-15T04-31-37Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-15T04-31-37Z.md) | ✅ `success` | `2026-09-15` `08:01:37` |
| 📄 [2026-09-14T21-42-45Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-14T21-42-45Z.md) | ✅ `success` | `2026-09-15` `01:12:45` |
| 📄 [2026-09-14T12-27-33Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-14T12-27-33Z.md) | ✅ `success` | `2026-09-14` `15:57:33` |
| 📄 [2026-09-14T04-31-41Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-14T04-31-41Z.md) | ✅ `success` | `2026-09-14` `08:01:41` |

<!-- RUN_TABLE_END -->
