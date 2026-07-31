from prometheus_client import Counter, Histogram, Gauge

scrape_requests_total=Counter(
    "scrape_requests_total",
    "Total scrape attempts",
    ["platform","status"]
)
scrape_duration_seconds= Histogram(
    "scrape_duration_seconds",
    "Time taken for scrapping"
)
queue_depth=Gauge(
    "queue_depth",
    "Number of pending scrape jobs"
)