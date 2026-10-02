import re
import sys
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
    "df=pd.DataFrame({\"name\":[\"A\",\"B\"],\"score\":[80,90]})": "ডিকশনারি থেকে দুই কলাম (name, score) বিশিষ্ট Pandas DataFrame তৈরি করা হয়েছে",
    "print(df)": "সম্পূর্ণ DataFrame টেবিল ফরম্যাটে প্রিন্ট করা হয়েছে",
    "print(df[\"score\"])": "DataFrame থেকে শুধু 'score' নামের কলামটি (Series) বের করে প্রিন্ট করা হয়েছে",
    "print(df[df[\"score\"] >= 85])": "Boolean indexing: score ৮৫ বা তার বেশি যেসব সারি সেগুলোকে ফিল্টার করে দেখানো হয়েছে",
    "df=pd.DataFrame({\"dept\":[\"CSE\",\"CSE\",\"EEE\"],\"score\":[80,90,70]})": "dept ও score কলামসহ নতুন DataFrame তৈরি করা হয়েছে",
    "print(df.groupby(\"dept\")[\"score\"].mean())": "dept অনুযায়ী গ্রুপ করে প্রতিটি বিভাগের score-র গড় মান বের করে প্রিন্ট করা হয়েছে",
    "df=df.fillna(0)": "DataFrame-এর সব missing (NaN) মানকে ০ দ্বারা প্রতিস্থাপন করা হয়েছে",

    "import matplotlib.pyplot as plt": "Matplotlib-এর pyplot মডিউল লোড করে 'plt' নামে বাইন্ড করা হয়েছে",
    "plt.plot([1,2,3,4],[2,4,3,6])": "x=[1,2,3,4], y=[2,4,3,6] ডেটা দিয়ে লাইন প্লট আঁকা হয়েছে",
    "plt.xlabel(\"Day\")": "X-অক্ষের নাম 'Day' সেট করা হয়েছে",
    "plt.ylabel(\"Value\")": "Y-অক্ষের নাম 'Value' সেট করা হয়েছে",
    "plt.show()": "তৈরি করা গ্রাফটি উইন্ডোতে প্রদর্শন করা হয়েছে",
    "plt.scatter([1,2,3,4],[2,5,3,7])": "x ও y ডেটা দিয়ে বিন্দু বিন্দু আকারে স্ক্যাটার প্লট আঁকা হয়েছে",
    "plt.xlabel(\"X\")": "X-অক্ষের লেবেল 'X' সেট করা হয়েছে",
    "plt.ylabel(\"Y\")": "Y-অক্ষের লেবেল 'Y' সেট করা হয়েছে",
    "plt.hist([1,2,2,3,3,3,4,5], bins=5)": "ডেটার ফ্রিকোয়েন্সি বিতরণ ৫টি bin-এ ভাগ করে হিস্টোগ্রাম আঁকা হয়েছে",
    "plt.xlabel(\"Value\")": "X-অক্ষে মান/Value লেবেল সেট করা হয়েছে",
    "plt.ylabel(\"Frequency\")": "Y-অক্ষে ফ্রিকোয়েন্সি/বারবারি লেবেল সেট করা হয়েছে",
    "fig,ax=plt.subplots(১,2)": "১ সারি × ২ কলামের দুটি সাবপ্লট (axes) সহ একটি figure তৈরি করা হয়েছে",
    "ax[0].plot([1,2,3],[2,4,3])": "প্রথম সাবপ্লটে (বাম) লাইন প্লট আঁকা হয়েছে",
    "ax[1].scatter([1,2,3],[3,1,4])": "দ্বিতীয় সাবপ্লটে (ডান) স্ক্যাটার প্লট আঁকা হয়েছে",

    "import sqlite3": "Python-এর বিল্ট-ইন SQLite3 ডাটাবেস মডিউল লোড করা হয়েছে",
    "con=sqlite3.connect(\"app.db\")": "app.db নামের লোকাল ডাটাবেস ফাইলের সাথে কানেকশন স্থাপন করা হয়েছে",
    "cur=con.cursor()": "SQL query চালানোর জন্য কানেকশন থেকে cursor অবজেক্ট তৈরি করা হয়েছে",
    "cur.execute(\"CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,name TEXT)\")": "users টেবিল না থাকলে id (primary key) ও name কলামসহ তৈরি করা হয়েছে",
    "con.commit()": "কানেকশনের সব pending পরিবর্তনকে স্থায়ীভাবে ডাটাবেসে সংরক্ষণ করা হয়েছে",
    "cur.execute(\"INSERT INTO users(name) VALUES (?)\", (\"Renco\",))": "Parameterized query দিয়ে users টেবিলে নতুন রো যোগ করা হয়েছে (SQL injection প্রতিরোধ)",
    "rows=cur.execute(\"SELECT id,name FROM users\").fetchall()": "users টেবিল থেকে সব রো SELECT করে rows হিসেবে fetchAll করা হয়েছে",
    "print(rows)": "fetch করা সব রো (tuple-এর list) প্রিন্ট করা হয়েছে",
    "cur.execute(\"UPDATE users SET name=? WHERE id=?\", (\"Mahadi\",1))": "id=১ য়েসব রো আছে তাদের name কে 'Mahadi' তে আপডেট করা হয়েছে",

    "X=[[1],[2],[3],[4]]": "Features ম্যাট্রিক্স: ৪টি স্যাম্পল, প্রত্যেকটিতে ১টি ফিচার (2D shape required by scikit-learn)",
    "y=[2,4,6,8]": "Target/labels: প্রতিটি ফিচার স্যাম্পলের সাথে সম্পর্কিত লেবেল মান (1D array)",
    "from sklearn.model_selection import train_test_split": "scikit-learn থেকে train/test split ফাংশন import করা হয়েছে",
    "X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.25,random_state=42)": "ডেটাকে ৭৫% train ও ২৫% test সেটে split করা হয়েছে (reproducible random_state)",
    "from sklearn.linear_model import LinearRegression": "scikit-learn থেকে LinearRegression মডেল ক্লাস import করা হয়েছে",
    "model=LinearRegression().fit(X_train,y_train)": "Linear Regression মডেল ইনিশিয়ালাইজ করে train ডেটা ওপর fit করা হয়েছে",
    "print(model.predict(X_test))": "Trained মডেল দিয়ে unseen test ডেটার prediction বের করে প্রিন্ট করা হয়েছে",
    "from sklearn.tree import DecisionTreeClassifier": "scikit-learn থেকে Decision Tree Classifier মডেল import করা হয়েছে",
    "model=DecisionTreeClassifier(random_state=42)": "ডিসিশন ট্রি ক্লাসিফায়ার মডেল তৈরি করা হয়েছে (নির্দিষ্ট random_state)",
    "model.fit([[0],[1],[2],[3]],[\"low\",\"low\",\"high\",\"high\"])": "মডেলকে (X features, y categories) দিয়ে train করা হয়েছে",
    "print(model.predict([[2.5]]))": "নতুন input [[2.5]] এর জন্য category (low/high) predict করে প্রিন্ট করা হয়েছে",

    "import time": "Python time মডিউল লোড করা হয়েছে (sleep, timestamp ইত্যাদি জন্য)",
    "print(\"Start\")": "কনসোলে 'Start' টেক্সট প্রিন্ট করা হয়েছে (প্রোগ্রাম শুরু হওয়ার সংকেত)",
    "time.sleep(1)": "প্রোগ্রামকে ১ সেকেন্ডের জন্য ব্লক করে অপেক্ষা করানো হয়েছে (I/O wait simulation)",
    "print(\"Done\")": "শেষে 'Done' প্রিন্ট করা হয়েছে (sleep শেষ হওয়ার পর)",
    "import asyncio": "Python asyncio লাইব্রেরি লোড করা হয়েছে (async/await coroutine সম্পাদনের জন্য)",
    "async def task(name):": "'task' নামে async coroutine ফাংশন ডিফাইন করা হয়েছে যা 'name' প্যারামিটার নেয়",
    "    await asyncio.sleep(1)": "১ সেকেন্ডের non-blocking sleep (ঐ সময়ে event loop অন্য task চালাতে পারে)",
    "    print(name)": "await শেষ হওয়ার পর বর্তমান task-এর নাম প্রিন্ট করা হয়েছে",
    "async def main():": "'main' নামে top-level async coroutine ডিফাইন করা হয়েছে",
    "    await asyncio.gather(task(\"A\"),task(\"B\"))": "দুটি coroutine একসাথে schedule করা হয়েছে যাতে তাদের sleep period overlap করে",
    "asyncio.run(main())": "asyncio event loop শুরু করে main coroutine চালানো হয়েছে",
    "from concurrent.futures import ThreadPoolExecutor": "concurrent.futures থেকে ThreadPoolExecutor import করা হয়েছে (thread pool-based concurrency)",
    "with ThreadPoolExecutor(max_workers=2) as ex:": "২টি worker thread থেকে thread pool তৈরি করা হয়েছে (context manager দিয়ে স্বয়ংক্রিয় cleanup)",
    "    print(list(ex.map(lambda x:x*x,[1,2,3])))": "pool-এর threads-এ [1,2,3] এর স্কয়ার ক্যালকুলেশন ডিসট্রিবিউট করে results list হিসেবে প্রিন্ট করা হয়েছে",
    "from concurrent.futures import ProcessPoolExecutor": "concurrent.futures থেকে ProcessPoolExecutor import করা হয়েছে (separate processes, multi-core)",
    "with ProcessPoolExecutor() as ex:": "CPU-core সংখ্যা অনুযায়ী worker process দিয়ে Process Pool তৈরি করা হয়েছে",
    "    print(list(ex.map(lambda x:x*x,[1,2,3])))": "প্রতিটি process-এ স্কয়ার ক্যালকুলেশন dispatch করে parallel execution-এর results list প্রিন্ট করা হয়েছে",

    "def add(a,b): return a+b": "a ও b দুইটি প্যারামিটারের যোগফল রিটার্ন করে এমন ছোট helper function ডিফাইন করা হয়েছে",
    "print(add(10,20))": "add() ফাংশনকে ১০ ও ২০ আর্গুমেন্ট দিয়ে call করে result ৩০ প্রিন্ট করা হয়েছে",
    "from pathlib import Path": "pathlib থেকে OOP-style file path handler 'Path' ক্লাস import করা হয়েছে",
    "for p in Path(\".\").glob(\"*.txt\"):": "বর্তমান directory (.) থেকে সব .txt ফাইলগুলোকে glob করে loop চালানো হয়েছে",
    "    print(p.name)": "প্রতিটি .txt ফাইলের শুধু filename (path না দিয়ে) প্রিন্ট করা হয়েছে",
    "import requests": "HTTP request করার জন্য জনপ্রিয় 'requests' লাইব্রেরি লোড করা হয়েছে",
    "r=requests.get(\"https://api.github.com\",timeout=10)": "GitHub API-তে GET request পাঠানো হয়েছে (১০ সেকেন্ড timeout সহ)",
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

FILE_HEADER_COMMENTS = {
    "16-numpy.html": "<!-- ===========================================================================\n     FILE: 16-numpy.html — Python Handbook অধ্যায় ১৬\n     বিষয়বস্তু: NumPy numerical computing library (arrays, indexing, aggregation, masks)\n     কাঠামো: Bangla structural comments + line-by-line Bengali explanations\n     =========================================================================== -->",
    "17-pandas.html": "<!-- ===========================================================================\n     FILE: 17-pandas.html — Python Handbook অধ্যায় ১৭\n     বিষয়বস্তু: Pandas data analysis (Series, DataFrame, selection, groupby, missing data)\n     কাঠামো: Bangla structural comments + line-by-line Bengali explanations\n     =========================================================================== -->",
    "18-visualization.html": "<!-- ===========================================================================\n     FILE: 18-visualization.html — Python Handbook অধ্যায় ১৮\n     বিষয়বস্তু: Matplotlib data visualization (line, scatter, histogram, subplots)\n     কাঠামো: Bangla structural comments + line-by-line Bengali explanations\n     =========================================================================== -->",
    "19-sql-sqlite.html": "<!-- ===========================================================================\n     FILE: 19-sql-sqlite.html — Python Handbook অধ্যায় ১৯\n     বিষয়বস্তু: SQL + SQLite database (CRUD, parameterized queries, Python workflow)\n     কাঠামো: Bangla structural comments + line-by-line Bengali explanations\n     =========================================================================== -->",
    "20-machine-learning-foundations.html": "<!-- ===========================================================================\n     FILE: 20-machine-learning-foundations.html — Python Handbook অধ্যায় ২০\n     বিষয়বস্তু: Machine Learning basics (features/labels, train-split, regression, classification)\n     কাঠামো: Bangla structural comments + line-by-line Bengali explanations\n     =========================================================================== -->",
    "21-concurrency-async.html": "<!-- ===========================================================================\n     FILE: 21-concurrency-async.html — Python Handbook অধ্যায় ২১\n     বিষয়বস্তু: Concurrency models (asyncio, ThreadPool, ProcessPool, I/O vs CPU bound)\n     কাঠামো: Bangla structural comments + line-by-line Bengali explanations\n     =========================================================================== -->",
    "22-portfolio-projects.html": "<!-- ===========================================================================\n     FILE: 22-portfolio-projects.html — Python Handbook অধ্যায় ২২\n     বিষয়বস্তু: Portfolio project ideas (CLI, automation, API client, architecture)\n     কাঠামো: Bangla structural comments + line-by-line Bengali explanations\n     =========================================================================== -->"
}

TOPIC_SECTION_COMMENTS = {
    "16-numpy.html": {
        "topic1": "<!-- ==============================================================\n             TOPIC SECTION #1: Array vs Python list — NumPy array-এর সুবিধা ও ভেক্টরাইজড অপারেশন\n             ============================================================== -->",
        "topic2": "<!-- ==============================================================\n             TOPIC SECTION #2: Indexing and slicing — Multi-dimensional array থেকে ডেটা বাছাই করা\n             ============================================================== -->",
        "topic3": "<!-- ==============================================================\n             TOPIC SECTION #3: Aggregation — Mean, sum, min, max ইত্যাদি summary statistics\n             ============================================================== -->",
        "topic4": "<!-- ==============================================================\n             TOPIC SECTION #4: Masks — Boolean condition দিয়ে ডেটা ফিল্টার করা\n             ============================================================== -->"
    },
    "17-pandas.html": {
        "topic1": "<!-- ==============================================================\n             TOPIC SECTION #1: DataFrame — Pandas-এর মূল ২D টেবিল ডেটা স্ট্রাকচার\n             ============================================================== -->",
        "topic2": "<!-- ==============================================================\n             TOPIC SECTION #2: Selection — Column selection ও Boolean masking দিয়ে রো ফিল্টার\n             ============================================================== -->",
        "topic3": "<!-- ==============================================================\n             TOPIC SECTION #3: GroupBy — ক্যাটাগরি/কলাম অনুযায়ী গ্রুপ করে aggregate করা\n             ============================================================== -->",
        "topic4": "<!-- ==============================================================\n             TOPIC SECTION #4: Missing data — NaN মান হ্যান্ডেল করা (fillna/imputation)\n             ============================================================== -->"
    },
    "18-visualization.html": {
        "topic1": "<!-- ==============================================================\n             TOPIC SECTION #1: Line plot — Ordered X-axis ধরে trend দেখানোর জন্য লাইন গ্রাফ\n             ============================================================== -->",
        "topic2": "<!-- ==============================================================\n             TOPIC SECTION #2: Scatter plot — দুইটি numeric variable-এর সম্পর্ক দেখানো\n             ============================================================== -->",
        "topic3": "<!-- ==============================================================\n             TOPIC SECTION #3: Histogram — Numeric value-এর ফ্রিকোয়েন্সি বিতরণ দেখানো\n             ============================================================== -->",
        "topic4": "<!-- ==============================================================\n             TOPIC SECTION #4: Subplots — এক Figure-এ একাধিক গ্রাফ সাজানো\n             ============================================================== -->"
    },
    "19-sql-sqlite.html": {
        "topic1": "<!-- ==============================================================\n             TOPIC SECTION #1: Create a database — SQLite ফাইল + table schema তৈরি\n             ============================================================== -->",
        "topic2": "<!-- ==============================================================\n             TOPIC SECTION #2: Insert safely — Parameterized query দিয়ে SQL injection এড়ানো\n             ============================================================== -->",
        "topic3": "<!-- ==============================================================\n             TOPIC SECTION #3: Read data — SELECT query + fetchAll দিয়ে রো পড়া\n             ============================================================== -->",
        "topic4": "<!-- ==============================================================\n             TOPIC SECTION #4: CRUD mindset — UPDATE (সাথে Create Read Delete) পুরো ডাটা লাইফসাইকেল\n             ============================================================== -->"
    },
    "20-machine-learning-foundations.html": {
        "topic1": "<!-- ==============================================================\n             TOPIC SECTION #1: Features and labels — ML input (X) ও output target (y) বোঝা\n             ============================================================== -->",
        "topic2": "<!-- ==============================================================\n             TOPIC SECTION #2: Train/test split — Unseen data দিয়ে মডেল নির্ভরযোগ্যভাবে মূল্যায়ন\n             ============================================================== -->",
        "topic3": "<!-- ==============================================================\n             TOPIC SECTION #3: Regression — Continuous/numeric value predict করা (Linear Regression)\n             ============================================================== -->",
        "topic4": "<!-- ==============================================================\n             TOPIC SECTION #4: Classification — Category/class predict করা (Decision Tree)\n             ============================================================== -->"
    },
    "21-concurrency-async.html": {
        "topic1": "<!-- ==============================================================\n             TOPIC SECTION #1: I/O-bound vs CPU-bound — কাজের ধরন অনুযায়ী concurrency স্ট্র্যাটেজি বেছে নেওয়া\n             ============================================================== -->",
        "topic2": "<!-- ==============================================================\n             TOPIC SECTION #2: Async task — asyncio + async/await দিয়ে single-threaded concurrent I/O\n             ============================================================== -->",
        "topic3": "<!-- ==============================================================\n             TOPIC SECTION #3: Threading concept — ThreadPoolExecutor + GIL-friendly I/O-bound workload\n             ============================================================== -->",
        "topic4": "<!-- ==============================================================\n             TOPIC SECTION #4: Multiprocessing concept — ProcessPoolExecutor + multi-core CPU-bound parallelism\n             ============================================================== -->"
    },
    "22-portfolio-projects.html": {
        "topic1": "<!-- ==============================================================\n             TOPIC SECTION #1: CLI project — Command-line tool (function + validation + menu)\n             ============================================================== -->",
        "topic2": "<!-- ==============================================================\n             TOPIC SECTION #2: Automation project — ফাইল/ফোল্ডার ডিটেক্ট করে repeatable task করা\n             ============================================================== -->",
        "topic3": "<!-- ==============================================================\n             TOPIC SECTION #3: API project — HTTP client (requests + JSON + error handling)\n             ============================================================== -->",
        "topic4": "<!-- ==============================================================\n             TOPIC SECTION #4: Capstone architecture — ৩-টায়ার ফোল্ডার স্ট্রাকচার (UI/logic/data)\n             ============================================================== -->"
    }
}


def add_ln_text_spans(html_content):
    def replace_linebox_div(match):
        full_match = match.group(0)
        inner = match.group(1)

        def replace_single_code(m2):
            code_open = m2.group(1)
            code_inner = m2.group(2)
            code_close = m2.group(3)

            key = unescape(code_inner).strip()

            if key in LN_TEXT_MAP:
                explanation = LN_TEXT_MAP[key]
            else:
                explanation = f"'{key}' — উপরের কোড লাইনটির কার্যকারিতা বিশ্লেষণ করুন"

            return f'<div>{code_open}{code_inner}{code_close}<span class="ln-text">{explanation}</span></div>'

        processed_inner = re.sub(
            r'(<div>\s*<code>)([^<]*?)(</code>\s*</div>)',
            replace_single_code,
            inner,
            flags=re.DOTALL
        )

        return f'<div class="linebox">{processed_inner}</div>'

    return re.sub(
        r'<div class="linebox">(.*?)</div>',
        replace_linebox_div,
        html_content,
        flags=re.DOTALL
    )


def insert_structural_comments(html_content, filename):
    result = html_content

    if filename in FILE_HEADER_COMMENTS:
        result = re.sub(
            r'(<!doctype html>)',
            FILE_HEADER_COMMENTS[filename] + r'\n\1',
            result,
            count=1
        )

    result = re.sub(
        r'(<head>)',
        r'\1\n        <!-- =========================================================\n             HEAD METADATA: Document title, charset, viewport, stylesheet attachment\n             ========================================================= -->',
        result
    )

    result = re.sub(
        r'(<body>)',
        r'\1\n    <!-- ==============================================================\n         BODY START\n         ============================================================== -->\n    <!-- TOP SCROLL PROGRESS BAR: .top i element width যতখানি scroll ততখানি বাড়ে (app.js দেখুন) -->',
        result
    )

    result = re.sub(
        r'(<nav>)',
        r'\n    <!-- ==============================================================\n         NAVIGATION BAR: brand logo + Home/Contents লিংকসমূহ\n         ============================================================== -->\n    \1',
        result
    )

    result = re.sub(
        r'(<main class="wrap reader">)',
        r'\n    <!-- ==============================================================\n         MAIN READER LAYOUT: ২-কলাম (TOC sidebar + article content) flex/grid wrapper\n         ============================================================== -->\n    \1',
        result
    )

    result = re.sub(
        r'(<aside class="toc">)',
        r'\n        <!-- ==========================================================\n             ASIDE TOC SIDEBAR: এখানে Chapter-এর সব heading-এর anchor লিংক আছে\n             (app.js-এর scroll spy দিয়ে active link highlight হয়)\n             ========================================================== -->\n        \1',
        result
    )

    result = re.sub(
        r'(<article class="article">)',
        r'\n        <!-- ==========================================================\n             ARTICLE BODY: Chapter-এর মূল কনটেন্ট (kicker, h1, lead, topics, practice, pager)\n             ========================================================== -->\n        \1',
        result
    )

    topic_comments = TOPIC_SECTION_COMMENTS.get(filename, {})
    for topic_id, comment_text in topic_comments.items():
        pattern = r'(<section>\s*<h2 id="' + re.escape(topic_id) + r'">)'
        replacement = r'\n        ' + comment_text + r'\n        \1'
        result = re.sub(pattern, replacement, result)

    result = re.sub(
        r'(<div class="code">)',
        r'            <!-- CODE BLOCK: Copy বাটন + <pre><code> syntax highlight area -->\n            \1',
        result
    )

    result = re.sub(
        r'(<div class="definition">)',
        r'            <!-- DEFINITION CALLOUT: সহজ ভাষায় concept-এর সংক্ষিপ্ত ব্যাখ্যা -->\n            \1',
        result
    )

    result = re.sub(
        r'(<div class="why">)',
        r'            <!-- WHY CALLOUT: কেন codeটি কাজ করছে — underlying mechanism ব্যাখ্যা -->\n            \1',
        result
    )

    result = re.sub(
        r'(<div class="tip">)',
        r'            <!-- TIP CALLOUT: Self-study guide / hands-on experiment নির্দেশনা -->\n            \1',
        result
    )

    result = re.sub(
        r'(<div class="linebox">)',
        r'            <!-- LINEBOX ROWS: প্রতিটি line-র জন্য code + Bangla explanation (ln-text) -->\n            \1',
        result
    )

    result = re.sub(
        r'(<h2 id="practice">Practice Lab</h2>)',
        r'\n        <!-- ==========================================================\n             PRACTICE EXERCISE AREA: ৩টি difficulty level — Beginner/Intermediate/Challenge\n             ========================================================== -->\n        \1',
        result
    )

    result = re.sub(
        r'(<div class="pager">)',
        r'\n        <!-- ==========================================================\n             PAGER NAVIGATION: Previous chapter + Colab link + Next chapter বাটন\n             ========================================================== -->\n        \1',
        result
    )

    result = re.sub(
        r'(<footer class="footer">)',
        r'\n    <!-- ==============================================================\n         FOOTER: Copyright + learning reference credits\n         ============================================================== -->\n    \1',
        result
    )

    result = re.sub(
        r'(<script src="\.\./assets/app\.js"></script>)',
        r'\n    <!-- ==============================================================\n         SCRIPT INCLUDE: Interactive logic (scroll bar, copy button, TOC spy)\n         ============================================================== -->\n    \1',
        result
    )

    return result


def pretty_print_html(html_content):
    INDENT = '    '
    output_lines = []
    current_indent = 0

    tokens = re.findall(
        r'<!--.*?-->|<[^>]+>|[^<]+',
        html_content,
        flags=re.DOTALL
    )

    i = 0
    while i < len(tokens):
        token = tokens[i]
        stripped = token.strip()

        if not stripped:
            i += 1
            continue

        if stripped.startswith('<!--'):
            comment_lines = stripped.split('\n')
            for cline in comment_lines:
                output_lines.append(INDENT * current_indent + cline.strip())
            i += 1
            continue

        if stripped.startswith('</'):
            tag_name = re.match(r'</([a-zA-Z0-9]+)', stripped)
            if tag_name:
                current_indent = max(0, current_indent - 1)
            output_lines.append(INDENT * current_indent + stripped)
            i += 1
            continue

        if stripped.startswith('<'):
            self_closing = bool(re.match(
                r'<(meta|link|br|hr|img|input|!doctype)',
                stripped,
                re.IGNORECASE
            ))
            is_void_no_slash = stripped.endswith('>') and not stripped.endswith('/>') and self_closing

            open_match = re.match(r'<([a-zA-Z0-9]+)', stripped)
            if open_match and not self_closing:
                tag_name_open = open_match.group(1).lower()
                close_at_end = stripped.endswith(f'</{tag_name_open}>') or (tag_name_open == 'html' and stripped.lower().endswith('</html>'))

                in_pre_code = False
                check = i
                depth_check = 1
                combined_text = stripped
                while check + 1 < len(tokens) and depth_check > 0:
                    check += 1
                    nxt = tokens[check].strip()
                    if nxt:
                        if nxt.startswith(f'</{tag_name_open}'):
                            depth_check -= 1
                        elif nxt.startswith(f'<{tag_name_open}') and not nxt.startswith(f'</') and not nxt.startswith(f'<{tag_name_open}/'):
                            depth_check += 1

                if check - i <= 3 and not (tag_name_open in ['pre', 'code', 'h1', 'h2', 'h3', 'p']):
                    has_child_element = False
                    for j in range(i + 1, check + 1):
                        if tokens[j].strip().startswith('<') and not tokens[j].strip().startswith('<!--') and not tokens[j].strip().startswith('</'):
                            has_child_element = True
                            break

                    if tag_name_open == 'code' or tag_name_open == 'span' or tag_name_open == 'a':
                        in_pre_code = True
                    if not has_child_element and tag_name_open not in ['div', 'section', 'article', 'aside', 'nav', 'footer', 'main', 'body', 'html', 'head', 'ul', 'ol', 'table', 'tr']:
                        in_pre_code = True

                if in_pre_code or close_at_end:
                    combined_parts = []
                    combined_parts.append(stripped)
                    j = i + 1
                    found_close = False
                    while j <= check:
                        combined_parts.append(tokens[j].strip() if tokens[j].strip() else tokens[j])
                        if tokens[j].strip().startswith(f'</{tag_name_open}'):
                            found_close = True
                            break
                        j += 1
                    if found_close:
                        output_lines.append(INDENT * current_indent + ''.join(combined_parts))
                        i = j + 1
                        continue

                output_lines.append(INDENT * current_indent + stripped)
                current_indent += 1
                i += 1
                continue

            output_lines.append(INDENT * current_indent + stripped)
            i += 1
            continue

        if output_lines and output_lines[-1].strip().startswith('<code'):
            output_lines[-1] = output_lines[-1].rstrip() + stripped
        elif output_lines and re.search(r'<code[^>]*>$', output_lines[-1]):
            output_lines[-1] = output_lines[-1].rstrip() + stripped
        else:
            text_lines = stripped.split('\n')
            for tl in text_lines:
                tl_strip = tl.strip()
                if tl_strip:
                    output_lines.append(INDENT * current_indent + tl_strip)
        i += 1

    return '\n'.join(output_lines)


def process_file(filepath, filename):
    with open(filepath, 'r', encoding='utf-8') as f:
        raw = f.read()

    step1 = add_ln_text_spans(raw)
    step2 = insert_structural_comments(step1, filename)
    step3 = pretty_print_html(step2)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(step3)

    print(f"[OK] PROCESSED: {filename}")


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
    import os
    for fn in files:
        fp = os.path.join(base_dir, fn)
        try:
            process_file(fp, fn)
        except Exception as e:
            print(f"[ERROR] in {fn}: {e}")
            import traceback
            traceback.print_exc()
