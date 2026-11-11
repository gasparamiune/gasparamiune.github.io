// Theme, filters, lightbox, lazy embeds, reveal-on-scroll.
(function(){
  const root=document.documentElement;
  try{const t=localStorage.getItem('theme'); if(t) root.dataset.theme=t;}catch(e){}
  document.querySelectorAll('.theme-btn').forEach(b=>b.addEventListener('click',()=>{
    const n=root.dataset.theme==='light'?'dark':'light'; root.dataset.theme=n; try{localStorage.setItem('theme',n)}catch(e){}
  }));

  // Reveal
  const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.08});
  document.querySelectorAll('.rv').forEach(el=>io.observe(el));

  // Project filters (category tabs + skill chips)
  const cards=[...document.querySelectorAll('.card[data-cat]')];
  if(cards.length){
    let cat='all', skill=null;
    const note=document.querySelector('.filter-note');
    const apply=()=>{
      let n=0;
      cards.forEach(c=>{
        const ok=(cat==='all'||c.dataset.cat===cat)&&(!skill||c.dataset.skills.split(' ').includes(skill));
        c.classList.toggle('hide',!ok); if(ok)n++;
      });
      document.querySelectorAll('[data-skill]').forEach(ch=>ch.classList.toggle('on',ch.dataset.skill===skill));
      if(note){
        if(skill){const lab=document.querySelector(`[data-skill="${skill}"]`)?.dataset.label||skill;
          note.innerHTML=`Showing ${n} project${n===1?'':'s'} that use <b>${lab}</b> · <button type="button">clear</button>`;
          note.querySelector('button').onclick=()=>{skill=null;apply()};}
        else note.textContent='';
      }
    };
    document.querySelectorAll('.filters button').forEach(b=>b.addEventListener('click',()=>{
      document.querySelectorAll('.filters button').forEach(x=>x.classList.remove('on')); b.classList.add('on'); cat=b.dataset.f; apply();
    }));
    document.querySelectorAll('[data-skill]').forEach(ch=>ch.addEventListener('click',()=>{
      skill=skill===ch.dataset.skill?null:ch.dataset.skill; apply();
      document.getElementById('projects').scrollIntoView({behavior:'smooth'});
    }));
  }

  // Lightbox
  const figs=[...document.querySelectorAll('.gallery figure')];
  if(figs.length){
    const lb=document.createElement('div'); lb.className='lb';
    lb.innerHTML='<button class="x" aria-label="Close">✕</button><button class="pv" aria-label="Previous">‹</button><img alt=""><p></p><button class="nx" aria-label="Next">›</button>';
    document.body.appendChild(lb); let i=0;
    const show=k=>{i=(k+figs.length)%figs.length;const f=figs[i];lb.querySelector('img').src=f.querySelector('img').src;lb.querySelector('img').alt=f.querySelector('img').alt;lb.querySelector('p').textContent=f.querySelector('figcaption')?.textContent||'';lb.classList.add('on')};
    figs.forEach((f,k)=>f.addEventListener('click',()=>show(k)));
    lb.querySelector('.x').onclick=()=>lb.classList.remove('on');
    lb.querySelector('.pv').onclick=e=>{e.stopPropagation();show(i-1)}; lb.querySelector('.nx').onclick=e=>{e.stopPropagation();show(i+1)};
    lb.addEventListener('click',e=>{if(e.target===lb)lb.classList.remove('on')});
    document.addEventListener('keydown',e=>{if(!lb.classList.contains('on'))return;if(e.key==='Escape')lb.classList.remove('on');if(e.key==='ArrowLeft')show(i-1);if(e.key==='ArrowRight')show(i+1)});
  }

  // Lazy live previews
  document.querySelectorAll('.embed [data-src]').forEach(b=>b.addEventListener('click',()=>{
    const st=b.closest('.stage'); const f=document.createElement('iframe'); f.src=b.dataset.src; f.loading='lazy';
    f.allow='fullscreen; accelerometer; gyroscope'; f.title='Live preview'; st.innerHTML=''; st.appendChild(f);
  }));

  // Play videos only when visible
  const vio=new IntersectionObserver(es=>es.forEach(e=>{const v=e.target; if(e.isIntersecting) v.play().catch(()=>{}); else v.pause();}),{threshold:.35});
  document.querySelectorAll('video[data-auto]').forEach(v=>vio.observe(v));
})();
