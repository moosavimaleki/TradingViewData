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
| 📄 [2026-05-04T19-49-13Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-04T19-49-13Z.md) | ✅ `success` | `2026-05-04` `23:19:13` |
| 📄 [2026-05-04T14-20-08Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-04T14-20-08Z.md) | ✅ `success` | `2026-05-04` `17:50:08` |
| 📄 [2026-05-04T08-38-55Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-04T08-38-55Z.md) | ✅ `success` | `2026-05-04` `12:08:55` |
| 📄 [2026-05-04T03-53-56Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-04T03-53-56Z.md) | ❌ `failed` | `2026-05-04` `07:23:56` |
| 📄 [2026-05-03T19-09-47Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-03T19-09-47Z.md) | ✅ `success` | `2026-05-03` `22:39:47` |
| 📄 [2026-05-03T13-38-04Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-03T13-38-04Z.md) | ✅ `success` | `2026-05-03` `17:08:04` |
| 📄 [2026-05-03T08-08-46Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-03T08-08-46Z.md) | ✅ `success` | `2026-05-03` `11:38:46` |
| 📄 [2026-05-03T03-56-09Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-03T03-56-09Z.md) | ✅ `success` | `2026-05-03` `07:26:09` |
| 📄 [2026-05-02T19-10-32Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-02T19-10-32Z.md) | ✅ `success` | `2026-05-02` `22:40:32` |
| 📄 [2026-05-02T13-26-48Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-02T13-26-48Z.md) | ✅ `success` | `2026-05-02` `16:56:48` |

<!-- RUN_TABLE_END -->
