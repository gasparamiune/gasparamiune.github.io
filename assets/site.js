// Theme, reveal on scroll, filters, hero plate, lightbox, lazy live previews, videos.
(function(){
  const root=document.documentElement, $$=(s,el)=>[...(el||document).querySelectorAll(s)];

  // Theme: paper (default) or dark
  $$('.theme-btn').forEach(b=>b.addEventListener('click',()=>{
    const dark=root.dataset.theme!=='dark';
    if(dark)root.dataset.theme='dark';else delete root.dataset.theme;
    try{localStorage.setItem('theme',dark?'dark':'light')}catch(e){}
  }));

  // Reveal on scroll
  if('IntersectionObserver' in window){
    const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.06,rootMargin:'0px 0px -4% 0px'});
    $$('.rv').forEach(el=>io.observe(el));
  }else root.classList.add('ready');

  // Work filters: category buttons, plus a skill picked in the matrix
  const items=$$('[data-cat][data-skills]');
  if(items.length){
    let cat='all', skill=null; const note=document.querySelector('.fnote');
    const apply=()=>{
      let n=0;
      items.forEach(c=>{const ok=(cat==='all'||c.dataset.cat===cat)&&(!skill||c.dataset.skills.split(' ').includes(skill));c.classList.toggle('hide',!ok);if(ok){n++;c.classList.add('in')}});
      $$('tr[data-row]').forEach(r=>r.classList.toggle('on',r.dataset.row===skill));
      $$('.filters button').forEach(b=>b.classList.toggle('on',b.dataset.f===cat));
      if(note){
        if(skill){const lab=document.querySelector(`[data-skill="${skill}"]`).dataset.label;
          note.innerHTML=`Showing ${n} project${n===1?'':'s'} that use${n===1?'s':''} <b></b> <button type="button">Clear</button>`;
          note.querySelector('b').textContent=lab; note.querySelector('button').onclick=()=>{skill=null;apply()};}
        else note.textContent='';
      }
    };
    $$('.filters button').forEach(b=>b.addEventListener('click',()=>{cat=b.dataset.f;apply()}));
    $$('[data-skill]').forEach(b=>b.addEventListener('click',()=>{
      skill=skill===b.dataset.skill?null:b.dataset.skill; cat='all'; apply();
      if(skill)document.getElementById('work').scrollIntoView({behavior:'smooth'});
    }));
  }

  // Hero plate: rotate the real images
  const plate=document.querySelector('.plate');
  if(plate){
    const imgs=$$('.media img',plate), ticks=$$('.ticks i',plate), cap=plate.querySelector('.pc'), no=plate.querySelector('figcaption b'), link=plate.querySelector('a.media');
    let i=0, t=null;
    const show=k=>{i=(k+imgs.length)%imgs.length; imgs.forEach((m,j)=>m.classList.toggle('on',j===i)); ticks.forEach((m,j)=>m.classList.toggle('on',j===i));
      cap.textContent=imgs[i].dataset.cap; no.textContent='FIG. '+String(i+1).padStart(2,'0'); link.href=imgs[i].dataset.href};
    const go=()=>{clearInterval(t); t=setInterval(()=>show(i+1),4800)};
    if(!(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)&&imgs.length>1){
      imgs.forEach(m=>{m.loading='eager'}); go();
      plate.addEventListener('mouseenter',()=>clearInterval(t)); plate.addEventListener('mouseleave',go);
    }
  }

  // Lightbox for the figures
  const figs=$$('.figs .fig');
  if(figs.length){
    const lb=document.createElement('div'); lb.className='lb'; lb.setAttribute('role','dialog'); lb.setAttribute('aria-label','Figure viewer');
    lb.innerHTML='<button class="x" aria-label="Close">✕</button><button class="pv" aria-label="Previous">‹</button><img alt=""><p></p><button class="nx" aria-label="Next">›</button>';
    document.body.appendChild(lb); let i=0;
    const show=k=>{i=(k+figs.length)%figs.length;const f=figs[i],im=f.querySelector('img');lb.querySelector('img').src=im.currentSrc||im.src;lb.querySelector('img').alt=im.alt;const fc=f.querySelector('figcaption');lb.querySelector('p').textContent=fc.querySelector('b').textContent+' · '+fc.querySelector('span').textContent;lb.classList.add('on')};
    const close=()=>lb.classList.remove('on');
    figs.forEach((f,k)=>{f.addEventListener('click',()=>show(k));f.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();show(k)}})});
    lb.querySelector('.x').onclick=close;
    lb.querySelector('.pv').onclick=e=>{e.stopPropagation();show(i-1)}; lb.querySelector('.nx').onclick=e=>{e.stopPropagation();show(i+1)};
    lb.addEventListener('click',e=>{if(e.target===lb)close()});
    document.addEventListener('keydown',e=>{if(!lb.classList.contains('on'))return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')show(i-1);if(e.key==='ArrowRight')show(i+1)});
  }

  // Live previews load only when asked
  $$('.embed [data-src]').forEach(b=>b.addEventListener('click',()=>{
    const st=b.closest('.stage'), f=document.createElement('iframe'); f.src=b.dataset.src; f.loading='lazy';
    f.allow='fullscreen; accelerometer; gyroscope'; f.title='Live preview'; st.innerHTML=''; st.appendChild(f);
  }));

  // Videos play only while visible
  if('IntersectionObserver' in window){
    const vio=new IntersectionObserver(es=>es.forEach(e=>{const v=e.target; if(e.isIntersecting)v.play().catch(()=>{}); else v.pause()}),{threshold:.35});
    $$('video[data-auto]').forEach(v=>vio.observe(v));
  }

  // Table of contents: mark the section in view
  const toc=$$('.toc a[href^="#"]');
  if(toc.length&&'IntersectionObserver' in window){
    const map=new Map(toc.map(a=>[a.getAttribute('href').slice(1),a]));
    const so=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){toc.forEach(a=>a.classList.remove('on'));const a=map.get(e.target.id);if(a)a.classList.add('on')}}),{rootMargin:'-20% 0px -70% 0px'});
    map.forEach((a,id)=>{const s=document.getElementById(id);if(s)so.observe(s)});
  }
})();
