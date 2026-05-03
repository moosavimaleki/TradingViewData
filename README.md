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
| 📄 [2026-05-03T19-09-47Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-03T19-09-47Z.md) | ✅ `success` | `2026-05-03` `22:39:47` |
| 📄 [2026-05-03T13-38-04Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-03T13-38-04Z.md) | ✅ `success` | `2026-05-03` `17:08:04` |
| 📄 [2026-05-03T08-08-46Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-03T08-08-46Z.md) | ✅ `success` | `2026-05-03` `11:38:46` |
| 📄 [2026-05-03T03-56-09Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-03T03-56-09Z.md) | ✅ `success` | `2026-05-03` `07:26:09` |
| 📄 [2026-05-02T19-10-32Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-02T19-10-32Z.md) | ✅ `success` | `2026-05-02` `22:40:32` |
| 📄 [2026-05-02T13-26-48Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-02T13-26-48Z.md) | ✅ `success` | `2026-05-02` `16:56:48` |
| 📄 [2026-05-02T07-53-29Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-02T07-53-29Z.md) | ✅ `success` | `2026-05-02` `11:23:29` |
| 📄 [2026-05-02T03-34-14Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-02T03-34-14Z.md) | ✅ `success` | `2026-05-02` `07:04:14` |
| 📄 [2026-05-01T19-21-03Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-01T19-21-03Z.md) | ✅ `success` | `2026-05-01` `22:51:03` |
| 📄 [2026-05-01T13-43-03Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-01T13-43-03Z.md) | ✅ `success` | `2026-05-01` `17:13:03` |

<!-- RUN_TABLE_END -->
