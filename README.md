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
| 📄 [2026-11-24T09-30-42Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-24T09-30-42Z.md) | ❌ `failed` | `2026-11-24` `13:00:42` |
| 📄 [2026-11-23T23-42-31Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-23T23-42-31Z.md) | ❌ `failed` | `2026-11-24` `03:12:31` |
| 📄 [2026-11-23T07-06-13Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-23T07-06-13Z.md) | ❌ `failed` | `2026-11-23` `10:36:13` |
| 📄 [2026-11-22T19-22-29Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-22T19-22-29Z.md) | ❌ `failed` | `2026-11-22` `22:52:29` |
| 📄 [2026-11-22T06-15-08Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-22T06-15-08Z.md) | ❌ `failed` | `2026-11-22` `09:45:08` |
| 📄 [2026-11-21T18-59-18Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-21T18-59-18Z.md) | ❌ `failed` | `2026-11-21` `22:29:18` |
| 📄 [2026-11-21T06-44-52Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-21T06-44-52Z.md) | ❌ `failed` | `2026-11-21` `10:14:52` |
| 📄 [2026-11-20T23-53-41Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-20T23-53-41Z.md) | ❌ `failed` | `2026-11-21` `03:23:41` |
| 📄 [2026-11-20T15-13-36Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-20T15-13-36Z.md) | ❌ `failed` | `2026-11-20` `18:43:36` |
| 📄 [2026-11-20T00-30-26Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-20T00-30-26Z.md) | ❌ `failed` | `2026-11-20` `04:00:26` |

<!-- RUN_TABLE_END -->
