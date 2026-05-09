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
| 📄 [2026-05-09T19-13-38Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-09T19-13-38Z.md) | ✅ `success` | `2026-05-09` `22:43:38` |
| 📄 [2026-05-09T13-41-15Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-09T13-41-15Z.md) | ✅ `success` | `2026-05-09` `17:11:15` |
| 📄 [2026-05-09T08-04-01Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-09T08-04-01Z.md) | ✅ `success` | `2026-05-09` `11:34:01` |
| 📄 [2026-05-09T03-41-09Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-09T03-41-09Z.md) | ✅ `success` | `2026-05-09` `07:11:09` |
| 📄 [2026-05-08T19-39-00Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-08T19-39-00Z.md) | ✅ `success` | `2026-05-08` `23:09:00` |
| 📄 [2026-05-08T14-05-39Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-08T14-05-39Z.md) | ✅ `success` | `2026-05-08` `17:35:39` |
| 📄 [2026-05-08T07-50-01Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-08T07-50-01Z.md) | ✅ `success` | `2026-05-08` `11:20:01` |
| 📄 [2026-05-08T03-39-51Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-08T03-39-51Z.md) | ✅ `success` | `2026-05-08` `07:09:51` |
| 📄 [2026-05-07T19-48-53Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-07T19-48-53Z.md) | ✅ `success` | `2026-05-07` `23:18:53` |
| 📄 [2026-05-07T14-34-19Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-07T14-34-19Z.md) | ✅ `success` | `2026-05-07` `18:04:19` |

<!-- RUN_TABLE_END -->
