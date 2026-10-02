import re
import os
from html import unescape, escape

LN_TEXT_MAP = {
    "import numpy as np": "NumPy লাইব্রেরি লোড করে সংক্ষিপ্ত নাম 'np' হিসেবে বাইন্ড করা হয়েছে",
    "a=np.array([1,2,3])": "Python list [1,2,3] থেকে ১D NumPy array তৈরি করে ভেরিয়েবল 'a'-এ সংরক্ষণ করা হয়েছে",
    "print(a*2)": "Vectorized multiplication: array 'a'-র প্রতিটি উপাদানকে ২ দ্বারা গুণ করে প্রিন্ট করা হয়েছে",
    "a=np.arange(12).reshape(3,4)": "০-১১ পর্যন্ত সংখ্যার ১D array তৈরি করে ৩x৪ মাত্রার ২D matrix-এ রূপান্তরিত করা হয়েছে",
    "print(a[1,2])": "২D array-এর ২য় সারি (index ১) ও ৩য় কলাম (index ২) এর উপাদান প্রিন্ট করা হয়েছে",
    "print(a[:,1])": "সব সারি থেকে শুধু ২য় কলাম (index ১) এর সকল উপাদান একত্রে প্রিন্ট করা হয়েছে",
    "a=np.array([10,20,30,40])": "[10,20,30,40] মান দিয়ে একটি নতুন ১D NumPy array তৈরি করা হয়েছে",
    "print(a.mean(), a.sum(), a.max())": "array-এর গড় মান, মোট যোগফল ও সর্বোচ্চ মান একসাথে প্রিন্ট করা হয়েছে",
    "a=np.array([10,15,20,25])": "[10,15,20,25] মানসমূহ দিয়ে ১D NumPy array তৈরি করা হয়েছে",
    "print(a[a >= 20])": "Boolean mask দিয়ে ২০ বা তার বেশি মানবিশিষ্ট উপাদানগুলোকে ফিল্টার করে প্রিন্ট করা হয়েছে",
    "print(a[a &gt;= 20])": "Boolean mask দিয়ে ২০ বা তার বেশি মানবিশিষ্ট উপাদানগুলোকে ফিল্টার করে প্রিন্ট করা হয়েছে",

    "import pandas as pd": "Pandas লাইব্রেরি লোড করে সংক্ষিপ্ত নাম 'pd' হিসেবে বাইন্ড করা হয়েছে",
    'df=pd.DataFrame({"name":["A","B"],"score":[80,90]})': "ডিকশনারি থেকে দুই কলাম (name, score) বিশিষ্ট Pandas DataFrame তৈরি করা হয়েছে",
    "print(df)": "সম্পূর্ণ DataFrame টেবিল ফরম্যাটে প্রিন্ট করা হয়েছে",
    'print(df["score"])': "DataFrame থেকে শুধু 'score' নামের কলামটি (Series) বের করে প্রিন্ট করা হয়েছে",
    'print(df[df["score"] >= 85])': "Boolean indexing: score ৮৫ বা তার বেশি যেসব সারি সেগুলোকে ফিল্টার করে দেখানো হয়েছে",
    'print(df[df["score"] &gt;= 85])': "Boolean indexing: score ৮৫ বা তার বেশি যেসব সারি সেগুলোকে ফিল্টার করে দেখানো হয়েছে",
    'df=pd.DataFrame({"dept":["CSE","CSE","EEE"],"score":[80,90,70]})': "dept ও score কলামসহ নতুন DataFrame তৈরি করা হয়েছে",
    'print(df.groupby("dept")["score"].mean())': "dept অনুযায়ী গ্রুপ করে প্রতিটি বিভাগের score-র গড় মান বের করে প্রিন্ট করা হয়েছে",
    "df=df.fillna(0)": "DataFrame-এর সব missing (NaN) মানকে ০ দ্বারা প্রতিস্থাপন করা হয়েছে",

    "import matplotlib.pyplot as plt": "Matplotlib-এর pyplot মডিউল লোড করে 'plt' নামে বাইন্ড করা হয়েছে",
    "plt.plot([1,2,3,4],[2,4,3,6])": "x=[1,2,3,4], y=[2,4,3,6] ডেটা দিয়ে লাইন প্লট আঁকা হয়েছে",
    'plt.xlabel("Day")': "X-অক্ষের নাম 'Day' সেট করা হয়েছে",
    'plt.ylabel("Value")': "Y-অক্ষের নাম 'Value' সেট করা হয়েছে",
    "plt.show()": "তৈরি করা গ্রাফটি উইন্ডোতে প্রদর্শন করা হয়েছে",
    "plt.scatter([1,2,3,4],[2,5,3,7])": "x ও y ডেটা দিয়ে বিন্দু বিন্দু আকারে স্ক্যাটার প্লট আঁকা হয়েছে",
    'plt.xlabel("X")': "X-অক্ষের লেবেল 'X' সেট করা হয়েছে",
    'plt.ylabel("Y")': "Y-অক্ষের লেবেল 'Y' সেট করা হয়েছে",
    "plt.hist([1,2,2,3,3,3,4,5], bins=5)": "ডেটার ফ্রিকোয়েন্সি বিতরণ ৫টি bin-এ ভাগ করে হিস্টোগ্রাম আঁকা হয়েছে",
    'plt.xlabel("Value")': "X-অক্ষে মান/Value লেবেল সেট করা হয়েছে",
    'plt.ylabel("Frequency")': "Y-অক্ষে ফ্রিকোয়েন্সি/বারবারি লেবেল সেট করা হয়েছে",
    "fig,ax=plt.subplots(1,2)": "১ সারি × ২ কলামের দুটি সাবপ্লট (axes) সহ একটি figure তৈরি করা হয়েছে",
    "ax[0].plot([1,2,3],[2,4,3])": "প্রথম সাবপ্লটে (বাম) লাইন প্লট আঁকা হয়েছে",
    "ax[1].scatter([1,2,3],[3,1,4])": "দ্বিতীয় সাবপ্লটে (ডান) স্ক্যাটার প্লট আঁকা হয়েছে",

    "import sqlite3": "Python-এর বিল্ট-ইন SQLite3 ডাটাবেস মডিউল লোড করা হয়েছে",
    'con=sqlite3.connect("app.db")': "app.db নামের লোকাল ডাটাবেস ফাইলের সাথে কানেকশন স্থাপন করা হয়েছে",
    "cur=con.cursor()": "SQL query চালানোর জন্য কানেকশন থেকে cursor অবজেক্ট তৈরি করা হয়েছে",
    'cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,name TEXT)")': "users টেবিল না থাকলে id (primary key) ও name কলামসহ তৈরি করা হয়েছে",
    "con.commit()": "কানেকশনের সব pending পরিবর্তনকে স্থায়ীভাবে ডাটাবেসে সংরক্ষণ করা হয়েছে",
    'cur.execute("INSERT INTO users(name) VALUES (?)", ("Renco",))': "Parameterized query দিয়ে users টেবিলে নতুন রো যোগ করা হয়েছে (SQL injection প্রতিরোধ)",
    'rows=cur.execute("SELECT id,name FROM users").fetchall()': "users টেবিল থেকে সব রো SELECT করে rows হিসেবে fetchAll করা হয়েছে",
    "print(rows)": "fetch করা সব রো (tuple-এর list) প্রিন্ট করা হয়েছে",
    'cur.execute("UPDATE users SET name=? WHERE id=?", ("Mahadi",1))': "id=১ য়েসব রো আছে তাদের name কে 'Mahadi' তে আপডেট করা হয়েছে",

    "X=[[1],[2],[3],[4]]": "Features ম্যাট্রিক্স: ৪টি স্যাম্পল, প্রত্যেকটিতে ১টি ফিচার (2D shape required by scikit-learn)",
    "y=[2,4,6,8]": "Target/labels: প্রতিটি ফিচার স্যাম্পলের সাথে সম্পর্কিত লেবেল মান (1D array)",
    "from sklearn.model_selection import train_test_split": "scikit-learn থেকে train/test split ফাংশন import করা হয়েছে",
    "X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.25,random_state=42)": "ডেটাকে ৭৫% train ও ২৫% test সেটে split করা হয়েছে (reproducible random_state)",
    "from sklearn.linear_model import LinearRegression": "scikit-learn থেকে LinearRegression মডেল ক্লাস import করা হয়েছে",
    "model=LinearRegression().fit(X_train,y_train)": "Linear Regression মডেল ইনিশিয়ালাইজ করে train ডেটা ওপর fit করা হয়েছে",
    "print(model.predict(X_test))": "Trained মডেল দিয়ে unseen test ডেটার prediction বের করে প্রিন্ট করা হয়েছে",
    "from sklearn.tree import DecisionTreeClassifier": "scikit-learn থেকে Decision Tree Classifier মডেল import করা হয়েছে",
    "model=DecisionTreeClassifier(random_state=42)": "ডিসিশন ট্রি ক্লাসিফায়ার মডেল তৈরি করা হয়েছে (নির্দিষ্ট random_state)",
    'model.fit([[0],[1],[2],[3]],["low","low","high","high"])': "মডেলকে (X features, y categories) দিয়ে train করা হয়েছে",
    'print(model.predict([[2.5]]))': "নতুন input [[2.5]] এর জন্য category (low/high) predict করে প্রিন্ট করা হয়েছে",

    "import time": "Python time মডিউল লোড করা হয়েছে (sleep, timestamp ইত্যাদি জন্য)",
    'print("Start")': "কনসোলে 'Start' টেক্সট প্রিন্ট করা হয়েছে (প্রোগ্রাম শুরু হওয়ার সংকেত)",
    "time.sleep(1)": "প্রোগ্রামকে ১ সেকেন্ডের জন্য ব্লক করে অপেক্ষা করানো হয়েছে (I/O wait simulation)",
    'print("Done")': "শেষে 'Done' প্রিন্ট করা হয়েছে (sleep শেষ হওয়ার পর)",
    "import asyncio": "Python asyncio লাইব্রেরি লোড করা হয়েছে (async/await coroutine সম্পাদনের জন্য)",
    "async def task(name):": "'task' নামে async coroutine ফাংশন ডিফাইন করা হয়েছে যা 'name' প্যারামিটার নেয়",
    "    await asyncio.sleep(1)": "১ সেকেন্ডের non-blocking sleep (ঐ সময়ে event loop অন্য task চালাতে পারে)",
    "    print(name)": "await শেষ হওয়ার পর বর্তমান task-এর নাম প্রিন্ট করা হয়েছে",
    "async def main():": "'main' নামে top-level async coroutine ডিফাইন করা হয়েছে",
    '    await asyncio.gather(task("A"),task("B"))': "দুটি coroutine একসাথে schedule করা হয়েছে যাতে তাদের sleep period overlap করে",
    "asyncio.run(main())": "asyncio event loop শুরু করে main coroutine চালানো হয়েছে",
    "from concurrent.futures import ThreadPoolExecutor": "concurrent.futures থেকে ThreadPoolExecutor import করা হয়েছে (thread pool-based concurrency)",
    "with ThreadPoolExecutor(max_workers=2) as ex:": "২টি worker thread থেকে thread pool তৈরি করা হয়েছে (context manager দিয়ে স্বয়ংক্রিয় cleanup)",
    '    print(list(ex.map(lambda x:x*x,[1,2,3])))': "pool-এর threads-এ [1,2,3] এর স্কয়ার ক্যালকুলেশন ডিসট্রিবিউট করে results list হিসেবে প্রিন্ট করা হয়েছে",
    "from concurrent.futures import ProcessPoolExecutor": "concurrent.futures থেকে ProcessPoolExecutor import করা হয়েছে (separate processes, multi-core)",
    "with ProcessPoolExecutor() as ex:": "CPU-core সংখ্যা অনুযায়ী worker process দিয়ে Process Pool তৈরি করা হয়েছে",
    '    print(list(ex.map(lambda x:x*x,[1,2,3])))': "প্রতিটি process-এ স্কয়ার ক্যালকুলেশন dispatch করে parallel execution-এর results list প্রিন্ট করা হয়েছে",

    "def add(a,b): return a+b": "a ও b দুইটি প্যারামিটারের যোগফল রিটার্ন করে এমন ছোট helper function ডিফাইন করা হয়েছে",
    "print(add(10,20))": "add() ফাংশনকে ১০ ও ২০ আর্গুমেন্ট দিয়ে call করে result ৩০ প্রিন্ট করা হয়েছে",
    "from pathlib import Path": "pathlib থেকে OOP-style file path handler 'Path' ক্লাস import করা হয়েছে",
    'for p in Path(".").glob("*.txt"):': "বর্তমান directory (.) থেকে সব .txt ফাইলগুলোকে glob করে loop চালানো হয়েছে",
    "    print(p.name)": "প্রতিটি .txt ফাইলের শুধু filename (path না দিয়ে) প্রিন্ট করা হয়েছে",
    "import requests": "HTTP request করার জন্য জনপ্রিয় 'requests' লাইব্রেরি লোড করা হয়েছে",
    'r=requests.get("https://api.github.com",timeout=10)': "GitHub API-তে GET request পাঠানো হয়েছে (১০ সেকেন্ড timeout সহ)",
    "r.raise_for_status()": "যদি HTTP status ৪xx/5xx হয় তাহলে Exception raise করবে (error handling-র প্রথম ধাপ)",
    "print(r.json())": "Response body-কে JSON থেকে Python dict/list-এ parse করে প্রিন্ট করা হয়েছে",
    "project/": "Portfolio project-এর root directory নাম",
    "  app/": "সব application source code রাখার জন্য app সাব-ডিরেক্টরি",
    "    main.py": "প্রোগ্রামের এন্ট্রি পয়েন্ট (CLI/menu/UI code এখানে থাকবে)",
    "    services.py": "ব্যবসায়িক নীতি/লজিক থাকে (business logic layer)",
    "    storage.py": "ডাটাবেস/ফাইল read-write operations থাকে (data access layer)",
    "  tests/": "পুরো অ্যাপের unit/integration test রাখার directory",
    "  README.md": "প্রজেক্টের বিবরণ, setup guide ও usage নথি (Markdown format)"
}


def remove_dupes_by_line(html):
    lines = html.split('\n')
    result = []
    seen_topic_comments = set()
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if s.startswith('<!--') and '-----' in s and ('TOPIC SECTION #' in s or i + 2 < len(lines) and 'TOPIC SECTION #' in lines[i+2]):
            block_start = i
            block_lines = [lines[i]]
            j = i + 1
            while j < len(lines):
                block_lines.append(lines[j])
                if lines[j].strip().endswith('-->'):
                    break
                j += 1
            block_text = '\n'.join(block_lines)
            if block_text in seen_topic_comments:
                i = j + 1
                continue
            seen_topic_comments.add(block_text)
            result.extend(block_lines)
            i = j + 1
            continue
        result.append(lines[i])
        i += 1
    return '\n'.join(result)


def add_missing_ln_text(html):
    for code_line, explanation in LN_TEXT_MAP.items():
        for line_prefix, line_suffix in [
            (r'(<code>\s*)', r'(\s*</code>)(\s*</div>)'),
            (r'(<code>\s*)', r'(\s*</code>)'),
        ]:
            esc = re.escape(code_line)
            pat = line_prefix + esc + line_suffix
            if r'\s*</div>' in line_suffix:
                full_pat = pat
                if not re.search(full_pat, html):
                    continue
                if 'class="ln-text"' in html and re.search(line_prefix + esc + r'(\s*</code>)\s*<span class="ln-text">', html):
                    continue
                rep = r'\1' + code_line + r'\2<span class="ln-text">' + explanation + r'</span>\3'
                html = re.sub(full_pat, rep, html)
            else:
                full_pat2 = line_prefix + esc + line_suffix
                html = re.sub(full_pat2, lambda m, e=explanation: m.group(0) + f'<span class="ln-text">{e}</span>' if '</code>' in m.group(0) and 'ln-text' not in m.group(0) else m.group(0), html)
    return html


def add_ln_text_simple(html):
    lines = html.split('\n')
    result = []
    for ln in lines:
        stripped = ln.strip()
        if stripped.startswith('<code>') and stripped.endswith('</code>'):
            code_content = stripped[len('<code>'):-len('</code>')]
            code_content_stripped = code_content.strip()
            uc = unescape(code_content_stripped)
            match_text = None
            for k, v in LN_TEXT_MAP.items():
                if code_content_stripped == k or uc == k or unescape(k) == uc or escape(k).replace('&quot;', '"').replace('&#x27;', "'") == code_content_stripped:
                    match_text = v
                    break
            if match_text and 'ln-text' not in ln:
                indent = len(ln) - len(ln.lstrip())
                result.append(' ' * indent + stripped + f'<span class="ln-text">{match_text}</span>')
                continue
        elif '<code>' in stripped and '</code>' in stripped and 'ln-text' not in stripped and stripped.startswith('<code>') and not stripped.endswith('</code></div>'):
            m = re.search(r'<code>\s*(.*?)\s*</code>(\s*<span)?', stripped)
            if m and m.group(2) is None:
                cc = m.group(1).strip()
                uc = unescape(cc)
                for k, v in LN_TEXT_MAP.items():
                    if cc == k or uc == k or unescape(k) == uc:
                        old_close = '</code>'
                        idx = ln.rfind(old_close)
                        if idx != -1:
                            new_ln = ln[:idx] + old_close + f'<span class="ln-text">{v}</span>' + ln[idx + len(old_close):]
                            ln = new_ln
                            break
        result.append(ln)
    return '\n'.join(result)


def fix_missing_code_div(html):
    lines = html.split('\n')
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if '<!-- CODE BLOCK:' in stripped:
            comment_line = line
            comment_indent = len(line) - len(line.lstrip())
            result.append(line)
            i += 1
            while i < len(lines) and lines[i].strip() == '':
                result.append(lines[i])
                i += 1
            if i < len(lines) and '<button class="copy">' in lines[i]:
                btn_indent = len(lines[i]) - len(lines[i].lstrip())
                div_indent = comment_indent
                result.append(' ' * div_indent + '<div class="code">')
            continue

        if stripped == '</pre>' and i + 1 < len(lines) and lines[i + 1].strip().startswith('</div>'):
            j = i + 1
            while j < len(lines) and lines[j].strip() == '':
                j += 1
            result.append(line)
            i += 1
            continue

        result.append(line)
        i += 1

    result2 = []
    for idx, line in enumerate(result):
        s = line.strip()
        if s == '</pre>':
            j = idx + 1
            while j < len(result) and result[j].strip() == '':
                j += 1
            if j < len(result) and result[j].strip().startswith('<h3'):
                div_indent = len(line) - len(line.lstrip()) - 4
                result2.append(line)
                result2.append(' ' * (div_indent + 4) + '</pre>')
                result2.append(' ' * div_indent + '</div>')
                continue
        result2.append(line)
    return '\n'.join(result2)


def cleanup_dupes_all(html):
    lines = html.split('\n')
    result = []
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if s.startswith('<!--') and '=====' in s:
            block = [lines[i]]
            j = i + 1
            while j < len(lines):
                block.append(lines[j])
                if '-->' in lines[j] and ('=====' in lines[j] or '-----' in lines[j]):
                    break
                j += 1
            block_str = '\n'.join(block)
            is_dup = False
            check_start = max(0, len(result) - len(block) - 5)
            existing = '\n'.join(result[check_start:])
            if block_str in existing:
                is_dup = True
            if not is_dup:
                result.extend(block)
            i = j + 1
            continue
        result.append(lines[i])
        i += 1
    return '\n'.join(result)


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    s1 = cleanup_dupes_all(content)
    s2 = fix_missing_code_div(s1)
    s3 = add_ln_text_simple(s2)
    s4 = add_missing_ln_text(s3)

    lines = s4.split('\n')
    out = []
    prev_empty = False
    for ln in lines:
        if ln.strip() == '':
            if not prev_empty:
                out.append('')
            prev_empty = True
        else:
            out.append(ln)
            prev_empty = False
    s5 = '\n'.join(out)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(s5)

    fn = os.path.basename(filepath)
    print(f"[OK] V5: {fn}")


if __name__ == "__main__":
    base_dir = r"c:\Users\Mr  Alien\Downloads\python-handbook\chapters"
    files = [
        "16-numpy.html",
        "17-pandas.html",
        "18-visualization.html",
        "19-sql-sqlite.html",
        "20-machine-learning-foundations.html",
        "21-concurrency-async.html",
        "22-portfolio-projects.html",
    ]
    for fn in files:
        fp = os.path.join(base_dir, fn)
        try:
            process_file(fp)
        except Exception as e:
            print(f"[ERROR] {fn}: {e}")
            import traceback
            traceback.print_exc()
