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
| 📄 [2026-06-04T15-32-29Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-04T15-32-29Z.md) | ✅ `success` | `2026-06-04` `19:02:29` |
| 📄 [2026-06-04T10-06-56Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-04T10-06-56Z.md) | ✅ `success` | `2026-06-04` `13:36:56` |
| 📄 [2026-06-04T04-49-54Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-04T04-49-54Z.md) | ✅ `success` | `2026-06-04` `08:19:54` |
| 📄 [2026-06-03T21-23-04Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-03T21-23-04Z.md) | ✅ `success` | `2026-06-04` `00:53:04` |
| 📄 [2026-06-03T17-03-35Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-03T17-03-35Z.md) | ✅ `success` | `2026-06-03` `20:33:35` |
| 📄 [2026-06-03T11-15-37Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-03T11-15-37Z.md) | ✅ `success` | `2026-06-03` `14:45:37` |
| 📄 [2026-06-03T04-56-58Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-03T04-56-58Z.md) | ✅ `success` | `2026-06-03` `08:26:58` |
| 📄 [2026-06-02T21-17-28Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-02T21-17-28Z.md) | ✅ `success` | `2026-06-03` `00:47:28` |
| 📄 [2026-06-02T16-47-07Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-02T16-47-07Z.md) | ✅ `success` | `2026-06-02` `20:17:07` |
| 📄 [2026-06-02T10-48-02Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-02T10-48-02Z.md) | ✅ `success` | `2026-06-02` `14:18:02` |

<!-- RUN_TABLE_END -->
