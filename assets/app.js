/* ============================================================
   Python Handbook — Main JavaScript
   ------------------------------------------------------------------
   এই ফাইলটিতে ৩টি core interactive feature implement করা আছে:
     1. Scroll Progress Bar (পেজের উপরের colored progress strip)
     2. Copy to Clipboard (code block-এর Copy বাটন)
     3. Chapter Search / Live Filter (TOC search box)
   ============================================================ */


/* ============================================================
   FEATURE 01: SCROLL PROGRESS BAR
   ------------------------------------------------------------------
   কাজ: User যত খানি নিচে scroll করবে, তত খানি উপরের .top i element-এর
   width বাড়বে (0% থেকে 100%)।
   Formula:
     scroll% = (বর্তমান scrollY) / (মোট document height - viewport height) × 100
   ============================================================ */

// Step 1: .top class-এর ভিতরের <i> element টা ধরে আনা (progress bar-র colored strip)
const bar = document.querySelector('.top i');

// Step 2: Browser window-এ scroll event listener যোগ করা
// প্রতিবার user scroll করলে এই function টি run হবে
addEventListener('scroll', () => {

    // যদি bar element টি exist করে (null না হয়
    if (bar) {
        // document.documentElement = <html> element (page-এর root)
        const d = document.documentElement;

        // scrollY = যতটুকু scroll হয়েছে (পেজের শুরু থেকে
        // scrollHeight = page-এর সম্পূর্ণ উচ্চতা
        // innerHeight = বর্তমান viewport-এর উচ্চতা
        // হিসাব: কত percent scroll হয়েছে সেটা বের করে bar-এর width হিসেবে set করা
        bar.style.width = (scrollY / (d.scrollHeight - innerHeight) * 100) + '%';
    }
});


/* ============================================================
   FEATURE 02: CODE BLOCK — COPY TO CLIPBOARD BUTTON
   ------------------------------------------------------------------
   কাজ: প্রতিটি .copy button-এ click করলে ঐ button-র parent (.code div)
   এর ভিতরের <code> বা <pre> এর text ক্লিপবোর্ডে copy হবে।
   তারপর button-র লেখা "Copy → "Copied ✓" হয়ে 900ms পর আবার "Copy" হয়ে যায়।
   ============================================================ */

// Document-এর সব .copy class-র element গুলোকে select করে প্রতিটার উপর click listener বসানো
document.querySelectorAll('.copy').forEach(b =>
    b.addEventListener('click', () => {

        // Clipboard API দিয়ে code-র text কপি করা
        // b.parentElement = .code div; ভিতরে <code> element-র innerText নেয়া
        navigator.clipboard.writeText(b.parentElement.querySelector('code, pre').innerText);

        // Button টেক্সট পরিবর্তন করে success message দেখানো
        b.textContent = 'Copied ✓';

        // 900 মিলিসেকেন্ড (0.9 সেকেন্ড) পর আবার আগের লেখায় ফিরিয়ে আনা
        setTimeout(() => b.textContent = 'Copy', 900);
    })
);


/* ============================================================
   FEATURE 03: CHAPTER LIVE SEARCH / FILTER
   ------------------------------------------------------------------
   কাজ: #search input box-এ কিছু লেখা হলে সব .card গুলোর মধ্যে খুঁজে
   শুধু মিল থাকা card গুলো দেখাবে, বাকিগুলো hide করবে।
   Case-insensitive search হয়েছে (toLowerCase())
   ============================================================ */

// Search input element টা ধরা
const s = document.querySelector('#search');

// যদি search input element টা পাওয়া যায় (landing page-এ থাকে, chapter page-এ নাও থাকতে পারে)
if (s)
    // input event: যখনই user কিছু type করবে বা মুছবে
    s.addEventListener('input', () => {
        // লেখাটাকে ছোট হাতের অক্ষরে রূপান্তরিত করা
        const q = s.value.toLowerCase();

        // সব .card element গুলোর উপর loop চালিয়ে check করা
        document.querySelectorAll('.card').forEach(c =>
            // card-এর ভেতরের সব innerText lowercase করে search query আছে কিনা check
            // includes() থাকলে true → display: block (দেখাও)
            // না থাকলে false → display: none (লুকাও)
            c.style.display = c.innerText.toLowerCase().includes(q) ? 'block' : 'none'
        );
    });


/* ============================================================
   FEATURE 04: TOC SCROLL SPY — Sidebar Active Link Highlight
   ------------------------------------------------------------------
   কাজ: Reader page-এ (chapter পেজ) user যখন scroll করবেন, তখন
   viewport-এ কোন section currently visible সেটা detect করে
   সংশ্লিষ্ট TOC link-এ .active class add করবে।

   পদ্ধতি: IntersectionObserver দিয়ে সব h2[id] heading গুলোকে observe করা
   যখন কোনো section 30% visible হবে, তার corresponding TOC link active হবে।
   ============================================================ */
document.addEventListener('DOMContentLoaded', () => {

    // TOC links এবং section headings দুটোই থাকলেই run করব
    const tocLinks = document.querySelectorAll('.toc a[href^="#"]');
    const headings = document.querySelectorAll('.article h2[id]');

    if (tocLinks.length && headings.length) {

        // প্রথমে সব TOC link থেকে .active সরাও
        const clearActive = () => tocLinks.forEach(a => a.classList.remove('active'));

        // নির্দিষ্ট id-র জন্য TOC link-এ .active দাও
        const setActiveById = (id) => {
            clearActive();
            const match = document.querySelector(`.toc a[href="#${id}"]`);
            if (match) match.classList.add('active');
        };

        // IntersectionObserver: scroll অনুযায়ী কোন heading এখন viewport-এ আছে detect
        const spyObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) setActiveById(entry.target.id);
            });
        }, {
            rootMargin: '-30% 0px -65% 0px',  // viewport-এর মাঝের 35% জায়গায় এলেই activate
            threshold: 0                        // যেকোনো অংশ visible হলেই fire
        });

        // সব h2[id] heading গুলোকে observe করা
        headings.forEach(h => spyObserver.observe(h));

        // TOC link-এ click করলেও সাথে সাথে সেটা active দেখাও (UX improvement)
        tocLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                const href = link.getAttribute('href');
                if (href && href.startsWith('#')) {
                    setTimeout(() => setActiveById(href.slice(1)), 50);
                }
            });
        });
    }

    /* ============================================================
       FEATURE 05: CODE BLOCK — Copy Button Fallback (Compatibility)
       ------------------------------------------------------------------
       কিছু পুরোনো browser বা file:// প্রোটোকলে navigator.clipboard
       কাজ করে না। সেক্ষেত্রে textarea select → execCommand("copy") দিয়ে
       copy করার fallback system যোগ করা হয়েছে।
       ============================================================ */
    document.querySelectorAll('.copy').forEach(btn => {
        // আগের event listener শুধু তখনই না কাজ করে, এখানে upgrade করছি
        btn.addEventListener('click', async () => {
            const codeEl = btn.parentElement.querySelector('code, pre');
            if (!codeEl) return;
            const text = codeEl.innerText;

            try {
                // প্রথমে modern Clipboard API দিয়ে copy করার চেষ্টা
                if (navigator.clipboard && window.isSecureContext) {
                    await navigator.clipboard.writeText(text);
                } else {
                    // Fallback: hidden textarea + legacy execCommand
                    const ta = document.createElement('textarea');
                    ta.value = text;
                    ta.style.position = 'fixed';
                    ta.style.left = '-9999px';
                    document.body.appendChild(ta);
                    ta.select();
                    document.execCommand('copy');
                    document.body.removeChild(ta);
                }
                btn.textContent = 'Copied ✓';
                setTimeout(() => btn.textContent = 'Copy', 1000);
            } catch (e) {
                btn.textContent = 'Copy failed';
                setTimeout(() => btn.textContent = 'Copy', 1500);
            }
        });
    });

});
