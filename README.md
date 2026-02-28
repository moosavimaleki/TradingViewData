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
| 📄 [2026-02-28T06-50-35Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-28T06-50-35Z.md) | ✅ `success` | `2026-02-28` `10:20:35` |
| 📄 [2026-02-28T02-30-15Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-28T02-30-15Z.md) | ✅ `success` | `2026-02-28` `06:00:15` |
| 📄 [2026-02-27T18-55-46Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-27T18-55-46Z.md) | ✅ `success` | `2026-02-27` `22:25:46` |
| 📄 [2026-02-27T13-14-50Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-27T13-14-50Z.md) | ✅ `success` | `2026-02-27` `16:44:50` |
| 📄 [2026-02-27T07-04-00Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-27T07-04-00Z.md) | ✅ `success` | `2026-02-27` `10:34:00` |
| 📄 [2026-02-27T02-41-43Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-27T02-41-43Z.md) | ✅ `success` | `2026-02-27` `06:11:43` |
| 📄 [2026-02-26T19-01-47Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-26T19-01-47Z.md) | ✅ `success` | `2026-02-26` `22:31:47` |
| 📄 [2026-02-26T13-23-55Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-26T13-23-55Z.md) | ✅ `success` | `2026-02-26` `16:53:55` |
| 📄 [2026-02-26T07-09-50Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-26T07-09-50Z.md) | ✅ `success` | `2026-02-26` `10:39:50` |
| 📄 [2026-02-26T02-43-00Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-26T02-43-00Z.md) | ✅ `success` | `2026-02-26` `06:13:00` |

<!-- RUN_TABLE_END -->
