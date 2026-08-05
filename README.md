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
| 📄 [2026-08-05T03-16-18Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-05T03-16-18Z.md) | ❌ `failed` | `2026-08-05` `06:46:18` |
| 📄 [2026-08-04T19-45-27Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-04T19-45-27Z.md) | ❌ `failed` | `2026-08-04` `23:15:27` |
| 📄 [2026-08-04T14-30-59Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-04T14-30-59Z.md) | ❌ `failed` | `2026-08-04` `18:00:59` |
| 📄 [2026-08-04T08-48-15Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-04T08-48-15Z.md) | ❌ `failed` | `2026-08-04` `12:18:15` |
| 📄 [2026-08-04T03-20-53Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-04T03-20-53Z.md) | ❌ `failed` | `2026-08-04` `06:50:53` |
| 📄 [2026-08-03T19-46-07Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-03T19-46-07Z.md) | ❌ `failed` | `2026-08-03` `23:16:07` |
| 📄 [2026-08-03T14-54-49Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-03T14-54-49Z.md) | ❌ `failed` | `2026-08-03` `18:24:49` |
| 📄 [2026-08-03T09-58-24Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-03T09-58-24Z.md) | ❌ `failed` | `2026-08-03` `13:28:24` |
| 📄 [2026-08-03T03-37-17Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-03T03-37-17Z.md) | ❌ `failed` | `2026-08-03` `07:07:17` |
| 📄 [2026-08-02T19-19-57Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-02T19-19-57Z.md) | ❌ `failed` | `2026-08-02` `22:49:57` |

<!-- RUN_TABLE_END -->
