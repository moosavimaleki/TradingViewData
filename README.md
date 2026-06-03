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
| 📄 [2026-06-03T11-15-37Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-03T11-15-37Z.md) | ✅ `success` | `2026-06-03` `14:45:37` |
| 📄 [2026-06-03T04-56-58Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-03T04-56-58Z.md) | ✅ `success` | `2026-06-03` `08:26:58` |
| 📄 [2026-06-02T21-17-28Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-02T21-17-28Z.md) | ✅ `success` | `2026-06-03` `00:47:28` |
| 📄 [2026-06-02T16-47-07Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-02T16-47-07Z.md) | ✅ `success` | `2026-06-02` `20:17:07` |
| 📄 [2026-06-02T10-48-02Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-02T10-48-02Z.md) | ✅ `success` | `2026-06-02` `14:18:02` |
| 📄 [2026-06-02T04-46-49Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-02T04-46-49Z.md) | ✅ `success` | `2026-06-02` `08:16:49` |
| 📄 [2026-06-01T21-40-13Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-01T21-40-13Z.md) | ✅ `success` | `2026-06-02` `01:10:13` |
| 📄 [2026-06-01T17-54-56Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-01T17-54-56Z.md) | ✅ `success` | `2026-06-01` `21:24:56` |
| 📄 [2026-06-01T11-49-10Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-01T11-49-10Z.md) | ✅ `success` | `2026-06-01` `15:19:10` |
| 📄 [2026-06-01T05-00-23Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-01T05-00-23Z.md) | ✅ `success` | `2026-06-01` `08:30:23` |

<!-- RUN_TABLE_END -->
