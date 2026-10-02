import re
import os

BASE = r"c:\Users\Mr  Alien\Downloads\python-handbook\chapters"

def html_unescape(s):
    return (s.replace("&lt;", "<")
             .replace("&gt;", ">")
             .replace("&amp;", "&")
             .replace("&quot;", '"')
             .replace("&#39;", "'"))

def html_escape(s):
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;"))

# =====================================================================
# EXACT ORIGINAL MINIFIED HTML CONTENTS (from first Read runs before any
# processing). This lets us BYPASS "recovery" entirely.
# =====================================================================
ORIGINALS = {}

ORIGINALS["08-functions.html"] = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 08 — Functions | Python Handbook</title><link rel="stylesheet" href="../assets/style.css"></head><body><div class="top"><i></i></div><nav><div class="navin"><a class="brand" href="../index.html">Python<b>Handbook</b></a><div class="links"><a href="../index.html">Home</a><a href="../index.html#chapters">Contents</a></div></div></nav><main class="wrap reader"><aside class="toc"><b>Chapter contents</b><a href="#topic1">1. Defining a function</a><a href="#topic2">2. Default and keyword arguments</a><a href="#topic3">3. *args and **kwargs</a><a href="#topic4">4. Recursion</a><a href="#practice">Practice Lab</a><a href="#check">Check yourself</a></aside><article class="article"><div class="kicker">CHAPTER 08 · CONCEPT → CODE → EXPLANATION</div><h1>Functions</h1><p class="lead">parameters, return, defaults, keyword arguments, scope, *args, **kwargs, lambda, recursion</p><div class="tip"><b>How to study this page:</b> প্রথমে explanation পড়ো → code নিজে টাইপ করো → output দেখো → প্রতিটি line কী করছে নিজের ভাষায় বলো → তারপর code পরিবর্তন করো।</div><section><h2 id="topic1">1. Defining a function</h2><div class="definition"><b>সহজ ভাষায়:</b> Functions package reusable behavior.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code>def add(a, b):
    return a + b

print(add(10, 20))</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code>def add(a, b):</code></div><div><code>    return a + b</code></div><div><code>print(add(10, 20))</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>def creates the function. Parameters receive values. return sends a result back.</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><section><h2 id="topic2">2. Default and keyword arguments</h2><div class="definition"><b>সহজ ভাষায়:</b> Defaults make arguments optional and keyword arguments make calls clearer.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code>def greet(name, message="Welcome"):
    return f"{message}, {name}!"
print(greet("Renco"))
print(greet("Renco", message="Good morning"))</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code>def greet(name, message="Welcome"):</code></div><div><code>    return f"{message}, {name}!"</code></div><div><code>print(greet("Renco"))</code></div><div><code>print(greet("Renco", message="Good morning"))</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>The default is used when message is omitted. The keyword call explicitly names the parameter.</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><section><h2 id="topic3">3. *args and **kwargs</h2><div class="definition"><b>সহজ ভাষায়:</b> They collect variable-length positional and keyword arguments.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code>def report(*scores, **info):
    print(scores)
    print(info)
report(80,90,name="Renco")</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code>def report(*scores, **info):</code></div><div><code>    print(scores)</code></div><div><code>    print(info)</code></div><div><code>report(80,90,name="Renco")</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>scores becomes a tuple; info becomes a dictionary.</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><section><h2 id="topic4">4. Recursion</h2><div class="definition"><b>সহজ ভাষায়:</b> A recursive function calls itself and needs a base case.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code>def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)
print(factorial(5))</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code>def factorial(n):</code></div><div><code>    if n <= 1:</code></div><div><code>        return 1</code></div><div><code>    return n * factorial(n-1)</code></div><div><code>print(factorial(5))</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>The base case stops recursion. Each call reduces n until the base case.</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><h2 id="practice">Practice Lab</h2>
<div class="exercise"><b>Beginner:</b> এই chapter-এর সবচেয়ে সহজ concept দিয়ে নিজের একটি ছোট program লেখো।<br><br>
<b>Intermediate:</b> একটি example পরিবর্তন করে user input যোগ করো।<br><br>
<b>Challenge:</b> একটি edge case handle করো এবং কেন সেটি দরকার—নিজের ভাষায় লিখো।</div>
<h2 id="check">Before moving on</h2><p>তুমি কি এই chapter-এর code না দেখে একটি ছোট variation লিখতে পারো? পারলে next chapter-এ যাও। না পারলে examples আবার টাইপ করো—মুখস্থ নয়, বুঝে।</p><div class="pager"><a class="btn alt" href="07-loops.html">← Previous</a><a class="btn" href="https://colab.research.google.com/github/renco88/python-handbook/blob/main/notebooks/08-functions/lesson.ipynb" target="_blank">Open Chapter in Colab ↗</a><a class="btn alt" href="09-modules-packages.html">Next →</a></div></article></main><footer class="footer"><div class="wrap">Python Handbook · Learning reference: Python documentation + Python Data Science Handbook</div></footer><script src="../assets/app.js"></script></body></html>"""

ORIGINALS["09-modules-packages.html"] = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 09 — Modules &amp; Packages | Python Handbook</title><link rel="stylesheet" href="../assets/style.css"></head><body><div class="top"><i></i></div><nav><div class="navin"><a class="brand" href="../index.html">Python<b>Handbook</b></a><div class="links"><a href="../index.html">Home</a><a href="../index.html#chapters">Contents</a></div></div></nav><main class="wrap reader"><aside class="toc"><b>Chapter contents</b><a href="#topic1">1. Importing modules</a><a href="#topic2">2. Creating a module</a><a href="#topic3">3. pip and environments</a><a href="#practice">Practice Lab</a><a href="#check">Check yourself</a></aside><article class="article"><div class="kicker">CHAPTER 09 · CONCEPT → CODE → EXPLANATION</div><h1>Modules &amp; Packages</h1><p class="lead">import, standard library, creating modules, packages, pip and virtual environments</p><div class="tip"><b>How to study this page:</b> প্রথমে explanation পড়ো → code নিজে টাইপ করো → output দেখো → প্রতিটি line কী করছে নিজের ভাষায় বলো → তারপর code পরিবর্তন করো।</div><section><h2 id="topic1">1. Importing modules</h2><div class="definition"><b>সহজ ভাষায়:</b> Modules let you reuse code from another file or the standard library.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code>import math
print(math.sqrt(144))</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code>import math</code></div><div><code>print(math.sqrt(144))</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>import loads the module; math.sqrt accesses its sqrt function.</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><section><h2 id="topic2">2. Creating a module</h2><div class="definition"><b>সহজ ভাষায়:</b> Your own .py file can be imported by another script.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code># tools.py
def double(x):
    return x * 2

# main.py
from tools import double
print(double(8))</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code># tools.py</code></div><div><code>def double(x):</code></div><div><code>    return x * 2</code></div><div><code># main.py</code></div><div><code>from tools import double</code></div><div><code>print(double(8))</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>The function lives in tools.py and is imported into main.py.</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><section><h2 id="topic3">3. pip and environments</h2><div class="definition"><b>সহজ ভাষায়:</b> Virtual environments isolate project dependencies.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code>python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install requests</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code>python -m venv .venv</code></div><div><code># Windows PowerShell</code></div><div><code>.venv\Scripts\Activate.ps1</code></div><div><code>pip install requests</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>The environment keeps packages for one project separate from others.</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><h2 id="practice">Practice Lab</h2>
<div class="exercise"><b>Beginner:</b> এই chapter-এর সবচেয়ে সহজ concept দিয়ে নিজের একটি ছোট program লেখো।<br><br>
<b>Intermediate:</b> একটি example পরিবর্তন করে user input যোগ করো।<br><br>
<b>Challenge:</b> একটি edge case handle করো এবং কেন সেটি দরকার—নিজের ভাষায় লিখো।</div>
<h2 id="check">Before moving on</h2><p>তুমি কি এই chapter-এর code না দেখে একটি ছোট variation লিখতে পারো? পারলে next chapter-এ যাও। না পারলে examples আবার টাইপ করো—মুখস্থ নয়, বুঝে।</p><div class="pager"><a class="btn alt" href="08-functions.html">← Previous</a><a class="btn" href="https://colab.research.google.com/github/renco88/python-handbook/blob/main/notebooks/09-modules-packages/lesson.ipynb" target="_blank">Open Chapter in Colab ↗</a><a class="btn alt" href="10-files-json-csv.html">Next →</a></div></article></main><footer class="footer"><div class="wrap">Python Handbook · Learning reference: Python documentation + Python Data Science Handbook</div></footer><script src="../assets/app.js"></script></body></html>"""

ORIGINALS["10-files-json-csv.html"] = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 10 — Files, JSON &amp; CSV | Python Handbook</title><link rel="stylesheet" href="../assets/style.css"></head><body><div class="top"><i></i></div><nav><div class="navin"><a class="brand" href="../index.html">Python<b>Handbook</b></a><div class="links"><a href="../index.html">Home</a><a href="../index.html#chapters">Contents</a></div></div></nav><main class="wrap reader"><aside class="toc"><b>Chapter contents</b><a href="#topic1">1. Writing a file</a><a href="#topic2">2. Reading a file</a><a href="#topic3">3. JSON</a><a href="#topic4">4. CSV</a><a href="#practice">Practice Lab</a><a href="#check">Check yourself</a></aside><article class="article"><div class="kicker">CHAPTER 10 · CONCEPT → CODE → EXPLANATION</div><h1>Files, JSON &amp; CSV</h1><p class="lead">open(), with, pathlib, read/write/append, JSON, CSV and data persistence</p><div class="tip"><b>How to study this page:</b> প্রথমে explanation পড়ো → code নিজে টাইপ করো → output দেখো → প্রতিটি line কী করছে নিজের ভাষায় বলো → তারপর code পরিবর্তন করো।</div><section><h2 id="topic1">1. Writing a file</h2><div class="definition"><b>সহজ ভাষায়:</b> open() with mode w creates or overwrites a file.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code>with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("Hello Python")</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code>with open("notes.txt", "w", encoding="utf-8") as f:</code></div><div><code>    f.write("Hello Python")</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>with manages the file lifecycle and closes it after the block.</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><section><h2 id="topic2">2. Reading a file</h2><div class="definition"><b>সহজ ভাষায়:</b> read() loads the contents as text.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code>with open("notes.txt", "r", encoding="utf-8") as f:
    content = f.read()
print(content)</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code>with open("notes.txt", "r", encoding="utf-8") as f:</code></div><div><code>    content = f.read()</code></div><div><code>print(content)</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>The file is opened for reading and the text is assigned to content.</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><section><h2 id="topic3">3. JSON</h2><div class="definition"><b>সহজ ভাষায়:</b> JSON represents structured data and maps naturally to Python dictionaries and lists.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code>import json
data={"name":"Renco","skills":["Python","React"]}
text=json.dumps(data, indent=2)
print(text)</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code>import json</code></div><div><code>data={"name":"Renco","skills":["Python","React"]}</code></div><div><code>text=json.dumps(data, indent=2)</code></div><div><code>print(text)</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>dumps converts Python data to JSON text.</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><section><h2 id="topic4">4. CSV</h2><div class="definition"><b>সহজ ভাষায়:</b> CSV stores tabular data as rows and columns.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code>import csv
with open("students.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print(row["name"])</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code>import csv</code></div><div><code>with open("students.csv", newline="", encoding="utf-8") as f:</code></div><div><code>    for row in csv.DictReader(f):</code></div><div><code>        print(row["name"])</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>DictReader turns each row into a dictionary keyed by the header.</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><h2 id="practice">Practice Lab</h2>
<div class="exercise"><b>Beginner:</b> এই chapter-এর সবচেয়ে সহজ concept দিয়ে নিজের একটি ছোট program লেখো।<br><br>
<b>Intermediate:</b> একটি example পরিবর্তন করে user input যোগ করো।<br><br>
<b>Challenge:</b> একটি edge case handle করো এবং কেন সেটি দরকার—নিজের ভাষায় লিখো।</div>
<h2 id="check">Before moving on</h2><p>তুমি কি এই chapter-এর code না দেখে একটি ছোট variation লিখতে পারো? পারলে next chapter-এ যাও। না পারলে examples আবার টাইপ করো—মুখস্থ নয়, বুঝে।</p><div class="pager"><a class="btn alt" href="09-modules-packages.html">← Previous</a><a class="btn" href="https://colab.research.google.com/github/renco88/python-handbook/blob/main/notebooks/10-files-json-csv/lesson.ipynb" target="_blank">Open Chapter in Colab ↗</a><a class="btn alt" href="11-exceptions-debugging.html">Next →</a></div></article></main><footer class="footer"><div class="wrap">Python Handbook · Learning reference: Python documentation + Python Data Science Handbook</div></footer><script src="../assets/app.js"></script></body></html>"""

ORIGINALS["11-exceptions-debugging.html"] = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 11 — Exceptions &amp; Debugging | Python Handbook</title><link rel="stylesheet" href="../assets/style.css"></head><body><div class="top"><i></i></div><nav><div class="navin"><a class="brand" href="../index.html">Python<b>Handbook</b></a><div class="links"><a href="../index.html">Home</a><a href="../index.html#chapters">Contents</a></div></div></nav><main class="wrap reader"><aside class="toc"><b>Chapter contents</b><a href="#topic1">1. Reading a traceback</a><a href="#topic2">2. try / except</a><a href="#topic3">3. raise</a><a href="#topic4">4. finally</a><a href="#practice">Practice Lab</a><a href="#check">Check yourself</a></aside><article class="article"><div class="kicker">CHAPTER 11 · CONCEPT → CODE → EXPLANATION</div><h1>Exceptions &amp; Debugging</h1><p class="lead">tracebacks, try/except/else/finally, raise, custom exceptions, assertions and debugging</p><div class="tip"><b>How to study this page:</b> প্রথমে explanation পড়ো → code নিজে টাইপ করো → output দেখো → প্রতিটি line কী করছে নিজের ভাষায় বলো → তারপর code পরিবর্তন করো।</div><section><h2 id="topic1">1. Reading a traceback</h2><div class="definition"><b>সহজ ভাষায়:</b> A traceback tells you where an exception happened and what type it was.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code>numbers = [1,2]
print(numbers[5])</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code>numbers = [1,2]</code></div><div><code>print(numbers[5])</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>IndexError tells us the requested index does not exist.</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><section><h2 id="topic2">2. try / except</h2><div class="definition"><b>সহজ ভাষায়:</b> Handle expected runtime problems without crashing the whole program.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code>try:
    n=int(input("Number: "))
    print(10/n)
except ValueError:
    print("Enter an integer")
except ZeroDivisionError:
    print("Zero is not allowed")</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code>try:</code></div><div><code>    n=int(input("Number: "))</code></div><div><code>    print(10/n)</code></div><div><code>except ValueError:</code></div><div><code>    print("Enter an integer")</code></div><div><code>except ZeroDivisionError:</code></div><div><code>    print("Zero is not allowed")</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>Each except handles a particular failure.</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><section><h2 id="topic3">3. raise</h2><div class="definition"><b>সহজ ভাষায়:</b> raise lets your program reject invalid state explicitly.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code>def withdraw(balance, amount):
    if amount > balance:
        raise ValueError("Insufficient balance")
    return balance-amount</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code>def withdraw(balance, amount):</code></div><div><code>    if amount > balance:</code></div><div><code>        raise ValueError("Insufficient balance")</code></div><div><code>    return balance-amount</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>The function creates a clear error when the business rule is violated.</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><section><h2 id="topic4">4. finally</h2><div class="definition"><b>সহজ ভাষায়:</b> finally runs whether an exception happened or not.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code>try:
    print(10/2)
finally:
    print("Cleanup")</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code>try:</code></div><div><code>    print(10/2)</code></div><div><code>finally:</code></div><div><code>    print("Cleanup")</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>Cleanup code can be placed in finally.</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><h2 id="practice">Practice Lab</h2>
<div class="exercise"><b>Beginner:</b> এই chapter-এর সবচেয়ে সহজ concept দিয়ে নিজের একটি ছোট program লেখো।<br><br>
<b>Intermediate:</b> একটি example পরিবর্তন করে user input যোগ করো।<br><br>
<b>Challenge:</b> একটি edge case handle করো এবং কেন সেটি দরকার—নিজের ভাষায় লিখো।</div>
<h2 id="check">Before moving on</h2><p>তুমি কি এই chapter-এর code না দেখে একটি ছোট variation লিখতে পারো? পারলে next chapter-এ যাও। না পারলে examples আবার টাইপ করো—মুখস্থ নয়, বুঝে।</p><div class="pager"><a class="btn alt" href="10-files-json-csv.html">← Previous</a><a class="btn" href="https://colab.research.google.com/github/renco88/python-handbook/blob/main/notebooks/11-exceptions-debugging/lesson.ipynb" target="_blank">Open Chapter in Colab ↗</a><a class="btn alt" href="12-oop.html">Next →</a></div></article></main><footer class="footer"><div class="wrap">Python Handbook · Learning reference: Python documentation + Python Data Science Handbook</div></footer><script src="../assets/app.js"></script></body></html>"""

ORIGINALS["12-oop.html"] = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 12 — OOP | Python Handbook</title><link rel="stylesheet" href="../assets/style.css"></head><body><div class="top"><i></i></div><nav><div class="navin"><a class="brand" href="../index.html">Python<b>Handbook</b></a><div class="links"><a href="../index.html">Home</a><a href="../index.html#chapters">Contents</a></div></div></nav><main class="wrap reader"><aside class="toc"><b>Chapter contents</b><a href="#topic1">1. Class and object</a><a href="#topic2">2. Instance method</a><a href="#topic3">3. Inheritance and overriding</a><a href="#topic4">4. Encapsulation and abstraction</a><a href="#practice">Practice Lab</a><a href="#check">Check yourself</a></aside><article class="article"><div class="kicker">CHAPTER 12 · CONCEPT → CODE → EXPLANATION</div><h1>OOP</h1><p class="lead">classes, objects, __init__, methods, inheritance, polymorphism, encapsulation, abstraction</p><div class="tip"><b>How to study this page:</b> প্রথমে explanation পড়ো → code নিজে টাইপ করো → output দেখো → প্রতিটি line কী করছে নিজের ভাষায় বলো → তারপর code পরিবর্তন করো।</div><section><h2 id="topic1">1. Class and object</h2><div class="definition"><b>সহজ ভাষায়:</b> A class is a blueprint; an object is an instance created from it.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code>class Student:
    def __init__(self, name):
        self.name = name

s = Student("Renco")
print(s.name)</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code>class Student:</code></div><div><code>    def __init__(self, name):</code></div><div><code>        self.name = name</code></div><div><code>s = Student("Renco")</code></div><div><code>print(s.name)</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>__init__ initializes each new object. self refers to the current object.</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><section><h2 id="topic2">2. Instance method</h2><div class="definition"><b>সহজ ভাষায়:</b> Methods operate on object data.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code>class Student:
    def __init__(self,name): self.name=name
    def introduce(self): return f"I am {self.name}"
print(Student("Renco").introduce())</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code>class Student:</code></div><div><code>    def __init__(self,name): self.name=name</code></div><div><code>    def introduce(self): return f"I am {self.name}"</code></div><div><code>print(Student("Renco").introduce())</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>The method uses self.name from the specific object.</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><section><h2 id="topic3">3. Inheritance and overriding</h2><div class="definition"><b>সহজ ভাষায়:</b> A child class can inherit and replace behavior from a parent.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code>class Animal:
    def speak(self): return "sound"
class Dog(Animal):
    def speak(self): return "woof"
print(Dog().speak())</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code>class Animal:</code></div><div><code>    def speak(self): return "sound"</code></div><div><code>class Dog(Animal):</code></div><div><code>    def speak(self): return "woof"</code></div><div><code>print(Dog().speak())</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>Dog inherits Animal but overrides speak. This is a simple polymorphic pattern.</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><section><h2 id="topic4">4. Encapsulation and abstraction</h2><div class="definition"><b>সহজ ভাষায়:</b> Internal details can be protected behind methods; abstract classes define required behavior.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code>from abc import ABC, abstractmethod
class Shape(ABC):
    @abstractmethod
    def area(self): pass
class Square(Shape):
    def __init__(self,s): self.s=s
    def area(self): return self.s*self.s
print(Square(4).area())</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code>from abc import ABC, abstractmethod</code></div><div><code>class Shape(ABC):</code></div><div><code>    @abstractmethod</code></div><div><code>    def area(self): pass</code></div><div><code>class Square(Shape):</code></div><div><code>    def __init__(self,s): self.s=s</code></div><div><code>    def area(self): return self.s*self.s</code></div><div><code>print(Square(4).area())</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>The abstract interface says every Shape must provide area().</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><h2 id="practice">Practice Lab</h2>
<div class="exercise"><b>Beginner:</b> এই chapter-এর সবচেয়ে সহজ concept দিয়ে নিজের একটি ছোট program লেখো।<br><br>
<b>Intermediate:</b> একটি example পরিবর্তন করে user input যোগ করো।<br><br>
<b>Challenge:</b> একটি edge case handle করো এবং কেন সেটি দরকার—নিজের ভাষায় লিখো।</div>
<h2 id="check">Before moving on</h2><p>তুমি কি এই chapter-এর code না দেখে একটি ছোট variation লিখতে পারো? পারলে next chapter-এ যাও। না পারলে examples আবার টাইপ করো—মুখস্থ নয়, বুঝে।</p><div class="pager"><a class="btn alt" href="11-exceptions-debugging.html">← Previous</a><a class="btn" href="https://colab.research.google.com/github/renco88/python-handbook/blob/main/notebooks/12-oop/lesson.ipynb" target="_blank">Open Chapter in Colab ↗</a><a class="btn alt" href="13-pythonic-intermediate.html">Next →</a></div></article></main><footer class="footer"><div class="wrap">Python Handbook · Learning reference: Python documentation + Python Data Science Handbook</div></footer><script src="../assets/app.js"></script></body></html>"""

ORIGINALS["13-pythonic-intermediate.html"] = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 13 — Pythonic &amp; Intermediate | Python Handbook</title><link rel="stylesheet" href="../assets/style.css"></head><body><div class="top"><i></i></div><nav><div class="navin"><a class="brand" href="../index.html">Python<b>Handbook</b></a><div class="links"><a href="../index.html">Home</a><a href="../index.html#chapters">Contents</a></div></div></nav><main class="wrap reader"><aside class="toc"><b>Chapter contents</b><a href="#topic1">1. Unpacking</a><a href="#topic2">2. Generator</a><a href="#topic3">3. Decorator</a><a href="#topic4">4. Context manager</a><a href="#practice">Practice Lab</a><a href="#check">Check yourself</a></aside><article class="article"><div class="kicker">CHAPTER 13 · CONCEPT → CODE → EXPLANATION</div><h1>Pythonic &amp; Intermediate</h1><p class="lead">comprehensions, unpacking, iterators, generators, decorators, context managers, dataclasses</p><div class="tip"><b>How to study this page:</b> প্রথমে explanation পড়ো → code নিজে টাইপ করো → output দেখো → প্রতিটি line কী করছে নিজের ভাষায় বলো → তারপর code পরিবর্তন করো।</div><section><h2 id="topic1">1. Unpacking</h2><div class="definition"><b>সহজ ভাষায়:</b> Python can unpack sequences into separate variables.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code>first, *middle, last = [1,2,3,4]
print(first, middle, last)</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code>first, *middle, last = [1,2,3,4]</code></div><div><code>print(first, middle, last)</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>The star collects remaining values into a list.</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><section><h2 id="topic2">2. Generator</h2><div class="definition"><b>সহজ ভাষায়:</b> Generators produce values lazily with yield.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code>def countdown(n):
    while n:
        yield n
        n -= 1
print(list(countdown(3)))</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code>def countdown(n):</code></div><div><code>    while n:</code></div><div><code>        yield n</code></div><div><code>        n -= 1</code></div><div><code>print(list(countdown(3)))</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>yield pauses the function and resumes it later, which can save memory.</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><section><h2 id="topic3">3. Decorator</h2><div class="definition"><b>সহজ ভাষায়:</b> A decorator wraps a function to add behavior.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code>def log_call(fn):
    def wrapper(*args, **kwargs):
        print("Calling", fn.__name__)
        return fn(*args, **kwargs)
    return wrapper

@log_call
def hello(): return "Hi"
print(hello())</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code>def log_call(fn):</code></div><div><code>    def wrapper(*args, **kwargs):</code></div><div><code>        print("Calling", fn.__name__)</code></div><div><code>        return fn(*args, **kwargs)</code></div><div><code>    return wrapper</code></div><div><code>@log_call</code></div><div><code>def hello(): return "Hi"</code></div><div><code>print(hello())</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>@log_call replaces hello with the wrapped version.</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><section><h2 id="topic4">4. Context manager</h2><div class="definition"><b>সহজ ভাষায়:</b> with is a clean way to acquire and release resources.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code>with open("notes.txt", encoding="utf-8") as f:
    text=f.read()</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code>with open("notes.txt", encoding="utf-8") as f:</code></div><div><code>    text=f.read()</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>The context manager handles cleanup automatically.</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><h2 id="practice">Practice Lab</h2>
<div class="exercise"><b>Beginner:</b> এই chapter-এর সবচেয়ে সহজ concept দিয়ে নিজের একটি ছোট program লেখো।<br><br>
<b>Intermediate:</b> একটি example পরিবর্তন করে user input যোগ করো।<br><br>
<b>Challenge:</b> একটি edge case handle করো এবং কেন সেটি দরকার—নিজের ভাষায় লিখো।</div>
<h2 id="check">Before moving on</h2><p>তুমি কি এই chapter-এর code না দেখে একটি ছোট variation লিখতে পারো? পারলে next chapter-এ যাও। না পারলে examples আবার টাইপ করো—মুখস্থ নয়, বুঝে।</p><div class="pager"><a class="btn alt" href="12-oop.html">← Previous</a><a class="btn" href="https://colab.research.google.com/github/renco88/python-handbook/blob/main/notebooks/13-pythonic-intermediate/lesson.ipynb" target="_blank">Open Chapter in Colab ↗</a><a class="btn alt" href="14-typing-testing-clean-code.html">Next →</a></div></article></main><footer class="footer"><div class="wrap">Python Handbook · Learning reference: Python documentation + Python Data Science Handbook</div></footer><script src="../assets/app.js"></script></body></html>"""

ORIGINALS["14-typing-testing-clean-code.html"] = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 14 — Typing, Testing &amp; Clean Code | Python Handbook</title><link rel="stylesheet" href="../assets/style.css"></head><body><div class="top"><i></i></div><nav><div class="navin"><a class="brand" href="../index.html">Python<b>Handbook</b></a><div class="links"><a href="../index.html">Home</a><a href="../index.html#chapters">Contents</a></div></div></nav><main class="wrap reader"><aside class="toc"><b>Chapter contents</b><a href="#topic1">1. Type hints</a><a href="#topic2">2. Assertions</a><a href="#topic3">3. Logging</a><a href="#topic4">4. Clean project structure</a><a href="#practice">Practice Lab</a><a href="#check">Check yourself</a></aside><article class="article"><div class="kicker">CHAPTER 14 · CONCEPT → CODE → EXPLANATION</div><h1>Typing, Testing &amp; Clean Code</h1><p class="lead">type hints, docstrings, pytest concepts, assertions, logging, project structure and style</p><div class="tip"><b>How to study this page:</b> প্রথমে explanation পড়ো → code নিজে টাইপ করো → output দেখো → প্রতিটি line কী করছে নিজের ভাষায় বলো → তারপর code পরিবর্তন করো।</div><section><h2 id="topic1">1. Type hints</h2><div class="definition"><b>সহজ ভাষায়:</b> Type hints document intended types and help tools detect mistakes.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code>def add(a: int, b: int) -&gt; int:
    return a + b</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code>def add(a: int, b: int) -&gt; int:</code></div><div><code>    return a + b</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>The annotations say what types the function expects and returns.</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><section><h2 id="topic2">2. Assertions</h2><div class="definition"><b>সহজ ভাষায়:</b> Assertions check assumptions during development and tests.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code>def add(a,b): return a+b
assert add(2,3) == 5</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code>def add(a,b): return a+b</code></div><div><code>assert add(2,3) == 5</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>If the condition is false, Python raises AssertionError.</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><section><h2 id="topic3">3. Logging</h2><div class="definition"><b>সহজ ভাষায়:</b> Logging records useful runtime information.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code>import logging
logging.basicConfig(level=logging.INFO)
logging.info("Application started")</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code>import logging</code></div><div><code>logging.basicConfig(level=logging.INFO)</code></div><div><code>logging.info("Application started")</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>Logging is preferable to scattered print statements in larger applications.</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><section><h2 id="topic4">4. Clean project structure</h2><div class="definition"><b>সহজ ভাষায়:</b> Separate application code, tests, configuration and documentation as a project grows.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code>project/
  src/
  tests/
  README.md
  pyproject.toml</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code>project/</code></div><div><code>  src/</code></div><div><code>  tests/</code></div><div><code>  README.md</code></div><div><code>  pyproject.toml</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>A predictable structure makes collaboration and maintenance easier.</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><h2 id="practice">Practice Lab</h2>
<div class="exercise"><b>Beginner:</b> এই chapter-এর সবচেয়ে সহজ concept দিয়ে নিজের একটি ছোট program লেখো।<br><br>
<b>Intermediate:</b> একটি example পরিবর্তন করে user input যোগ করো।<br><br>
<b>Challenge:</b> একটি edge case handle করো এবং কেন সেটি দরকার—নিজের ভাষায় লিখো।</div>
<h2 id="check">Before moving on</h2><p>তুমি কি এই chapter-এর code না দেখে একটি ছোট variation লিখতে পারো? পারলে next chapter-এ যাও। না পারলে examples আবার টাইপ করো—মুখস্থ নয়, বুঝে।</p><div class="pager"><a class="btn alt" href="13-pythonic-intermediate.html">← Previous</a><a class="btn" href="https://colab.research.google.com/github/renco88/python-handbook/blob/main/notebooks/14-typing-testing-clean-code/lesson.ipynb" target="_blank">Open Chapter in Colab ↗</a><a class="btn alt" href="15-http-apis-automation.html">Next →</a></div></article></main><footer class="footer"><div class="wrap">Python Handbook · Learning reference: Python documentation + Python Data Science Handbook</div></footer><script src="../assets/app.js"></script></body></html>"""

ORIGINALS["15-http-apis-automation.html"] = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 15 — HTTP, APIs &amp; Automation | Python Handbook</title><link rel="stylesheet" href="../assets/style.css"></head><body><div class="top"><i></i></div><nav><div class="navin"><a class="brand" href="../index.html">Python<b>Handbook</b></a><div class="links"><a href="../index.html">Home</a><a href="../index.html#chapters">Contents</a></div></div></nav><main class="wrap reader"><aside class="toc"><b>Chapter contents</b><a href="#topic1">1. HTTP mental model</a><a href="#topic2">2. JSON API</a><a href="#topic3">3. POST request</a><a href="#topic4">4. Automation</a><a href="#practice">Practice Lab</a><a href="#check">Check yourself</a></aside><article class="article"><div class="kicker">CHAPTER 15 · CONCEPT → CODE → EXPLANATION</div><h1>HTTP, APIs &amp; Automation</h1><p class="lead">requests, HTTP concepts, JSON APIs, status codes, automation patterns and safe scripting</p><div class="tip"><b>How to study this page:</b> প্রথমে explanation পড়ো → code নিজে টাইপ করো → output দেখো → প্রতিটি line কী করছে নিজের ভাষায় বলো → তারপর code পরিবর্তন করো।</div><section><h2 id="topic1">1. HTTP mental model</h2><div class="definition"><b>সহজ ভাষায়:</b> A client sends a request; a server returns a response with a status code and data.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code>import requests
r=requests.get("https://api.github.com", timeout=10)
print(r.status_code)</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code>import requests</code></div><div><code>r=requests.get("https://api.github.com", timeout=10)</code></div><div><code>print(r.status_code)</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>requests performs the HTTP call and status_code tells you the outcome class.</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><section><h2 id="topic2">2. JSON API</h2><div class="definition"><b>সহজ ভাষায়:</b> Many APIs return JSON that becomes Python dictionaries/lists.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code>data=r.json()
print(type(data))
print(data.keys())</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code>data=r.json()</code></div><div><code>print(type(data))</code></div><div><code>print(data.keys())</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>json() parses the response body into Python data.</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><section><h2 id="topic3">3. POST request</h2><div class="definition"><b>সহজ ভাষায়:</b> POST commonly sends data to a server.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code>payload={"name":"Renco"}
r=requests.post("https://httpbin.org/post", json=payload, timeout=10)
print(r.status_code)</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code>payload={"name":"Renco"}</code></div><div><code>r=requests.post("https://httpbin.org/post", json=payload, timeout=10)</code></div><div><code>print(r.status_code)</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>The json parameter serializes the dictionary as JSON.</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><section><h2 id="topic4">4. Automation</h2><div class="definition"><b>সহজ ভাষায়:</b> Automation means turning a repeated manual workflow into deterministic code.</div><h3>Example</h3><div class="code"><button class="copy">Copy</button><pre><code>from pathlib import Path
for p in Path(".").glob("*.txt"):
    print("Found:",p.name)</code></pre></div><h3>Line-by-line explanation</h3><div class="linebox"><div><code>from pathlib import Path</code></div><div><code>for p in Path(".").glob("*.txt"):</code></div><div><code>    print("Found:",p.name)</code></div></div><div class="why"><b>কেন কাজ করছে?</b><br>The script discovers matching files without manually listing them.</div><div class="tip"><b>নিজে experiment করো:</b> উপরের example-এ অন্তত ২টি value পরিবর্তন করে output আগে অনুমান করো, তারপর run করো।</div></section><h2 id="practice">Practice Lab</h2>
<div class="exercise"><b>Beginner:</b> এই chapter-এর সবচেয়ে সহজ concept দিয়ে নিজের একটি ছোট program লেখো।<br><br>
<b>Intermediate:</b> একটি example পরিবর্তন করে user input যোগ করো।<br><br>
<b>Challenge:</b> একটি edge case handle করো এবং কেন সেটি দরকার—নিজের ভাষায় লিখো।</div>
<h2 id="check">Before moving on</h2><p>তুমি কি এই chapter-এর code না দেখে একটি ছোট variation লিখতে পারো? পারলে next chapter-এ যাও। না পারলে examples আবার টাইপ করো—মুখস্থ নয়, বুঝে।</p><div class="pager"><a class="btn alt" href="14-typing-testing-clean-code.html">← Previous</a><a class="btn" href="https://colab.research.google.com/github/renco88/python-handbook/blob/main/notebooks/15-http-apis-automation/lesson.ipynb" target="_blank">Open Chapter in Colab ↗</a><a class="btn alt" href="16-numpy.html">Next →</a></div></article></main><footer class="footer"><div class="wrap">Python Handbook · Learning reference: Python documentation + Python Data Science Handbook</div></footer><script src="../assets/app.js"></script></body></html>"""


# =====================================================================
# EXPLANATION DICT
# =====================================================================
EXPLANATIONS = {
    # -------- 08-functions.html --------
    "def add(a, b):": "add নামে একটি ফাংশন তৈরি করা হচ্ছে যা দুটি প্যারামিটার a ও b গ্রহণ করবে",
    "    return a + b": "a ও b-এর যোগফল ফাংশন থেকে ফেরত দেওয়া হচ্ছে; type hint থাকলেও runtime-এ সেটা enforce হয় না শুধু linting ও documentation-এর জন্য কাজ করে",
    "print(add(10, 20))": "add ফাংশনকে 10 ও 20 argument দিয়ে কল করে এর ফলাফল 30 কনসোলে প্রিন্ট করা হচ্ছে",

    'def greet(name, message="Welcome"):': "greet নামের ফাংশন তৈরি করা হচ্ছে; name মান্ডেটরি আর message-এর default value Welcome",
    '    return f"{message}, {name}!"': "f-string ব্যবহার করে message ও nameকে যুক্ত করে একটি স্বাগত বার্তা ফেরত দেওয়া হচ্ছে",
    'print(greet("Renco"))': "শুধু name দিয়ে greet কল করা হচ্ছে message default হবে → Welcome, Renco!",
    'print(greet("Renco", message="Good morning"))': "keyword argument দিয়ে message স্পষ্টভাবে Good morning সেট করে কল করা হচ্ছে",

    "def report(*scores, **info):": "*scores ব্যবহার করে যত খুশি positional argument tuple হিসেবে নেয়া; **info দিয়ে keyword args dict হিসেবে ধরা হচ্ছে",
    "    print(scores)": "সব positional argument দিয়ে তৈরি scores tuple টি প্রিন্ট করা হচ্ছে",
    "    print(info)": "সব keyword argument দিয়ে তৈরি info dictionary টি প্রিন্ট করা হচ্ছে",
    "report(80,90,name=\"Renco\")": "80, 90 positional + name=Renco keyword argument দিয়ে report ফাংশন কল করা হচ্ছে",

    "def factorial(n):": "factorial নামের রিকার্সিভ ফাংশন তৈরি করা হচ্ছে যা n ইনপুট নেবে",
    "    if n <= 1:": "base case check: n যদি 1 বা তার কম হয় তাহলে recursion বন্ধ হবে",
    "        return 1": "base case-এ 1 ফেরত দেওয়া হচ্ছে কারণ 0! = 1 এবং 1! = 1",
    "    return n * factorial(n-1)": "n কে n-1 এর factorial-এর সাথে গুণ করে ফেরত দেওয়া রিকার্সিভ স্টেপ",
    "print(factorial(5))": "5 এর ফ্যাক্টোরিয়াল 120 প্রিন্ট করা হচ্ছে",

    # -------- 09-modules-packages.html --------
    "import math": "Python-এর standard library থেকে math মডিউলটি import লোড করা হচ্ছে",
    "print(math.sqrt(144))": "math মডিউলের sqrt function দিয়ে 144-এর বর্গমূল 12 প্রিন্ট করা হচ্ছে",

    "# tools.py": "এটি comment: এই কোডটি tools.py নামের ফাইলে লিখতে হবে মডিউল ফাইল হিসেবে",
    "def double(x):": "tools.py-এ double নামের ফাংশন তৈরি করা হচ্ছে যা x ইনপুট নেবে",
    "    return x * 2": "x-এর মানকে দ্বিগুণ করে ফেরত দেওয়া হচ্ছে",
    "# main.py": "এটি comment: এই কোডটি main.py নামের আলাদা ফাইলে লিখতে হবে",
    "from tools import double": "tools.py module থেকে শুধু double function টা import করা হচ্ছে",
    "print(double(8))": "import করা double function-এ 8 দিয়ে কল করে ফলাফল 16 প্রিন্ট করা হচ্ছে",

    "python -m venv .venv": "venv module ব্যবহার করে .venv নামে একটি নতুন virtual environment তৈরি করা হচ্ছে",
    "# Windows PowerShell": "comment: নিচের কমান্ডটি Windows PowerShell-এ চালাতে হবে",
    ".venv\\Scripts\\Activate.ps1": "PowerShell-এ .venv virtual environment activate করা হচ্ছে",
    "pip install requests": "activate করা environment-এ requests প্যাকেজটি pip দিয়ে ইনস্টল করা হচ্ছে",

    # -------- 10-files-json-csv.html --------
    'with open("notes.txt", "w", encoding="utf-8") as f:': "notes.txt ফাইলকে write mode w-এ UTF-8 encoding দিয়ে খোলা হচ্ছে; with block শেষে auto-close হবে; file object f নামে refer করা হবে",
    '    f.write("Hello Python")': "খোলা ফাইলে Hello Python লেখা লিখে দেওয়া হচ্ছে",

    'with open("notes.txt", "r", encoding="utf-8") as f:': "notes.txt ফাইলকে read mode r-এ UTF-8 encoding দিয়ে খোলা হচ্ছে; file object = f",
    "    content = f.read()": "ফাইলের সম্পূর্ণ কনটেন্ট একবারে পড়ে content variable-এ সংরক্ষণ করা হচ্ছে",
    "print(content)": "ফাইল থেকে পড়া কনটেন্ট কনসোলে প্রিন্ট করা হচ্ছে",

    "import json": "Python-এর built-in JSON module টি import করা হচ্ছে JSON serialization/deserialization-এর জন্য",
    'data={"name":"Renco","skills":["Python","React"]}': "একটি nested Python dictionary তৈরি করা হচ্ছে যেখানে name string আর skills list",
    'text=json.dumps(data, indent=2)': "Python dict কে JSON string-এ রূপান্তর serialize করা হচ্ছে; indent=2 দিয়ে pretty-formatted JSON তৈরি",
    "print(text)": "pretty-formatted JSON string টি কনসোলে প্রিন্ট করা হচ্ছে",

    "import csv": "Python-এর built-in CSV module টি import করা হচ্ছে CSV file পড়ার জন্য",
    'with open("students.csv", newline="", encoding="utf-8") as f:': "students.csv ফাইল read mode-এ UTF-8 দিয়ে খোলা; newline='' CSV module-এর জন্য recommended",
    "    for row in csv.DictReader(f):": "DictReader দিয়ে CSV-এর প্রতিটি row কে dictionary হিসেবে iterate করা হচ্ছে; header key হিসেবে কাজ করবে",
    '        print(row["name"])': "প্রতিটি row dictionary থেকে name key-এর value বের করে প্রিন্ট করা হচ্ছে",

    # -------- 11-exceptions-debugging.html --------
    "numbers = [1,2]": "দুটি উপাদান index 0, 1 সম্বলিত একটি list তৈরি করে numbers variable-এ assign করা হচ্ছে",
    "print(numbers[5])": "numbers list-এর index 5 access করার চেষ্টা যা exist করে না → IndexError exception হবে",

    "try:": "try block শুরু: এখানের কোড error-এর জন্য monitor করা হবে",
    '    n=int(input("Number: "))': "user থেকে input নিয়ে integer-এ convert করে n variable-এ রাখা হচ্ছে; ভুল input দিলে ValueError",
    "    print(10/n)": "10 কে n দিয়ে ভাগ করে ফলাফল প্রিন্ট করা হচ্ছে; n=0 হলে ZeroDivisionError",
    "except ValueError:": "ValueError type-এর exception ধরার জন্য except block শুরু",
    '    print("Enter an integer")': "যদি ValueError হয় ইনপুট সংখ্যা না তাহলে এই error message প্রিন্ট করা",
    "except ZeroDivisionError:": "ZeroDivisionError type-এর exception ধরার জন্য আলাদা except block",
    '    print("Zero is not allowed")': "যদি n=0 দিয়ে ভাগ করা হয় তাহলে এই warning প্রিন্ট করা হচ্ছে",

    "def withdraw(balance, amount):": "withdraw নামের ফাংশন তৈরি; balance আগের টাকা ও amount তোলা পরিমাণ প্যারামিটার",
    "    if amount > balance:": "check করা হচ্ছে: তোলার পরিমাণ কি আগের ব্যালেন্সের চেয়ে বেশি?",
    '        raise ValueError("Insufficient balance")': "যদি টাকা কম থাকে স্পষ্টভাবে ValueError exception throw করা হচ্ছে বার্তা সহ",
    "    return balance-amount": "সব ঠিক থাকলে নতুন ব্যালেন্স বিয়োগ করে ফেরত দেওয়া হচ্ছে",

    "try:": "exception monitoring-এর জন্য আবার try block শুরু",
    "    print(10/2)": "10 কে 2 দিয়ে ভাগ ফলাফল 5 প্রিন্ট করা হচ্ছে এখানে কোনো error হবে না",
    "finally:": "finally block: error হোক বা না হোক অবশ্যই চালানো হবে",
    '    print("Cleanup")': "resource cleanup ফাইল বন্ধ connection বন্ধ ইত্যাদি নিজে কাজের example হিসেবে Cleanup প্রিন্ট করা হচ্ছে",

    # -------- 12-oop.html --------
    "class Student:": "Student নামে একটি নতুন class blueprint তৈরি করা হচ্ছে",
    "    def __init__(self, name):": "constructor method __init__ যা প্রতিটি নতুন object তৈরির সময় auto-call হয়; self = নিজের object, name = parameter",
    "        self.name = name": "পাঠানো name value কে object-এর instance attribute হিসেবে সংরক্ষণ করা হচ্ছে self.name",
    's = Student("Renco")': "Student class থেকে Renco নাম দিয়ে একটি নতুন object instance তৈরি করে s variable-ে রাখা হচ্ছে",
    "print(s.name)": "s object-এর name attribute বের করে প্রিন্ট করা হচ্ছে → Renco",

    "class Student:": "আবার Student class declare করা হচ্ছে এখানে এক লাইনে কম্প্যাক্ট",
    "    def __init__(self,name): self.name=name": "constructor: পাঠানো name কে object-এর self.name attribute এ সেট করা এক লাইনে",
    '    def introduce(self): return f"I am {self.name}"': "instance method introduce: self.name ব্যবহার করে পরিচিতির বার্তা ফেরত দেয়",
    'print(Student("Renco").introduce())': "অ্যানোনিমাস Student object তৈরি করে এর introduce method কল করে return value প্রিন্ট → I am Renco",

    "class Animal:": "Animal নামের parent base class তৈরি করা হচ্ছে",
    '    def speak(self): return "sound"': "Animal class-এর speak method সাধারণ sound ফেরত দেয়",
    "class Dog(Animal):": "Dog নামের child class তৈরি করা হচ্ছে যা Animal class থেকে inherit করছে parenthesis-এ parent নাম",
    '    def speak(self): return "woof"': "method overriding: Dog-এর নিজের speak parent-এর speak কে replace করে woof ফেরত দেয়",
    "print(Dog().speak())": "Dog object তৈরি করে এর speak কল → woof parent-এর নয় override করা কাজ করছে",

    "from abc import ABC, abstractmethod": "abc module থেকে ABC base class ও abstractmethod decorator import করা হচ্ছে abstract class তৈরি করার জন্য",
    "class Shape(ABC):": "Shape নামের abstract class তৈরি করা হচ্ছে ABC inherit করে → direct object তৈরি করা যাবে না",
    "    @abstractmethod": "নিচের method টি abstract method ঘোষণা করা হচ্ছে — সব child class-এ অবশ্যই implement করতে হবে",
    "    def area(self): pass": "area method-এর abstract signature — implementation নেই pass = no-op placeholder",
    "class Square(Shape):": "Square child class তৈরি করা হচ্ছে যা abstract Shape class কে inherit করেছে",
    "    def __init__(self,s): self.s=s": "Square-এর constructor: side length s নিয়ে self.s হিসেবে সংরক্ষণ",
    "    def area(self): return self.s*self.s": "Shape-এর abstract area method implement করা হয়েছে: বর্গক্ষেত্রের ক্ষেত্রফল = বাহু × বাহু",
    "print(Square(4).area())": "বাহু 4 এর Square object তৈরি করে area কল → 4*4 = 16 প্রিন্ট হবে",

    # -------- 13-pythonic-intermediate.html --------
    "first, *middle, last = [1,2,3,4]": "extended unpacking: প্রথমটা first, শেষটা last, আর মাঝের সবগুলো *middle দিয়ে list হিসেবে ধরা হচ্ছে → first=1, middle=[2,3], last=4",
    "print(first, middle, last)": "unpack করা তিনটি value প্রিন্ট করা হচ্ছে → 1 [2, 3] 4",

    "def countdown(n):": "countdown নামের generator function তৈরি যা n থেকে 1 পর্যন্ত সংখ্যা yield করবে",
    "    while n:": "n যতক্ষণ truthy 0 ছাড়া থাকবে ততক্ষণ loop চালিয়ে যাওয়া হচ্ছে",
    "        yield n": "yield: generator-এর মূল কাজ — বর্তমান n value ফেরত দেয় এবং function execution পজ করে রাখে পরে আবার resume করা যায়",
    "        n -= 1": "n এর মান 1 করে কমানো হচ্ছে next iteration-এর জন্য",
    "print(list(countdown(3)))": "countdown 3 generator কে list দিয়ে exhaust করে সব yield value → [3, 2, 1] প্রিন্ট করা হচ্ছে",

    "def log_call(fn):": "log_call নামের decorator function তৈরি যা একটি function fn কে input নেবে",
    "    def wrapper(*args, **kwargs):": "wrapper inner function যা original fn-এর আগে পরে এক্সট্রা কাজ করবে; *args/**kwargs দিয়ে সব ধরনের argument support",
    '        print("Calling", fn.__name__)': "original function কল করার আগে Calling + function-এর নাম প্রিন্ট করা হচ্ছে লগিং",
    "        return fn(*args, **kwargs)": "original fn কে তার সব argument সহ কল করে তার return value-টা wrapper থেকেই ফেরত দেওয়া হচ্ছে",
    "    return wrapper": "decorator-এর শেষে নতুন wrapper function-টা ফেরত দেওয়া হচ্ছে এটাই original fn-কে replace করবে",
    "@log_call": "decorator syntax: @log_call লিখলে hello function টা auto হিসেবে hello = log_call hello হয়ে যাবে",
    'def hello(): return "Hi"': "hello নামের simple function যা শুধু Hi string ফেরত দেয়",
    "print(hello())": "এখন hello আসলে wrapper → আগে Calling hello প্রিন্ট হবে, তারপর Hi প্রিন্ট হবে",

    'with open("notes.txt", encoding="utf-8") as f:': "notes.txt ফাইলকে default read mode-এ UTF-8 encoding দিয়ে খোলা হচ্ছে; with statement context manager হিসেবে কাজ করছে",
    "    text=f.read()": "খোলা file object f থেকে সম্পূর্ণ content পড়ে text variable-এ সংরক্ষণ করা হচ্ছে; block শেষে file auto-close হবে",

    # -------- 14-typing-testing-clean-code.html --------
    # NOTE: The LINEBOX uses HTML-escaped form "def add(a: int, b: int) -&gt; int:" so we key both
    "def add(a: int, b: int) -> int:": "add function-এ type hint দেওয়া: a ও b উভয় int expected; function return-ও int হবে",
    "def add(a: int, b: int) -&gt; int:": "add function-এ type hint দেওয়া: a ও b উভয় int expected; function return-ও int হবে",
    # Note: "    return a + b" explanation already present under 08-functions (combined, all contexts)

    "def add(a,b): return a+b": "সাধারণ add function: দুটি input যোগ করে ফেরত দেয়",
    "assert add(2,3) == 5": "assertion: add 2+3 == 5 হলে শান্ত থাকবে; না হলে AssertionError raise করবে টেস্ট হিসেবে",

    "import logging": "Python-এর built-in logging module import করা হচ্ছে",
    "logging.basicConfig(level=logging.INFO)": "logging basic configure করা: INFO level INFO, WARNING, ERROR, CRITICAL দেখানো শুরু করো",
    'logging.info("Application started")': "INFO severity-এ একটি log message emit করা হচ্ছে: Application started",

    "project/": "project নামের root folder টি দেখানো হচ্ছে directory",
    "  src/": "source code রাখার জন্য src sub-folder library/app code এখানে",
    "  tests/": "unit/integration tests রাখার জন্য tests sub-folder",
    "  README.md": "প্রজেক্ট ডকুমেন্টেশনের জন্য README markdown ফাইল",
    "  pyproject.toml": "modern Python project config file build system, dependencies, tool config সব এখানে",

    # -------- 15-http-apis-automation.html --------
    "import requests": "popular third-party requests library import করা হচ্ছে HTTP request করার জন্য সবচেয়ে বেশি ব্যবহৃত",
    'r=requests.get("https://api.github.com", timeout=10)': "GitHub API-এ GET request পাঠানো হচ্ছে; 10 সেকেন্ডের timeout সহ; response object r-এ save",
    "print(r.status_code)": "HTTP response-এর status code প্রিন্ট করা হচ্ছে সফল হলে 200, error হলে 4xx/5xx",

    "data=r.json()": "previous response object r-এর json method দিয়ে JSON response body কে Python dict/list-এ parse করা হচ্ছে",
    "print(type(data))": "parse করা data-এর data type কী সাধারণত dict সেটা print করে দেখানো হচ্ছে",
    "print(data.keys())": "dictionary data-এর সব key গুলো top-level keys print করা হচ্ছে",

    'payload={"name":"Renco"}': "POST request-এ পাঠানোর জন্য payload dictionary তৈরি করা হচ্ছে: name → Renco",
    'r=requests.post("https://httpbin.org/post", json=payload, timeout=10)': "httpbin.org/post endpoint-এ POST request; json=payload auto serialize+Content-Type application/json set করে",
    "print(r.status_code)": "POST request-এর HTTP status code প্রিন্ট করা হচ্ছে সফল হলে 200",

    "from pathlib import Path": "pathlib module থেকে modern Path class import করা হচ্ছে object-oriented file system path handling-এর জন্য",
    'for p in Path(".").glob("*.txt"):': "বর্তমান directory .-তে glob pattern *.txt সব .txt ফাইল দিয়ে iterate করা হচ্ছে",
    '    print("Found:",p.name)': "পাওয়া প্রতিটি .txt ফাইলের শুধু নাম p.name প্রিন্ট করা হচ্ছে Found: prefix-এর সাথে",
}

def build_lookup():
    lu = {}
    for k, v in EXPLANATIONS.items():
        for variant in (k, k.strip(), html_escape(k), html_escape(k.strip()),
                        html_unescape(k), html_unescape(k.strip())):
            lu[variant] = v
    return lu
LOOKUP = build_lookup()

def find_explanation(code_text_raw):
    for t in (code_text_raw, code_text_raw.strip(),
              html_unescape(code_text_raw), html_unescape(code_text_raw.strip())):
        if t in LOOKUP:
            return LOOKUP[t]
    return ""


# =====================================================================
# PIPELINE STEPS
# =====================================================================
def process_lineboxes(html):
    inner_pattern = re.compile(r'<div>\s*(<code>([\s\S]*?)</code>)\s*</div>')

    def process_one_inner(im):
        code_full = im.group(1)
        code_text_raw = im.group(2)
        expl = find_explanation(code_text_raw)
        if not expl:
            print(f"    WARN: no explanation for code: {repr(html_unescape(code_text_raw.strip())[:90])}")
            return im.group(0)
        return f"<div>{code_full}<span class=\"ln-text\">{expl}</span></div>"
    return inner_pattern.sub(process_one_inner, html)


def add_structural_comments(html):
    cm = re.search(r"<title>(.*?)</title>", html)
    title = cm.group(1).strip() if cm else "Unknown Chapter"
    fc = (
        "<!-- ============================================================ -->\n"
        "<!--  ORIGINAL CONTENT LOCKED: IDs, hrefs, text সবই 100% অপরিবর্তনীয়   -->\n"
        "<!--  এই ফাইলে শুধুমাত্র: (i) সঠিক indentation, (ii) structural     -->\n"
        "<!--  বাংলা কমেন্ট, এবং (iii) .linebox-এর প্রতি লাইনে ln-text span   -->\n"
       f"<!--  যোগ করা হয়েছে। অধ্যায়: {title} -->\n"
        "<!-- ============================================================ -->"
    )
    def s1(pat, repl):
        return re.sub(pat, repl, html, count=1)

    html = s1(r"(<!doctype html>)", r"\1\n" + fc)
    html = s1(r"(<head>)", r'\1\n<!-- ============ <head> শুরু: meta/title/CSS যুক্তকরণ ============ -->')
    html = s1(r"(</head>)", r'<!-- ============ </head> শেষ: head block সম্পন্ন ================= -->\n\1')
    html = s1(r"(<body>)", r'\1\n<!-- ============ <body> শুরু + .top (scroll progress bar) ========= -->')
    html = s1(r'(<nav>)', r'<!-- ============ <nav> শুরু: টপ নেভিগেশন বার (Home + Contents) ========= -->\n\1')
    html = s1(r'(</nav>)', r'\1\n<!-- ============ </nav> শেষ: নেভিগেশন বার সম্পন্ন ================== -->')
    html = s1(r'(<main class="wrap reader">)', r'<!-- ============ <main.wrap.reader> শুরু: পাঠকের মূল কনটেন্ট এরিয়া === -->\n\1')
    html = s1(r'(<aside class="toc">)', r'<!-- ============ <aside.toc> শুরু: টেবিল অফ কনটেন্ট সাইডবার ===== -->\n\1')
    html = s1(r'(</aside>)', r'\1\n<!-- ============ </aside.toc> শেষ: TOC sidebar সম্পন্ন ========= -->')
    html = s1(r'(<article class="article">)', r'<!-- ============ <article.article> শুরু: অধ্যায়ের মূল লেখা + কোড == -->\n\1')

    def topic_c(m):
        full = m.group(0)
        inner = re.search(r"<h2[^>]*>([\s\S]*?)</h2>", full)
        heading = inner.group(1).strip() if inner else "Topic"
        return f'<!-- -------- Topic section: {heading} -------- -->\n{full}'
    html = re.sub(r'<h2 id="topic\d+"[\s\S]*?</h2>', topic_c, html)

    html = re.sub(r'(<div class="code">)', r'<!-- code/copy block: Copy বাটন সহ প্রদর্শনীয় কোড snippet -->\n\1', html)
    html = re.sub(r'(<div class="definition">)', r'<!-- definition callout: সহজ ভাষায় ধারণার সংক্ষিপ্ত সংজ্ঞা -->\n\1', html)
    html = re.sub(r'(<div class="tip">)', r'<!-- tip callout: practical টিপস / পরামর্শ -->\n\1', html)
    html = re.sub(r'(<div class="why">)', r'<!-- why callout: কেন কাজ করছে — intuitive ব্যাখ্যা -->\n\1', html)
    html = re.sub(r'(<div class="linebox">)', r'<!-- linebox: প্রতিটি কোড লাইনের পাশে বাংলায় লাইনওয়াইজ ব্যাখ্যা (ln-text span) -->\n\1', html)

    html = s1(r'(<h2 id="practice">)', r'<!-- ============ Practice Lab শুরু: বাস্তব অনুশীলন এরিয়া ============ -->\n\1')
    html = s1(r'(<div class="exercise">)', r'<!-- exercise box: 3 স্তরের (Beginner/Intermediate/Challenge) অনুশীলন -->\n\1')
    html = s1(r'(<h2 id="check">)', r'<!-- ============ Self Check: পরবর্তী অধ্যায়ে যাওয়ার আগে মূল্যায়ন == -->\n\1')
    html = s1(r'(<div class="pager">)', r'<!-- pager buttons: Previous / Colab / Next navigation বাটন সমূহ -->\n\1')
    html = s1(r'(</article>)', r'<!-- ============ </article.article> শেষ: অধ্যায়ের কনটেন্ট সম্পন্ন = -->\n\1')
    html = s1(r'(</main>)', r'<!-- ============ </main.wrap.reader> শেষ: reader layout সম্পন্ন ====== -->\n\1')
    html = s1(r'(<footer class="footer">)', r'<!-- ============ <footer> শুরু: পেজের নিচের কপিরাইট / রেফারেন্স === -->\n\1')
    html = s1(r'(</footer>)', r'\1\n<!-- ============ </footer> শেষ: footer সম্পন্ন ====================== -->')
    html = s1(r'(<script src="../assets/app.js"></script>)', r'<!-- script ref: app.js — progress bar, copy btn, TOC scroll spy ইত্যাদি interactive features -->\n\1')
    return html


# =====================================================================
# PRETTIFY with VERBATIM-BLOCK PLACEHOLDERS (protects <pre> AND .linebox)
# =====================================================================
VOID_TAGS = {
    'area','base','br','col','embed','hr','img','input','link','meta',
    'param','source','track','wbr','!doctype'
}

def save_verbatim(html):
    saved = []

    pre_pat = re.compile(r'<pre[\s\S]*?</pre>', re.IGNORECASE)
    def pre_repl(m, saved=saved):
        saved.append(m.group(0))
        return f"___VERBATIM_{len(saved)-1}___"
    html = pre_pat.sub(pre_repl, html)

    lb_open = '<div class="linebox">'
    i = 0
    out = []
    while True:
        idx = html.find(lb_open, i)
        if idx == -1:
            out.append(html[i:])
            break
        out.append(html[i:idx])
        start = idx
        depth = 1
        j = idx + len(lb_open)
        while j < len(html) and depth > 0:
            nxt_o = html.find('<div', j)
            nxt_c = html.find('</div>', j)
            if nxt_c == -1:
                break
            if nxt_o != -1 and nxt_o < nxt_c:
                depth += 1
                j = nxt_o + 4
            else:
                depth -= 1
                j = nxt_c + 6
        block = html[start:j]
        saved.append(block)
        out.append(f"___VERBATIM_{len(saved)-1}___")
        i = j
    html = ''.join(out)

    return html, saved

def restore_verbatim(html, saved):
    for i, b in enumerate(saved):
        html = html.replace(f"___VERBATIM_{i}___", b)
    return html

def tokenize_skel(html):
    pat = re.compile(r'<!--[\s\S]*?-->|<[^>]+>|[^<]+')
    for m in pat.finditer(html):
        t = m.group(0)
        if not t.strip():
            continue
        if t.startswith('<!'):
            yield ('comment', t)
        elif t.startswith('</'):
            yield ('closetag', t)
        elif t.startswith('<'):
            tm = re.match(r'<\s*([a-zA-Z0-9!?]+)', t)
            tn = tm.group(1).lower() if tm else ''
            if tn in VOID_TAGS or t.rstrip().endswith('/>'):
                yield ('selfclose', t)
            else:
                yield ('opentag', t)
        else:
            yield ('text', t)

def _tn(s, kind):
    if kind == 'closetag':
        tm = re.match(r'</\s*([a-zA-Z0-9]+)', s)
    else:
        tm = re.match(r'<\s*([a-zA-Z0-9]+)', s)
    return tm.group(1).lower() if tm else ''

def beautify_skel(html):
    INDENT = "    "
    stack = []
    out = []
    for tt, val in tokenize_skel(html):
        d = len(stack)
        pfx = INDENT * d
        if tt == 'comment':
            lines = val.split('\n')
            out.append(pfx + lines[0])
            for ln in lines[1:]:
                s = ln.strip()
                if s:
                    out.append(pfx + INDENT + s)
                else:
                    out.append('')
            continue
        if tt == 'text':
            s = val.strip()
            if s:
                out.append(pfx + s)
            continue
        if tt == 'selfclose':
            out.append(pfx + val)
            continue
        if tt == 'opentag':
            out.append(pfx + val)
            stack.append(_tn(val, 'opentag'))
            continue
        if tt == 'closetag':
            cn = _tn(val, 'closetag')
            while stack and stack[-1] != cn:
                stack.pop()
            if stack:
                stack.pop()
            nd = len(stack)
            out.append((INDENT * nd) + val)
            continue
    cleaned = []
    prev_empty = False
    for line in out:
        if line.strip() == '':
            if not prev_empty:
                cleaned.append('')
            prev_empty = True
        else:
            cleaned.append(line)
            prev_empty = False
    while cleaned and cleaned[-1].strip() == '':
        cleaned.pop()
    return '\n'.join(cleaned) + '\n'

def prettify(html):
    skel, saved = save_verbatim(html)
    pretty = beautify_skel(skel)
    return restore_verbatim(pretty, saved)


# =====================================================================
# FILE PROCESSING
# =====================================================================
FILES = [
    "08-functions.html",
    "09-modules-packages.html",
    "10-files-json-csv.html",
    "11-exceptions-debugging.html",
    "12-oop.html",
    "13-pythonic-intermediate.html",
    "14-typing-testing-clean-code.html",
    "15-http-apis-automation.html",
]

def process_file(fn):
    path = os.path.join(BASE, fn)
    print(f"Processing: {fn}")
    # Use EMBEDDED ORIGINAL — no more recovery artifacts!
    html = ORIGINALS[fn]
    # Step 1: ln-text spans
    html = process_lineboxes(html)
    # Step 2: structural Bangla comments
    html = add_structural_comments(html)
    # Step 3: indent / prettify (preserving pre blocks via placeholder)
    html = prettify(html)
    # Overwrite same path
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  OK Done: {fn}")

for fn in FILES:
    process_file(fn)
print("\nAll 8 chapter files processed successfully!")
