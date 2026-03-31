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
| 📄 [2026-03-31T03-16-45Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-31T03-16-45Z.md) | ✅ `success` | `2026-03-31` `06:46:45` |
| 📄 [2026-03-30T19-10-29Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-30T19-10-29Z.md) | ✅ `success` | `2026-03-30` `22:40:29` |
| 📄 [2026-03-30T13-50-34Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-30T13-50-34Z.md) | ✅ `success` | `2026-03-30` `17:20:34` |
| 📄 [2026-03-30T07-54-26Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-30T07-54-26Z.md) | ✅ `success` | `2026-03-30` `11:24:26` |
| 📄 [2026-03-30T03-25-37Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-30T03-25-37Z.md) | ✅ `success` | `2026-03-30` `06:55:37` |
| 📄 [2026-03-29T18-54-55Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-29T18-54-55Z.md) | ✅ `success` | `2026-03-29` `22:24:55` |
| 📄 [2026-03-29T13-11-53Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-29T13-11-53Z.md) | ✅ `success` | `2026-03-29` `16:41:53` |
| 📄 [2026-03-29T07-14-31Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-29T07-14-31Z.md) | ✅ `success` | `2026-03-29` `10:44:31` |
| 📄 [2026-03-29T03-22-08Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-29T03-22-08Z.md) | ✅ `success` | `2026-03-29` `06:52:08` |
| 📄 [2026-03-28T18-53-09Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-28T18-53-09Z.md) | ✅ `success` | `2026-03-28` `22:23:09` |

<!-- RUN_TABLE_END -->
