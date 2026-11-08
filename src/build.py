"""Собирает один самодостаточный index.html: картинки Алисы и стартовый план встраиваются в страницу.
Запуск из корня репозитория: python src/build.py [стартовый-план.json] [выходной-файл.html]"""
import base64, json, sys, pathlib
root = pathlib.Path(__file__).resolve().parent
plan = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else root / "example-plan.json"
out = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else root.parent / "index.html"
looks = {p.stem: "data:image/webp;base64," + base64.b64encode(p.read_bytes()).decode() for p in (root / "alisa").glob("*.webp")}
html = (root / "index.src.html").read_text(encoding="utf-8")
assert "/*ALISA_DATA*/{}" in html and "/*FIRST_PLAN*/null" in html
html = html.replace("/*ALISA_DATA*/{}", json.dumps(looks)).replace("/*FIRST_PLAN*/null", json.dumps(json.loads(plan.read_text(encoding="utf-8")), ensure_ascii=False))
out.write_text(html, encoding="utf-8")
print(out, len(html) // 1024, "KB")
