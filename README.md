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
| 📄 [2026-10-12T15-05-28Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-12T15-05-28Z.md) | ❌ `failed` | `2026-10-12` `18:35:28` |
| 📄 [2026-10-12T05-33-20Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-12T05-33-20Z.md) | ✅ `success` | `2026-10-12` `09:03:20` |
| 📄 [2026-10-11T21-43-52Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-11T21-43-52Z.md) | ✅ `success` | `2026-10-12` `01:13:52` |
| 📄 [2026-10-11T12-32-53Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-11T12-32-53Z.md) | ❌ `failed` | `2026-10-11` `16:02:53` |
| 📄 [2026-10-11T05-21-45Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-11T05-21-45Z.md) | ✅ `success` | `2026-10-11` `08:51:45` |
| 📄 [2026-10-10T21-27-51Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-10T21-27-51Z.md) | ✅ `success` | `2026-10-11` `00:57:51` |
| 📄 [2026-10-10T12-16-47Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-10T12-16-47Z.md) | ✅ `success` | `2026-10-10` `15:46:47` |
| 📄 [2026-10-10T05-27-29Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-10T05-27-29Z.md) | ✅ `success` | `2026-10-10` `08:57:29` |
| 📄 [2026-10-09T22-30-21Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-09T22-30-21Z.md) | ✅ `success` | `2026-10-10` `02:00:21` |
| 📄 [2026-10-09T12-59-38Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-09T12-59-38Z.md) | ✅ `success` | `2026-10-09` `16:29:38` |

<!-- RUN_TABLE_END -->
