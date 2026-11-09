# Collector

ساختار ساده و لایه‌ای:

- `simple_tvdatafeed_collector.py`: Runner
- `pipeline/config.py`: خواندن jobها و نرمال‌سازی تنظیمات
- `pipeline/fetchers.py`: دریافت time-bar با `tvdatafeed`
- `pipeline/ws_fetcher.py`: دریافت range-bar مثل `100R` با websocket
- `pipeline/normalize.py`: نرمال‌سازی دیتافریم (تبدیل `ts` به epoch-seconds و حذف آخرین کندل)
- `pipeline/storage.py`: خواندن/ادغام/ذخیره Parquet سالانه
- `pipeline/raw_archive.py`: ثبت مستقل دادهٔ خام پیش از parse، نرمال‌سازی و ادغام

فرمت خروجی:

`data/tradingview/{BROKER}/{TIMEFRAME}/{SYMBOL}/{RUN_YEAR}.parquet`

در تایم‌فریم‌های رنج، ترتیب ردیف‌ها همان ترتیب سری دریافتی از WebSocket است؛
چند کندل با `ts` یکسان حفظ می‌شوند. `bar_index` فقط در همان اتصال معتبر است
و هویت دائمی کندل بین دو دریافت نیست.

هر دریافت جدید، تمام ردیف‌های قبلی از اولین `ts` دریافت جدید به بعد را
جایگزین می‌کند؛ فقط ردیف‌های قدیمی‌تر نگه داشته می‌شوند. اگر دریافت به مرز
overlap نرسد، اجرا برای آن job خطا می‌دهد و فایل قبلی تغییر نمی‌کند.
تعداد کم‌تر کندل نسبت به درخواست، به‌تنهایی نشانهٔ دریافت کل تاریخچه نیست.
در گزارش، `replaced_rows` تعداد ردیف‌های قدیمی جایگزین‌شده را نشان می‌دهد.

WebSocket باید پایان هر پاسخ را با `series_completed` اعلام کند و indexهای
کندل‌های رنج نباید فاصله داشته باشند. دریافت ناقص یا دارای مقدار نامعتبر
ذخیره نمی‌شود. همچنین دریافت جدید نباید انتهای شناخته‌شدهٔ فایل را کوتاه کند.
برای مرز شروع، ترتیب و مقادیر کندل‌های آن ثانیه با نسخهٔ قبلی بررسی می‌شود؛
اگر مرز مبهم باشد دادهٔ بیشتری دریافت می‌شود و اگر ابهام رفع نشود فایل تغییر نمی‌کند.
این مقایسه فقط برای بررسی مرز اتصال است؛ کندل‌های هم‌زمان یا حتی یکسان حذف نمی‌شوند.

مثال اجرا:

```bash
python collector/simple_tvdatafeed_collector.py \
  --config config/collect_jobs.json \
  --data-root data
```

## آرشیو خام و بازیابی

collector همیشه زیر `DATA_ROOT/raw` یک مسیر جدید شامل زمان UTC و UUID می‌سازد.
همهٔ نمادها، تایم‌فریم‌ها و تلاش‌های دریافتِ آن اجرا در یک `data.parquet`
با فشرده‌سازی ZSTD سطح ۹ جمع می‌شوند. `manifest.json` شامل SHA-256 فایل و
هش محتوای منطقی ردیف‌هاست. هیچ تبدیل float32، گردکردن یا حذف تکراری انجام نمی‌شود.

- پیام ورودی WebSocket پیش از decode/parse با همان bytes ثبت می‌شود، حتی برای پاسخ ناقص یا نامعتبر.
- دیتافریم ورودی همراه ستون‌ها، index و timezone در Arrow IPC ثبت می‌شود؛ آخرین کندل هم حفظ می‌شود.
- برای time-bar، خام یعنی خروجی کتابخانهٔ `tvDatafeed` پیش از اصلاح timezone در این پروژه.
- `sequence` ترتیب دریافت، و `request_id` مرز هر درخواست را مشخص می‌کنند؛ timestamp شناسه نیست.
- فایل تنظیمات اجرا و شناسهٔ اجرای GitHub هم ثبت می‌شوند؛ credential و پیام‌های ارسالی احراز هویت ثبت نمی‌شوند.

هر پیام ابتدا در یک قطعهٔ مستقل و fsync‌شده ثبت می‌شود. پایان اجرا قطعه‌ها
بدون حذف یا ادغام ردیف‌ها تجمیع و دوباره از نظر checksum بررسی می‌شوند.
قطعه‌های موقت فقط محلی‌اند؛ Drive تنها پارکت نهایی و manifest را دریافت می‌کند:

`gdrive:market-data/raw/tradingview/YYYY-MM-DD/RUN_ID/data.parquet`

workflow حتی پس از خطای collector آرشیو را می‌بندد و آپلود می‌کند. انتقال با
`rclone copy --immutable --checksum` انجام می‌شود و پس از آن `rclone check`
اجرا می‌شود. تا آپلود و بررسی raw موفق نشود، فایل‌های پردازش‌شده به Drive
نمی‌روند. rawهای قبلی بازنویسی یا خودکار پاک نمی‌شوند. `RCLONE_CONF` برای
این workflow الزامی است. اگر انتقال raw به Drive شکست بخورد، فایل‌های محلی
به‌عنوان artifact با نام `raw-recovery` برای ۳۰ روز نگه داشته می‌شوند.

برای بستن و بررسی قطعه‌های یک اجرای قطع‌شده:

```bash
python scripts/finalize_raw_archive.py --raw-root data/raw
```

برای دیدن درخواست‌های موجود در آرشیوی که از Drive دانلود شده:

```bash
python scripts/recover_raw_archive.py --run-dir data/raw/tradingview/DATE/RUN_ID
```

برای استخراج یک درخواست به یک پوشهٔ جدید (بدون تغییر دادهٔ اصلی):

```bash
python scripts/recover_raw_archive.py \
  --run-dir data/raw/tradingview/DATE/RUN_ID \
  --request-id r000001 --output-dir recovered/r000001
```

خروجی `frame-*.parquet` دیتافریم خام اصلی است. فایل `events.parquet` پیام‌های
ورودی و وضعیت درخواست را نگه می‌دارد تا در صورت ایراد parser بتوان آن‌ها را
دوباره پردازش کرد. ابزار بازیابی پوشهٔ موجود را بازنویسی نمی‌کند.
