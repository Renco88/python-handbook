
const bar=document.querySelector('.top i');
addEventListener('scroll',()=>{if(bar){const d=document.documentElement;bar.style.width=(scrollY/(d.scrollHeight-innerHeight)*100)+'%'}});
document.querySelectorAll('.copy').forEach(b=>b.addEventListener('click',()=>{navigator.clipboard.writeText(b.parentElement.querySelector('code').innerText);b.textContent='Copied ✓';setTimeout(()=>b.textContent='Copy',900)}));
const s=document.querySelector('#search');if(s)s.addEventListener('input',()=>{const q=s.value.toLowerCase();document.querySelectorAll('.card').forEach(c=>c.style.display=c.innerText.toLowerCase().includes(q)?'block':'none')});
