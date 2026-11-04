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
| 📄 [2026-11-04T14-12-52Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-04T14-12-52Z.md) | ❌ `failed` | `2026-11-04` `17:42:52` |
| 📄 [2026-11-04T05-52-05Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-04T05-52-05Z.md) | ❌ `failed` | `2026-11-04` `09:22:05` |
| 📄 [2026-11-03T23-07-13Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-03T23-07-13Z.md) | ✅ `success` | `2026-11-04` `02:37:13` |
| 📄 [2026-11-03T13-57-41Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-03T13-57-41Z.md) | ❌ `failed` | `2026-11-03` `17:27:41` |
| 📄 [2026-11-03T00-50-08Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-03T00-50-08Z.md) | ✅ `success` | `2026-11-03` `04:20:08` |
| 📄 [2026-11-02T15-26-38Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-02T15-26-38Z.md) | ✅ `success` | `2026-11-02` `18:56:38` |
| 📄 [2026-11-02T05-36-06Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-02T05-36-06Z.md) | ✅ `success` | `2026-11-02` `09:06:06` |
| 📄 [2026-11-01T21-54-56Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-01T21-54-56Z.md) | ✅ `success` | `2026-11-02` `01:24:56` |
| 📄 [2026-11-01T13-03-01Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-01T13-03-01Z.md) | ✅ `success` | `2026-11-01` `16:33:01` |
| 📄 [2026-11-01T05-38-20Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-01T05-38-20Z.md) | ✅ `success` | `2026-11-01` `09:08:20` |

<!-- RUN_TABLE_END -->
