import json

# 1. Load template.html
with open('/Users/franciscomateus/Documents/DashboardUMB/template.html', 'r', encoding='utf-8') as f:
    template = f.read()

# 2. Load processed_metrics.json
with open('/Users/franciscomateus/Documents/DashboardUMB/processed_metrics.json', 'r', encoding='utf-8') as f:
    metrics = json.load(f)

# 3. Replace __DATA_JSON__ with JSON string
compiled_html = template.replace('__DATA_JSON__', json.dumps(metrics, ensure_ascii=False))

# 4. Write index.html
with open('/Users/franciscomateus/Documents/DashboardUMB/index.html', 'w', encoding='utf-8') as f:
    f.write(compiled_html)

print("index.html compiled successfully! File size:", len(compiled_html), "bytes.")
