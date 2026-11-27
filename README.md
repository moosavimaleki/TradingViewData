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
| 📄 [2026-11-27T07-53-50Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-27T07-53-50Z.md) | ❌ `failed` | `2026-11-27` `11:23:50` |
| 📄 [2026-11-26T21-17-23Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-26T21-17-23Z.md) | ❌ `failed` | `2026-11-27` `00:47:23` |
| 📄 [2026-11-26T07-53-08Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-26T07-53-08Z.md) | ❌ `failed` | `2026-11-26` `11:23:08` |
| 📄 [2026-11-25T21-29-51Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-25T21-29-51Z.md) | ❌ `failed` | `2026-11-26` `00:59:51` |
| 📄 [2026-11-25T08-01-13Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-25T08-01-13Z.md) | ❌ `failed` | `2026-11-25` `11:31:13` |
| 📄 [2026-11-24T22-14-06Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-24T22-14-06Z.md) | ❌ `failed` | `2026-11-25` `01:44:06` |
| 📄 [2026-11-24T09-30-42Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-24T09-30-42Z.md) | ❌ `failed` | `2026-11-24` `13:00:42` |
| 📄 [2026-11-23T23-42-31Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-23T23-42-31Z.md) | ❌ `failed` | `2026-11-24` `03:12:31` |
| 📄 [2026-11-23T07-06-13Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-23T07-06-13Z.md) | ❌ `failed` | `2026-11-23` `10:36:13` |
| 📄 [2026-11-22T19-22-29Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-22T19-22-29Z.md) | ❌ `failed` | `2026-11-22` `22:52:29` |

<!-- RUN_TABLE_END -->
