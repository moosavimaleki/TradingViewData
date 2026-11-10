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
| 📄 [2026-11-10T01-24-02Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-10T01-24-02Z.md) | ❌ `failed` | `2026-11-10` `04:54:02` |
| 📄 [2026-11-09T15-53-10Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-09T15-53-10Z.md) | ❌ `failed` | `2026-11-09` `19:23:10` |
| 📄 [2026-11-09T05-49-32Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-09T05-49-32Z.md) | ✅ `success` | `2026-11-09` `09:19:32` |
| 📄 [2026-11-08T21-54-20Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-08T21-54-20Z.md) | ✅ `success` | `2026-11-09` `01:24:20` |
| 📄 [2026-11-08T13-07-34Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-08T13-07-34Z.md) | ✅ `success` | `2026-11-08` `16:37:34` |
| 📄 [2026-11-08T05-39-38Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-08T05-39-38Z.md) | ✅ `success` | `2026-11-08` `09:09:38` |
| 📄 [2026-11-07T21-40-33Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-07T21-40-33Z.md) | ✅ `success` | `2026-11-08` `01:10:33` |
| 📄 [2026-11-07T12-47-45Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-07T12-47-45Z.md) | ✅ `success` | `2026-11-07` `16:17:45` |
| 📄 [2026-11-07T05-37-40Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-07T05-37-40Z.md) | ✅ `success` | `2026-11-07` `09:07:40` |
| 📄 [2026-11-06T19-11-56Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-06T19-11-56Z.md) | ✅ `success` | `2026-11-06` `22:41:56` |

<!-- RUN_TABLE_END -->
