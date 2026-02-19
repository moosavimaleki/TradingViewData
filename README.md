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
- سینک بهینه با Google Drive:
  - قبل از اجرا فقط `manifest.json` و chunk های آخر دانلود می‌شوند.
  - بعد از اجرا فقط فایل‌های تغییر کرده آپلود می‌شوند.

## ساختار دیتا

```
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

Workflow آماده:  
`.github/workflows/collect-and-backup.yml`

زمان‌بندی فعلی:
- `06:00 UTC`
- `18:00 UTC`

### Secrets موردنیاز

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

## نکات

- فایل `data/` در `.gitignore` است و وارد ریپو نمی‌شود.
- برای تغییر تعداد کندل هر chunk:
  - `storage.chunk_size` در `data_collector/config/settings.json`
- برای میزان بازنویسی tail هنگام merge:
  - `storage.merge_tail_chunks` در `data_collector/config/settings.json`
