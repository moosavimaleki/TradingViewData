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
| 📄 [2026-05-19T04-12-48Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-19T04-12-48Z.md) | ✅ `success` | `2026-05-19` `07:42:48` |
| 📄 [2026-05-18T19-53-55Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-18T19-53-55Z.md) | ✅ `success` | `2026-05-18` `23:23:55` |
| 📄 [2026-05-18T15-49-02Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-18T15-49-02Z.md) | ✅ `success` | `2026-05-18` `19:19:02` |
| 📄 [2026-05-18T10-18-43Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-18T10-18-43Z.md) | ✅ `success` | `2026-05-18` `13:48:43` |
| 📄 [2026-05-18T04-18-01Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-18T04-18-01Z.md) | ✅ `success` | `2026-05-18` `07:48:01` |
| 📄 [2026-05-17T19-18-30Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-17T19-18-30Z.md) | ✅ `success` | `2026-05-17` `22:48:30` |
| 📄 [2026-05-17T13-47-04Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-17T13-47-04Z.md) | ✅ `success` | `2026-05-17` `17:17:04` |
| 📄 [2026-05-17T08-28-49Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-17T08-28-49Z.md) | ✅ `success` | `2026-05-17` `11:58:49` |
| 📄 [2026-05-17T04-05-04Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-17T04-05-04Z.md) | ✅ `success` | `2026-05-17` `07:35:04` |
| 📄 [2026-05-16T19-15-37Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-16T19-15-37Z.md) | ✅ `success` | `2026-05-16` `22:45:37` |

<!-- RUN_TABLE_END -->
