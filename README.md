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
| 📄 [2026-05-07T03-49-08Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-07T03-49-08Z.md) | ✅ `success` | `2026-05-07` `07:19:08` |
| 📄 [2026-05-06T19-55-11Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-06T19-55-11Z.md) | ✅ `success` | `2026-05-06` `23:25:11` |
| 📄 [2026-05-06T14-32-29Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-06T14-32-29Z.md) | ❌ `failed` | `2026-05-06` `18:02:29` |
| 📄 [2026-05-06T08-36-42Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-06T08-36-42Z.md) | ✅ `success` | `2026-05-06` `12:06:42` |
| 📄 [2026-05-06T03-50-35Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-06T03-50-35Z.md) | ✅ `success` | `2026-05-06` `07:20:35` |
| 📄 [2026-05-05T19-44-33Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-05T19-44-33Z.md) | ✅ `success` | `2026-05-05` `23:14:33` |
| 📄 [2026-05-05T14-13-20Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-05T14-13-20Z.md) | ✅ `success` | `2026-05-05` `17:43:20` |
| 📄 [2026-05-05T08-20-46Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-05T08-20-46Z.md) | ✅ `success` | `2026-05-05` `11:50:46` |
| 📄 [2026-05-05T03-34-46Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-05T03-34-46Z.md) | ✅ `success` | `2026-05-05` `07:04:46` |
| 📄 [2026-05-04T19-49-13Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-04T19-49-13Z.md) | ✅ `success` | `2026-05-04` `23:19:13` |

<!-- RUN_TABLE_END -->
