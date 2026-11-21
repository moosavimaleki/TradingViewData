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

- هر ساعت: جمع‌آوری رنج‌های `10R`, `100R`, `1000R`؛ در ساعت‌های غیر از اجرای `major` با حالت `minor`
- هر ۶ ساعت: اجرای `major` (همه تایم‌فریم‌ها + گزارش کامل)

علت دریافت ساعتی، تغییر مشاهده‌شدهٔ تاریخچهٔ رنج حتی برای دادهٔ حدود ۹۳ دقیقه قبل است؛ این تصمیم تضمینِ ثباتِ یک ساعت اخیر نیست. تشخیص منبع پیش از ذخیره، جلوی بازنویسی فایل اصلی با رنج منطبق با بازسازی M1 یا نامشخص را می‌گیرد. [تصمیم و شواهد ADR](docs/adr/0001-hourly-range-collection-and-source-guard.fa.md).

<!-- RUN_TABLE_START -->
## 🕒 آخرین اجراها

| گزارش | وضعیت | زمان اجرا (تهران) |
|---|---|---|
| 📄 [2026-11-21T18-59-18Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-21T18-59-18Z.md) | ❌ `failed` | `2026-11-21` `22:29:18` |
| 📄 [2026-11-21T06-44-52Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-21T06-44-52Z.md) | ❌ `failed` | `2026-11-21` `10:14:52` |
| 📄 [2026-11-20T23-53-41Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-20T23-53-41Z.md) | ❌ `failed` | `2026-11-21` `03:23:41` |
| 📄 [2026-11-20T15-13-36Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-20T15-13-36Z.md) | ❌ `failed` | `2026-11-20` `18:43:36` |
| 📄 [2026-11-20T00-30-26Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-20T00-30-26Z.md) | ❌ `failed` | `2026-11-20` `04:00:26` |
| 📄 [2026-11-19T15-34-36Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-19T15-34-36Z.md) | ❌ `failed` | `2026-11-19` `19:04:36` |
| 📄 [2026-11-19T00-08-41Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-19T00-08-41Z.md) | ❌ `failed` | `2026-11-19` `03:38:41` |
| 📄 [2026-11-18T15-28-17Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-18T15-28-17Z.md) | ❌ `failed` | `2026-11-18` `18:58:17` |
| 📄 [2026-11-18T00-50-29Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-18T00-50-29Z.md) | ❌ `failed` | `2026-11-18` `04:20:29` |
| 📄 [2026-11-17T15-48-51Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-17T15-48-51Z.md) | ❌ `failed` | `2026-11-17` `19:18:51` |

<!-- RUN_TABLE_END -->
