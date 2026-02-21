# TradingViewData

این پروژه برای جمع‌آوری و به‌روزرسانی دیتای بازار از TradingView ساخته شده است.

## داده‌ها از کجا می‌آید؟

- منبع اصلی: TradingView
- نمادها/بازارهای فعال فعلی:
  - `XAUUSD` (BlackBull)
  - `XAGUSD` (BlackBull)
  - `EURUSD` (BlackBull)
  - `DXY` (TVC)
  - `BTCUSDT` (BINANCE)

## زمان‌بندی اجرا

- هر ۳ ساعت: اجرای `minor` (فقط تایم‌فریم‌های رنج: `10R`, `100R`, `1000R`)
- هر ۶ ساعت: اجرای `major` (همه تایم‌فریم‌ها + گزارش کامل)

## داده‌ها را از کجا بگیریم؟

- Google Drive (دیتای اصلی):
  - https://drive.google.com/drive/folders/189HIU2eouf3Ftzil_0Nmm1fk1yAgs61B?usp=sharing

## ساختار ذخیره‌سازی

- مسیر فایل‌ها به‌صورت سالانه ذخیره می‌شود:
  - `data/tradingview/{BROKER}/{TIMEFRAME}/{SYMBOL}/{RUN_YEAR}.parquet`
