from flask import Flask, request, jsonify

app = Flask(__name__)

WESTERN_ZODIAC = [
    ("Capricorn",  (12, 22), (1, 19)),
    ("Aquarius",   (1, 20),  (2, 18)),
    ("Pisces",     (2, 19),  (3, 20)),
    ("Aries",      (3, 21),  (4, 19)),
    ("Taurus",     (4, 20),  (5, 20)),
    ("Gemini",     (5, 21),  (6, 20)),
    ("Cancer",     (6, 21),  (7, 22)),
    ("Leo",        (7, 23),  (8, 22)),
    ("Virgo",      (8, 23),  (9, 22)),
    ("Libra",      (9, 23),  (10, 22)),
    ("Scorpio",    (10, 23), (11, 21)),
    ("Sagittarius",(11, 22), (12, 21)),
    ("Capricorn",  (12, 22), (12, 31)),
]

CHINESE_ZODIAC = [
    "Monkey","Rooster","Dog","Pig","Rat","Ox",
    "Tiger","Rabbit","Dragon","Snake","Horse","Goat"
]

def western_zodiac(month: int, day: int) -> str:
    for sign, (sm, sd), (em, ed) in WESTERN_ZODIAC[:-1]:
        if (month, day) >= (sm, sd) and (month, day) <= (em, ed):
            return sign
    return "Capricorn"

def chinese_zodiac(year: int) -> str:
    return CHINESE_ZODIAC[year % 12]

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Zodiac Finder</title>
<style>
  body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;max-width:720px;margin:40px auto;padding:0 16px}
  .card{border:1px solid #ddd;border-radius:12px;padding:20px;box-shadow:0 4px 16px rgba(0,0,0,.05)}
  h1{margin:0 0 12px}
  label{display:block;margin:.5rem 0 .25rem}
  input[type="text"],input[type="date"]{width:100%;padding:.6rem;border:1px solid #ccc;border-radius:8px}
  button{margin-top:12px;padding:.6rem 1rem;border:0;border-radius:8px;background:#2563eb;color:#fff;cursor:pointer}
  .result{margin-top:16px;padding:12px;border-radius:10px;background:#f9fafb;border:1px dashed #d1d5db}
  .muted{color:#6b7280;font-size:.9rem}
</style>
</head>
<body>
  <div class="card">
    <h1>🔮 Zodiac Finder</h1>
    <p class="muted">Enter your name and birthdate to see your Western and Chinese zodiac signs.</p>
    <form method="post">
      <label for="name">Name</label>
      <input id="name" name="name" type="text" required placeholder="e.g., Ani" value="{name}">
      <label for="dob">Date of birth</label>
      <input id="dob" name="dob" type="date" required value="{dob}">
      <button type="submit">Tell me my signs</button>
    </form>
    {result}
    <p class="muted">API: <code>/api/zodiac?name=Ani&dob=2000-05-12</code></p>
  </div>
</body>
</html>
"""

def render_result(name, dob, w_sign, c_sign):
    return f"""
    <div class="result">
      <strong>Hi {name}!</strong><br/>
      Western zodiac: <strong>{w_sign}</strong><br/>
      Chinese zodiac: <strong>{c_sign}</strong>
    </div>
    """

@app.route("/", methods=["GET","POST"])
def index():
    name = ""
    dob = ""
    result_html = ""
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        dob = (request.form.get("dob") or "").strip()
        try:
            y, m, d = map(int, dob.split("-"))
            w = western_zodiac(m, d)
            c = chinese_zodiac(y)
            result_html = render_result(name or "there", dob, w, c)
        except Exception:
            result_html = '<div class="result">Please enter a valid date in YYYY-MM-DD format.</div>'
    return HTML_PAGE.format(name=name, dob=dob, result=result_html)

@app.route("/api/zodiac")
def api_zodiac():
    name = (request.args.get("name") or "").strip() or "there"
    dob = request.args.get("dob") or ""
    try:
        y, m, d = map(int, dob.split("-"))
        return jsonify({
            "name": name,
            "dob": dob,
            "western": western_zodiac(m, d),
            "chinese": chinese_zodiac(y)
        })
    except Exception:
        return jsonify({"error":"Use dob=YYYY-MM-DD"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
