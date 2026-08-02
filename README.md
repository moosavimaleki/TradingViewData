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
| 📄 [2026-08-02T08-32-10Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-02T08-32-10Z.md) | ❌ `failed` | `2026-08-02` `12:02:10` |
| 📄 [2026-08-02T03-35-01Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-02T03-35-01Z.md) | ❌ `failed` | `2026-08-02` `07:05:01` |
| 📄 [2026-08-01T19-18-50Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-01T19-18-50Z.md) | ❌ `failed` | `2026-08-01` `22:48:50` |
| 📄 [2026-08-01T13-42-10Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-01T13-42-10Z.md) | ❌ `failed` | `2026-08-01` `17:12:10` |
| 📄 [2026-08-01T08-29-18Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-01T08-29-18Z.md) | ❌ `failed` | `2026-08-01` `11:59:18` |
| 📄 [2026-08-01T03-35-08Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-01T03-35-08Z.md) | ❌ `failed` | `2026-08-01` `07:05:08` |
| 📄 [2026-07-31T19-43-47Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-31T19-43-47Z.md) | ❌ `failed` | `2026-07-31` `23:13:47` |
| 📄 [2026-07-31T14-23-29Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-31T14-23-29Z.md) | ❌ `failed` | `2026-07-31` `17:53:29` |
| 📄 [2026-07-31T09-10-44Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-31T09-10-44Z.md) | ❌ `failed` | `2026-07-31` `12:40:44` |
| 📄 [2026-07-31T03-35-31Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-31T03-35-31Z.md) | ❌ `failed` | `2026-07-31` `07:05:31` |

<!-- RUN_TABLE_END -->
