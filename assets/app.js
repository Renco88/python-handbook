
const bar=document.querySelector('.bar'); addEventListener('scroll',()=>{if(!bar)return;const d=document.documentElement;bar.style.width=(scrollY/(d.scrollHeight-innerHeight)*100)+'%'});
document.querySelectorAll('.copy').forEach(b=>b.onclick=()=>{const c=b.parentElement.querySelector('code');navigator.clipboard.writeText(c.innerText);b.textContent='Copied';setTimeout(()=>b.textContent='Copy',1000)});
const search=document.querySelector('#chapterSearch');if(search){search.oninput=()=>{const q=search.value.toLowerCase();document.querySelectorAll('.card').forEach(c=>c.style.display=c.innerText.toLowerCase().includes(q)?'block':'none')}}
