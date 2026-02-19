# TradingViewData

پروژه‌ی مینیمال برای دانلود و آپدیت افزایشی دیتا (مخصوص اجرا در GitHub Actions) بدون پابلیک کردن کل پروژه اصلی.

## ویژگی‌ها

- فقط بخش لازم از `data_collector` منتقل شده.
- ذخیره‌سازی به صورت `CSV chunked`:
  - هر `10,000` کندل یک فایل: `SYMBOL_0.csv.gz`, `SYMBOL_1.csv.gz`, ...
  - کنار هر دیتاست یک `manifest.json` نگه داشته می‌شود.
- آپدیت افزایشی:
  - فقط tail chunk ها merge/rewrite می‌شوند (پیش‌فرض 2 chunk آخر).
  - برای تشخیص `latest timestamp` لازم نیست کل دیتاست خوانده شود.
- رفتار idempotent و fail-safe:
  - اجرای تکراری با همان داده باعث duplicate نمی‌شود.
  - dedupe بر اساس `timestamp` انجام می‌شود.
  - اگر `manifest` موجود باشد ولی tail chunk ها ناقص دانلود شده باشند، write متوقف می‌شود تا دیتاست خراب نشود.
- کندل ناپایدار انتهایی:
  - برای `100R` و سایر range-barها آخرین کندل همیشه قبل از ذخیره حذف می‌شود.
  - برای time-barها (مثل `1m`, `5m`, `1h`, `1d`) اگر کندل آخر مربوط به bucket بازِ فعلی باشد، ذخیره نمی‌شود.
  - برای `update_only` هم overlap اعمال می‌شود تا اگر کندل ناقص قبلاً وارد شده بود در اجرای بعدی اصلاح/جایگزین شود.
- تأخیر چندروزه:
  - برای سورس‌های TradingView time-bar، backfill به‌صورت پنجره‌ای انجام می‌شود تا سقف `max_fetch_bars` باعث از دست رفتن بازه‌های قدیمی نشود.
- سینک بهینه با Google Drive:
  - قبل از اجرا فقط `manifest.json` و chunk های آخر دانلود می‌شوند.
  - بعد از اجرا فقط فایل‌های تغییر کرده آپلود می‌شوند.

## ساختار دیتا

```text
data/
  <source>/
    <broker>/
      <timeframe>/
        <symbol>/
          manifest.json
          <symbol>_0.csv.gz
          <symbol>_1.csv.gz
```

## تنظیمات اصلی

- `config/collect_jobs.json`: لیست job ها (source/symbol/broker/timeframe)
- `data_collector/config/settings.json`: تنظیمات سورس‌ها، storage، logging

## اجرای لوکال

```bash
python -m pip install -r requirements.txt
python -m data_collector.run --config config/collect_jobs.json --dry-run
python -m data_collector.run --config config/collect_jobs.json
```

## GitHub Actions

Workflow اصلی:
- `.github/workflows/collect-and-backup.yml`
  - در هر اجرا از `proxifly/free-proxy-list` لیست پروکسی می‌گیرد،
  - پروکسی‌ها را با تست واقعی WebSocket به TradingView صحت‌سنجی می‌کند،
  - ۱۰ پروکسی سالم را در `TV_WS_PROXY` (multi-line pool) ست می‌کند.
  - اگر کمتر از ۱۰ پروکسی سالم پیدا شود، job fail می‌شود (تا با تنظیمات نیمه‌خراب جلو نرود).

Workflow تست دیده‌شدن:
- `.github/workflows/ping.yml`

## Secrets موردنیاز

حداقل:
- `GDRIVE_SA_JSON`
- `GDRIVE_FOLDER_ID`

اختیاری (بسته به سورس):
- `FARAZ_COOKIES`
- `TV_FASTPASS_COOKIE_STRING`
- `TV_FASTPASS_CHART_URL`
- `TV_FASTPASS_WS_URL`
- `TV_FASTPASS_WS_ORIGIN`
- `TV_AUTH_TOKEN`

اختیاری (برای WebSocket پایتون، فقط در مرحله Run collector):
- `TV_WS_PROXY` (می‌تواند یک proxy یا pool چندخطی/Comma-separated باشد)
- `TV_FASTPASS_WS_PROXY` (می‌تواند یک proxy یا pool چندخطی/Comma-separated باشد)

نکته:
- اسکریپت `scripts/select_ws_proxies.py` پروتکل‌های `http/https/socks4/socks5` را تست و پشتیبانی می‌کند.
- در کد، برای retry ها بین proxy های pool چرخش انجام می‌شود.
