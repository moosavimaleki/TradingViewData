# TradingViewData

این پروژه برای جمع‌آوری و به‌روزرسانی دیتای بازار از TradingView ساخته شده است.


## داده‌ها را از کجا بگیریم؟

- Google Drive (دیتای اصلی):
  - https://drive.google.com/drive/folders/189HIU2eouf3Ftzil_0Nmm1fk1yAgs61B?usp=sharing

## ساختار ذخیره‌سازی

- مسیر فایل‌ها به‌صورت سالانه ذخیره می‌شود:
  - `data/tradingview/{BROKER}/{TIMEFRAME}/{SYMBOL}/{RUN_YEAR}.parquet`

## زمان‌بندی اجرا

- هر ۳ ساعت: اجرای `minor` (فقط تایم‌فریم‌های رنج: `10R`, `100R`, `1000R`)
- هر ۶ ساعت: اجرای `major` (همه تایم‌فریم‌ها + گزارش کامل)


<!-- RUN_TABLE_START -->
## آخرین اجراها

| لینک گزارش | وضعیت اجرا | زمان اجرا (UTC) |
|---|---|---|
| [2026-02-21T13-04-00Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-21T13-04-00Z.md) | success | 2026-02-21T13:04:00Z |
| [2026-02-21T11-34-51Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-21T11-34-51Z.md) | success | 2026-02-21T11:34:51Z |
| [2026-02-21T06-53-47Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-21T06-53-47Z.md) | success | 2026-02-21T06:53:47Z |
| [2026-02-21T04-04-22Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-21T04-04-22Z.md) | success | 2026-02-21T04:04:22Z |
| [2026-02-20T18-31-14Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-20T18-31-14Z.md) | success | 2026-02-20T18:31:14Z |
| [2026-02-20T17-08-16Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-20T17-08-16Z.md) | success | 2026-02-20T17:08:16Z |
| [2026-02-20.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-20.md) | failed | 2026-02-20T16:36:34Z |

<!-- RUN_TABLE_END -->
