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
| 📄 [2026-04-29T19-45-37Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-29T19-45-37Z.md) | ✅ `success` | `2026-04-29` `23:15:37` |
| 📄 [2026-04-29T14-20-24Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-29T14-20-24Z.md) | ✅ `success` | `2026-04-29` `17:50:24` |
| 📄 [2026-04-29T08-28-20Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-29T08-28-20Z.md) | ✅ `success` | `2026-04-29` `11:58:20` |
| 📄 [2026-04-29T03-49-02Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-29T03-49-02Z.md) | ✅ `success` | `2026-04-29` `07:19:02` |
| 📄 [2026-04-28T19-50-11Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-28T19-50-11Z.md) | ✅ `success` | `2026-04-28` `23:20:11` |
| 📄 [2026-04-28T14-31-29Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-28T14-31-29Z.md) | ✅ `success` | `2026-04-28` `18:01:29` |
| 📄 [2026-04-28T08-34-43Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-28T08-34-43Z.md) | ❌ `failed` | `2026-04-28` `12:04:43` |
| 📄 [2026-04-28T03-51-40Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-28T03-51-40Z.md) | ✅ `success` | `2026-04-28` `07:21:40` |
| 📄 [2026-04-27T19-42-26Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-27T19-42-26Z.md) | ✅ `success` | `2026-04-27` `23:12:26` |
| 📄 [2026-04-27T14-13-02Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-27T14-13-02Z.md) | ✅ `success` | `2026-04-27` `17:43:02` |

<!-- RUN_TABLE_END -->
