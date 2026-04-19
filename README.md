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
| 📄 [2026-04-19T07-40-14Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-19T07-40-14Z.md) | ✅ `success` | `2026-04-19` `11:10:14` |
| 📄 [2026-04-19T03-36-31Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-19T03-36-31Z.md) | ✅ `success` | `2026-04-19` `07:06:31` |
| 📄 [2026-04-18T19-01-42Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-18T19-01-42Z.md) | ✅ `success` | `2026-04-18` `22:31:42` |
| 📄 [2026-04-18T13-17-18Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-18T13-17-18Z.md) | ✅ `success` | `2026-04-18` `16:47:18` |
| 📄 [2026-04-18T07-19-43Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-18T07-19-43Z.md) | ✅ `success` | `2026-04-18` `10:49:43` |
| 📄 [2026-04-18T03-17-41Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-18T03-17-41Z.md) | ✅ `success` | `2026-04-18` `06:47:41` |
| 📄 [2026-04-17T19-11-31Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-17T19-11-31Z.md) | ✅ `success` | `2026-04-17` `22:41:31` |
| 📄 [2026-04-17T13-46-58Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-17T13-46-58Z.md) | ✅ `success` | `2026-04-17` `17:16:58` |
| 📄 [2026-04-17T08-00-15Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-17T08-00-15Z.md) | ✅ `success` | `2026-04-17` `11:30:15` |
| 📄 [2026-04-17T03-29-40Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-17T03-29-40Z.md) | ✅ `success` | `2026-04-17` `06:59:40` |

<!-- RUN_TABLE_END -->
