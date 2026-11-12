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
| 📄 [2026-11-12T14-57-51Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-12T14-57-51Z.md) | ❌ `failed` | `2026-11-12` `18:27:51` |
| 📄 [2026-11-12T00-24-43Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-12T00-24-43Z.md) | ❌ `failed` | `2026-11-12` `03:54:43` |
| 📄 [2026-11-11T13-56-48Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-11T13-56-48Z.md) | ❌ `failed` | `2026-11-11` `17:26:48` |
| 📄 [2026-11-11T05-45-32Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-11T05-45-32Z.md) | ❌ `failed` | `2026-11-11` `09:15:32` |
| 📄 [2026-11-10T23-05-03Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-10T23-05-03Z.md) | ❌ `failed` | `2026-11-11` `02:35:03` |
| 📄 [2026-11-10T14-41-20Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-10T14-41-20Z.md) | ❌ `failed` | `2026-11-10` `18:11:20` |
| 📄 [2026-11-10T01-24-02Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-10T01-24-02Z.md) | ❌ `failed` | `2026-11-10` `04:54:02` |
| 📄 [2026-11-09T15-53-10Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-09T15-53-10Z.md) | ❌ `failed` | `2026-11-09` `19:23:10` |
| 📄 [2026-11-09T05-49-32Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-09T05-49-32Z.md) | ✅ `success` | `2026-11-09` `09:19:32` |
| 📄 [2026-11-08T21-54-20Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-08T21-54-20Z.md) | ✅ `success` | `2026-11-09` `01:24:20` |

<!-- RUN_TABLE_END -->
