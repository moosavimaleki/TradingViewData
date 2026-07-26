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
| 📄 [2026-07-26T03-37-32Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-26T03-37-32Z.md) | ✅ `success` | `2026-07-26` `07:07:32` |
| 📄 [2026-07-25T19-17-42Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-25T19-17-42Z.md) | ✅ `success` | `2026-07-25` `22:47:42` |
| 📄 [2026-07-25T13-49-50Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-25T13-49-50Z.md) | ✅ `success` | `2026-07-25` `17:19:50` |
| 📄 [2026-07-25T08-16-17Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-25T08-16-17Z.md) | ✅ `success` | `2026-07-25` `11:46:17` |
| 📄 [2026-07-25T03-23-47Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-25T03-23-47Z.md) | ✅ `success` | `2026-07-25` `06:53:47` |
| 📄 [2026-07-24T19-38-53Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-24T19-38-53Z.md) | ✅ `success` | `2026-07-24` `23:08:53` |
| 📄 [2026-07-24T13-59-45Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-24T13-59-45Z.md) | ✅ `success` | `2026-07-24` `17:29:45` |
| 📄 [2026-07-24T08-35-39Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-24T08-35-39Z.md) | ✅ `success` | `2026-07-24` `12:05:39` |
| 📄 [2026-07-24T03-25-43Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-24T03-25-43Z.md) | ✅ `success` | `2026-07-24` `06:55:43` |
| 📄 [2026-07-23T14-20-54Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-23T14-20-54Z.md) | ✅ `success` | `2026-07-23` `17:50:54` |

<!-- RUN_TABLE_END -->
