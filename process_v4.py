import re
import os
from html import unescape

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

    "import pandas as pd": "Pandas লাইব্রেরি লোড করে সংক্ষিপ্ত নাম 'pd' হিসেবে বাইন্ড করা হয়েছে",
    'df=pd.DataFrame({"name":["A","B"],"score":[80,90]})': "ডিকশনারি থেকে দুই কলাম (name, score) বিশিষ্ট Pandas DataFrame তৈরি করা হয়েছে",
    "print(df)": "সম্পূর্ণ DataFrame টেবিল ফরম্যাটে প্রিন্ট করা হয়েছে",
    'print(df["score"])': "DataFrame থেকে শুধু 'score' নামের কলামটি (Series) বের করে প্রিন্ট করা হয়েছে",
    'print(df[df["score"] >= 85])': "Boolean indexing: score ৮৫ বা তার বেশি যেসব সারি সেগুলোকে ফিল্টার করে দেখানো হয়েছে",
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

TOPIC_SECTION_COMMENTS = {
    "16-numpy.html": {
        "topic1": "TOPIC SECTION #1: Array vs Python list — NumPy array-এর সুবিধা ও ভেক্টরাইজড অপারেশন",
        "topic2": "TOPIC SECTION #2: Indexing and slicing — Multi-dimensional array থেকে ডেটা বাছাই করা",
        "topic3": "TOPIC SECTION #3: Aggregation — Mean, sum, min, max ইত্যাদি summary statistics",
        "topic4": "TOPIC SECTION #4: Masks — Boolean condition দিয়ে ডেটা ফিল্টার করা"
    },
    "17-pandas.html": {
        "topic1": "TOPIC SECTION #1: DataFrame — Pandas-এর মূল ২D টেবিল ডেটা স্ট্রাকচার",
        "topic2": "TOPIC SECTION #2: Selection — Column selection ও Boolean masking দিয়ে রো ফিল্টার",
        "topic3": "TOPIC SECTION #3: GroupBy — ক্যাটাগরি/কলাম অনুযায়ী গ্রুপ করে aggregate করা",
        "topic4": "TOPIC SECTION #4: Missing data — NaN মান হ্যান্ডেল করা (fillna/imputation)"
    },
    "18-visualization.html": {
        "topic1": "TOPIC SECTION #1: Line plot — Ordered X-axis ধরে trend দেখানোর জন্য লাইন গ্রাফ",
        "topic2": "TOPIC SECTION #2: Scatter plot — দুইটি numeric variable-এর সম্পর্ক দেখানো",
        "topic3": "TOPIC SECTION #3: Histogram — Numeric value-এর ফ্রিকোয়েন্সি বিতরণ দেখানো",
        "topic4": "TOPIC SECTION #4: Subplots — এক Figure-এ একাধিক গ্রাফ সাজানো"
    },
    "19-sql-sqlite.html": {
        "topic1": "TOPIC SECTION #1: Create a database — SQLite ফাইল + table schema তৈরি",
        "topic2": "TOPIC SECTION #2: Insert safely — Parameterized query দিয়ে SQL injection এড়ানো",
        "topic3": "TOPIC SECTION #3: Read data — SELECT query + fetchAll দিয়ে রো পড়া",
        "topic4": "TOPIC SECTION #4: CRUD mindset — UPDATE (সাথে Create Read Delete) পুরো ডাটা লাইফসাইকেল"
    },
    "20-machine-learning-foundations.html": {
        "topic1": "TOPIC SECTION #1: Features and labels — ML input (X) ও output target (y) বোঝা",
        "topic2": "TOPIC SECTION #2: Train/test split — Unseen data দিয়ে মডেল নির্ভরযোগ্যভাবে মূল্যায়ন",
        "topic3": "TOPIC SECTION #3: Regression — Continuous/numeric value predict করা (Linear Regression)",
        "topic4": "TOPIC SECTION #4: Classification — Category/class predict করা (Decision Tree)"
    },
    "21-concurrency-async.html": {
        "topic1": "TOPIC SECTION #1: I/O-bound vs CPU-bound — কাজের ধরন অনুযায়ী concurrency স্ট্র্যাটেজি বেছে নেওয়া",
        "topic2": "TOPIC SECTION #2: Async task — asyncio + async/await দিয়ে single-threaded concurrent I/O",
        "topic3": "TOPIC SECTION #3: Threading concept — ThreadPoolExecutor + GIL-friendly I/O-bound workload",
        "topic4": "TOPIC SECTION #4: Multiprocessing concept — ProcessPoolExecutor + multi-core CPU-bound parallelism"
    },
    "22-portfolio-projects.html": {
        "topic1": "TOPIC SECTION #1: CLI project — Command-line tool (function + validation + menu)",
        "topic2": "TOPIC SECTION #2: Automation project — ফাইল/ফোল্ডার ডিটেক্ট করে repeatable task করা",
        "topic3": "TOPIC SECTION #3: API project — HTTP client (requests + JSON + error handling)",
        "topic4": "TOPIC SECTION #4: Capstone architecture — ৩-টায়ার ফোল্ডার স্ট্রাকচার (UI/logic/data)"
    }
}

FILE_HEADER = {
    "16-numpy.html": "FILE: 16-numpy.html — Python Handbook অধ্যায় ১৬\n     বিষয়বস্তু: NumPy numerical computing library (arrays, indexing, aggregation, masks)\n     কাঠামো: Bangla structural comments + line-by-line Bengali explanations",
    "17-pandas.html": "FILE: 17-pandas.html — Python Handbook অধ্যায় ১৭\n     বিষয়বস্তু: Pandas data analysis (Series, DataFrame, selection, groupby, missing data)\n     কাঠামো: Bangla structural comments + line-by-line Bengali explanations",
    "18-visualization.html": "FILE: 18-visualization.html — Python Handbook অধ্যায় ১৮\n     বিষয়বস্তু: Matplotlib data visualization (line, scatter, histogram, subplots)\n     কাঠামো: Bangla structural comments + line-by-line Bengali explanations",
    "19-sql-sqlite.html": "FILE: 19-sql-sqlite.html — Python Handbook অধ্যায় ১৯\n     বিষয়বস্তু: SQL + SQLite database (CRUD, parameterized queries, Python workflow)\n     কাঠামো: Bangla structural comments + line-by-line Bengali explanations",
    "20-machine-learning-foundations.html": "FILE: 20-machine-learning-foundations.html — Python Handbook অধ্যায় ২০\n     বিষয়বস্তু: Machine Learning basics (features/labels, train-split, regression, classification)\n     কাঠামো: Bangla structural comments + line-by-line Bengali explanations",
    "21-concurrency-async.html": "FILE: 21-concurrency-async.html — Python Handbook অধ্যায় ২১\n     বিষয়বস্তু: Concurrency models (asyncio, ThreadPool, ProcessPool, I/O vs CPU bound)\n     কাঠামো: Bangla structural comments + line-by-line Bengali explanations",
    "22-portfolio-projects.html": "FILE: 22-portfolio-projects.html — Python Handbook অধ্যায় ২২\n     বিষয়বস্তু: Portfolio project ideas (CLI, automation, API client, architecture)\n     কাঠামো: Bangla structural comments + line-by-line Bengali explanations"
}


def make_comment(text, indent=0, width=75, style='='):
    edge = style * width
    pad = ' ' * indent
    lines = text.split('\n')
    result = [f'{pad}<!-- {edge}']
    for ln in lines:
        result.append(f'{pad}     {ln}')
    result.append(f'{pad}     {edge} -->')
    return '\n'.join(result)


def strip_all_traces(html):
    html = re.sub(r'<!--\s*=+\s*[\s\S]*?=+\s*-->', '', html)
    html = re.sub(r'<span class="ln-text">.*?</span>', '', html, flags=re.DOTALL)
    markers = ['TOPIC SECTION #', 'HEAD METADATA:', 'BODY START', 'TOP SCROLL PROGRESS BAR:',
               'NAVIGATION BAR:', 'MAIN READER LAYOUT:', 'ASIDE TOC SIDEBAR:',
               'ARTICLE BODY:', 'DEFINITION CALLOUT:', 'WHY CALLOUT:',
               'TIP CALLOUT:', 'CODE BLOCK:', 'LINEBOX ROWS:',
               'PRACTICE EXERCISE AREA:', 'PAGER NAVIGATION:', 'FOOTER:',
               'SCRIPT INCLUDE:', 'FILE:']
    for m in markers:
        html = re.sub(r'<!--[^<]*?' + re.escape(m) + r'[\s\S]*?-->', '', html)
    return html


def pretty_print(html_content):
    INDENT = '    '
    lines = []
    level = 0

    tokens = re.findall(r'<!--.*?-->|<[^>]+>|[^<]+', html_content, flags=re.DOTALL)
    inline_tags = {'code', 'span', 'a', 'b', 'i', 'br', 'pre'}
    preserve_ws_tags = {'code', 'pre'}
    text_buffer_preserve = False
    buffer_line = None

    i = 0
    while i < len(tokens):
        tok = tokens[i]
        s = tok.strip()
        if not s:
            i += 1
            continue

        if s.startswith('<!--'):
            clines = s.split('\n')
            for idx, c in enumerate(clines):
                cstrip = c.strip()
                if cstrip.startswith('<!--') or cstrip.endswith('-->') or cstrip.startswith('=') or idx == 0 or idx == len(clines) - 1:
                    lines.append(INDENT * level + cstrip)
                else:
                    lines.append(INDENT * level + c.rstrip())
            i += 1
            continue

        if s.startswith('</'):
            m = re.match(r'</([a-zA-Z0-9]+)', s)
            tname = m.group(1).lower() if m else ''
            level = max(0, level - 1)
            lines.append(INDENT * level + s)
            buffer_line = None
            text_buffer_preserve = False
            i += 1
            continue

        if s.startswith('<'):
            m = re.match(r'<([a-zA-Z0-9]+)', s)
            tname = m.group(1).lower() if m else ''
            is_selfclose = bool(re.match(r'<(meta|link|br|hr|img|input|!doctype)', s, re.I)) or s.endswith('/>')

            if tname in preserve_ws_tags:
                combined = [s]
                j = i + 1
                close_found = False
                while j < len(tokens):
                    nt = tokens[j].strip() if tokens[j].strip() else tokens[j]
                    combined.append(nt if isinstance(nt, str) else nt)
                    if nt.startswith(f'</{tname}'):
                        close_found = True
                        break
                    j += 1
                if close_found:
                    full = ''.join(combined)
                    if '\n' not in full[:80] or tname == 'code':
                        lines.append(INDENT * level + full.replace('\n', ' ').replace('  ', ' ').strip())
                    else:
                        lines.append(INDENT * level + s)
                    i = j + 1
                    continue

            if is_selfclose:
                lines.append(INDENT * level + s)
            elif tname in inline_tags:
                combined = [s]
                j = i + 1
                inner_has_el = False
                close_found = False
                while j < len(tokens):
                    nt = tokens[j]
                    ns = nt.strip()
                    if ns.startswith('<') and not ns.startswith('<!--') and not ns.startswith('</'):
                        inner_has_el = True
                    combined.append(nt)
                    if ns.startswith(f'</{tname}'):
                        close_found = True
                        break
                    j += 1
                if close_found and not inner_has_el:
                    full = ''.join(combined)
                    lines.append(INDENT * level + full)
                    i = j + 1
                    continue
                lines.append(INDENT * level + s)
                level += 1
            else:
                lines.append(INDENT * level + s)
                level += 1
            i += 1
            continue

        if buffer_line is not None and (tokens[i-1].strip().startswith('<code') or tokens[i-1].strip().startswith('<pre')):
            lines[-1] = (lines[-1] + s)
        else:
            for tl in s.split('\n'):
                ts = tl.strip()
                if ts:
                    lines.append(INDENT * level + ts)
        i += 1

    return '\n'.join(lines)


def add_ln_text(html):
    result = html
    for code_line, explanation in LN_TEXT_MAP.items():
        esc = re.escape(code_line)
        pat = r'(<div>\s*<code>\s*)(' + esc + r')(\s*</code>)(\s*</div>)'
        rep = r'\1\2\3<span class="ln-text">' + explanation + r'</span>\4'
        result = re.sub(pat, rep, result)
    return result


def add_all_comments(html, filename):
    r = html

    if filename in FILE_HEADER:
        comment_block = make_comment(FILE_HEADER[filename], indent=0, style='=', width=75)
        r = re.sub(r'(<!doctype html>)', comment_block + '\n' + r'\1', r, count=1, flags=re.I)

    r = re.sub(
        r'(\n\s*<head>)',
        lambda m: m.group(1) + '\n' + make_comment(
            'HEAD METADATA: Document title, charset, viewport, stylesheet attachment',
            indent=8, style='-', width=57
        ),
        r, count=1
    )

    r = re.sub(
        r'(\n\s*<body>)',
        lambda m: m.group(1) + '\n' + make_comment(
            'BODY START\nTOP SCROLL PROGRESS BAR: .top i element width যতখানি scroll ততখানি বাড়ে (app.js দেখুন)',
            indent=4, style='-', width=70
        ),
        r, count=1
    )

    r = re.sub(
        r'(\n\s*<nav>)',
        lambda m: '\n' + make_comment(
            'NAVIGATION BAR: brand logo + Home/Contents লিংকসমূহ',
            indent=4, style='-', width=70
        ) + m.group(1),
        r, count=1
    )

    r = re.sub(
        r'(\n\s*<main class="wrap reader">)',
        lambda m: '\n' + make_comment(
            'MAIN READER LAYOUT: ২-কলাম (TOC sidebar + article content) flex/grid wrapper',
            indent=4, style='-', width=70
        ) + m.group(1),
        r, count=1
    )

    r = re.sub(
        r'(\n\s*<aside class="toc">)',
        lambda m: '\n' + make_comment(
            'ASIDE TOC SIDEBAR: এখানে Chapter-এর সব heading-এর anchor লিংক আছে\n(Scroll spy: app.js দিয়ে active link highlight হয়)',
            indent=8, style='-', width=60
        ) + m.group(1),
        r, count=1
    )

    r = re.sub(
        r'(\n\s*<article class="article">)',
        lambda m: '\n' + make_comment(
            'ARTICLE BODY: Chapter-এর মূল কনটেন্ট (kicker, h1, lead, topics, practice, pager)',
            indent=8, style='-', width=60
        ) + m.group(1),
        r, count=1
    )

    topics = TOPIC_SECTION_COMMENTS.get(filename, {})
    for tid, txt in topics.items():
        pat = r'(\n\s*<section>\s*\n\s*<h2 id="' + re.escape(tid) + r'">)'
        if not re.search(pat, r):
            pat = r'(\n\s*<section>\s*<h2 id="' + re.escape(tid) + r'">)'
        if re.search(pat, r):
            cmt = make_comment(txt, indent=8, style='-', width=62)
            r = re.sub(pat, '\n' + cmt + r'\1', r, count=1)

    r = re.sub(
        r'(\n\s*<div class="code">)',
        lambda m: m.group(1).split('\n')[0] + '\n' + (
            ' ' * (len(m.group(1)) - len(m.group(1).lstrip('\n')))
        ).replace('\n', '') + '            ' +
        '<!-- CODE BLOCK: Copy বাটন + <pre><code> syntax highlight area -->',
        r
    )
    r = re.sub(
        r'\n(\s*)<div class="code">',
        lambda m: f'\n{m.group(1)}<!-- CODE BLOCK: Copy বাটন + <pre><code> syntax highlight area -->\n{m.group(1)}<div class="code">',
        r
    )

    r = re.sub(
        r'\n(\s*)<div class="definition">',
        lambda m: f'\n{m.group(1)}<!-- DEFINITION CALLOUT: সহজ ভাষায় concept-এর সংক্ষিপ্ত ব্যাখ্যা -->\n{m.group(1)}<div class="definition">',
        r
    )
    r = re.sub(
        r'\n(\s*)<div class="why">',
        lambda m: f'\n{m.group(1)}<!-- WHY CALLOUT: কেন codeটি কাজ করছে — underlying mechanism ব্যাখ্যা -->\n{m.group(1)}<div class="why">',
        r
    )
    r = re.sub(
        r'\n(\s*)<div class="tip">',
        lambda m: f'\n{m.group(1)}<!-- TIP CALLOUT: Self-study guide / hands-on experiment নির্দেশনা -->\n{m.group(1)}<div class="tip">',
        r
    )
    r = re.sub(
        r'\n(\s*)<div class="linebox">',
        lambda m: f'\n{m.group(1)}<!-- LINEBOX ROWS: প্রতিটি line-র জন্য code + Bangla explanation (ln-text) -->\n{m.group(1)}<div class="linebox">',
        r
    )

    r = re.sub(
        r'(\n\s*<h2 id="practice">Practice Lab</h2>)',
        lambda m: '\n' + make_comment(
            'PRACTICE EXERCISE AREA: ৩টি difficulty level — Beginner/Intermediate/Challenge',
            indent=8, style='-', width=60
        ) + m.group(1),
        r, count=1
    )

    r = re.sub(
        r'(\n\s*<div class="pager">)',
        lambda m: '\n' + make_comment(
            'PAGER NAVIGATION: Previous chapter + Colab link + Next chapter বাটন',
            indent=8, style='-', width=60
        ) + m.group(1),
        r, count=1
    )

    r = re.sub(
        r'(\n\s*<footer class="footer">)',
        lambda m: '\n' + make_comment(
            'FOOTER: Copyright + learning reference credits',
            indent=4, style='-', width=70
        ) + m.group(1),
        r, count=1
    )

    r = re.sub(
        r'(\n\s*<script src="\.\./assets/app\.js"></script>)',
        lambda m: '\n' + make_comment(
            'SCRIPT INCLUDE: Interactive logic (scroll bar, copy button, TOC spy)',
            indent=4, style='-', width=70
        ) + m.group(1),
        r, count=1
    )

    return r


def cleanup_whitespace(html):
    lines = html.split('\n')
    out = []
    prev_blank = False
    for ln in lines:
        if ln.strip() == '':
            if not prev_blank:
                out.append('')
            prev_blank = True
        else:
            out.append(ln)
            prev_blank = False
    return '\n'.join(out)


def process_file(filepath, filename):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    s1 = strip_all_traces(content)
    s2 = pretty_print(s1)
    s3 = add_ln_text(s2)
    s4 = add_all_comments(s3, filename)
    s5 = cleanup_whitespace(s4)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(s5)

    print(f"[OK] V4: {filename}")


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
            process_file(fp, fn)
        except Exception as e:
            print(f"[ERROR] {fn}: {e}")
            import traceback
            traceback.print_exc()
