// Micromouse floodfill simulator. Mirrors the firmware's Flood(): breadth-first search from the
// four centre cells over the walls the mouse KNOWS; the mouse moves to the open neighbour with the
// lowest distance, preferring straight, then right/left, then back.
// The competition maze is 16 x 16; the small decorative mazes use other grids to fill their frame.
(function(global){
  const DX=[0,1,0,-1], DY=[-1,0,1,0]; // 0=N 1=E 2=S 3=W (y grows down)
  const BIG=65535;
  function rng(seed){let s=seed>>>0||1;return()=>((s=Math.imul(s^s>>>15,s|1),s^=s+Math.imul(s^s>>>7,s|61),((s^s>>>14)>>>0))/4294967296)}
  const grid=(C,R,f)=>[...Array(C)].map((_,x)=>[...Array(R)].map((_,y)=>f(x,y)));

  function makeMaze(seed,C,R,goals){
    const r=rng(seed), w=grid(C,R,()=>[1,1,1,1]), seen=grid(C,R,()=>false);
    const gx=goals[0][0], gy=goals[0][1], isGoal=(x,y)=>(x===gx||x===gx+1)&&(y===gy||y===gy+1);
    const open=(x,y,d)=>{w[x][y][d]=0;w[x+DX[d]][y+DY[d]][(d+2)%4]=0};
    // the centre 2x2 is one open room with a single entrance
    open(gx,gy,1);open(gx,gy,2);open(gx+1,gy+1,0);open(gx+1,gy+1,3);
    goals.forEach(([x,y])=>seen[x][y]=true);
    const st=[[0,R-1]];seen[0][R-1]=true;
    while(st.length){const [x,y]=st[st.length-1];const opts=[];
      for(let d=0;d<4;d++){const nx=x+DX[d],ny=y+DY[d];if(nx>=0&&ny>=0&&nx<C&&ny<R&&!seen[nx][ny])opts.push(d)}
      if(!opts.length){st.pop();continue}const d=opts[Math.floor(r()*opts.length)];open(x,y,d);seen[x+DX[d]][y+DY[d]]=true;st.push([x+DX[d],y+DY[d]])}
    const ent=[[gx,gy,0],[gx+1,gy,0],[gx+1,gy,1],[gx+1,gy+1,1],[gx+1,gy+1,2],[gx,gy+1,2],[gx,gy+1,3],[gx,gy,3]][Math.floor(r()*8)];open(...ent);
    // a few loops so the shortest path is not trivial
    for(let k=0;k<Math.round(26*C*R/256);k++){const x=1+Math.floor(r()*(C-2)),y=1+Math.floor(r()*(R-2)),d=Math.floor(r()*4);
      if(!isGoal(x,y)&&!isGoal(x+DX[d],y+DY[d]))open(x,y,d)}
    return w;
  }

  function Sim(seed,C,R){
    C=this.C=C||16; R=this.R=R||16;
    const gx=C/2-1, gy=R/2-1;
    this.goals=[[gx,gy],[gx,gy+1],[gx+1,gy],[gx+1,gy+1]];
    this.real=makeMaze(seed,C,R,this.goals);
    this.known=grid(C,R,(x,y)=>[y===0?1:0,x===C-1?1:0,y===R-1?1:0,x===0?1:0]);
    this.dist=grid(C,R,()=>BIG); this.visited=grid(C,R,()=>false);
    this.x=0;this.y=R-1;this.h=0;this.phase='explore';this.steps=0;this.trail=[[0,R-1]];this.runPath=null;this.target='goal';
    this.sense();this.flood();
  }
  Sim.prototype.isGoal=function(x,y){const g=this.goals[0];return(x===g[0]||x===g[0]+1)&&(y===g[1]||y===g[1]+1)};
  Sim.prototype.inside=function(x,y){return x>=0&&y>=0&&x<this.C&&y<this.R};
  Sim.prototype.setWall=function(x,y,d){this.known[x][y][d]=1;const nx=x+DX[d],ny=y+DY[d];if(this.inside(nx,ny))this.known[nx][ny][(d+2)%4]=1};
  Sim.prototype.sense=function(){this.visited[this.x][this.y]=true;for(let d=0;d<4;d++)if(this.real[this.x][this.y][d])this.setWall(this.x,this.y,d)};
  // Flood(): the same logic as the firmware listing, generalised to any target set
  Sim.prototype.flood=function(targets){
    const q=[];for(let i=0;i<this.C;i++)for(let j=0;j<this.R;j++)this.dist[i][j]=BIG;
    (targets||this.goals).forEach(([x,y])=>{this.dist[x][y]=0;q.push([x,y])});
    while(q.length){const [x,y]=q.shift();
      for(let d=0;d<4;d++){const nx=x+DX[d],ny=y+DY[d];
        if(!this.inside(nx,ny))continue; if(this.known[x][y][d]===1)continue;
        if(this.dist[nx][ny]>this.dist[x][y]+1){this.dist[nx][ny]=this.dist[x][y]+1;q.push([nx,ny])}}}
  };
  Sim.prototype.targets=function(){return this.target==='goal'?this.goals:[[0,this.R-1]]};
  Sim.prototype.step=function(){
    if(this.phase==='done')return false;
    if(this.phase==='run'){ if(this.runIdx<this.runPath.length-1){this.runIdx++;const [nx,ny]=this.runPath[this.runIdx];
        for(let d=0;d<4;d++)if(this.x+DX[d]===nx&&this.y+DY[d]===ny)this.h=d; this.x=nx;this.y=ny;return true} this.phase='done';return false;}
    const here=this.dist[this.x][this.y];
    if(here===0){ // reached the target
      if(this.target==='goal'){this.target='start';this.phase='return';this.flood(this.targets());return true}
      // back at the start: plan the speed run on known walls only
      this.flood(this.goals);this.phase='run';this.runPath=[[this.x,this.y]];let cx=this.x,cy=this.y;
      while(this.dist[cx][cy]>0){let moved=false;for(let d=0;d<4;d++){const nx=cx+DX[d],ny=cy+DY[d];if(!this.known[cx][cy][d]&&this.inside(nx,ny)&&this.dist[nx][ny]===this.dist[cx][cy]-1){cx=nx;cy=ny;moved=true;break}}if(!moved)break;this.runPath.push([cx,cy])}
      this.runIdx=0;this.trail=[];return true;
    }
    const pref=[this.h,(this.h+1)%4,(this.h+3)%4,(this.h+2)%4];let best=-1,bd=BIG;
    for(const d of pref){if(this.known[this.x][this.y][d])continue;const nx=this.x+DX[d],ny=this.y+DY[d];if(this.dist[nx][ny]<bd){bd=this.dist[nx][ny];best=d}}
    if(best<0)return false;
    this.h=best;this.x+=DX[best];this.y+=DY[best];this.steps++;this.trail.push([this.x,this.y]);
    this.sense();this.flood(this.targets());return true;
  };

  // Colours come from the page's design tokens, read on the canvas itself so a dark band or theme applies.
  function draw(ctx,sim,W,opt){
    opt=opt||{};const C=sim.C,R=sim.R,c=W/C,H=c*R, css=getComputedStyle(ctx.canvas);
    const col=(k,f)=>css.getPropertyValue(k).trim()||f;
    const ink=col('--ink','#111315'), ink3=col('--ink-3','#7f848b'), accent=col('--accent','#ff4d1a'), blue=col('--blue','#1846c9');
    ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle=col('--sheet','#f8f6f0');ctx.fillRect(0,0,ctx.canvas.width,ctx.canvas.height);
    ctx.translate(opt.ox||0,opt.oy||0);
    let max=1;for(let x=0;x<C;x++)for(let y=0;y<R;y++){const v=sim.dist[x][y];if(v<BIG&&v>max)max=v}
    const nums=opt.numbers&&c>=26; if(nums){ctx.font=`500 ${Math.floor(c*.3)}px "IBM Plex Mono",ui-monospace,monospace`;ctx.textAlign='center';ctx.textBaseline='middle'}
    for(let x=0;x<C;x++)for(let y=0;y<R;y++){
      const d=sim.dist[x][y];
      if(d<BIG){ctx.globalAlpha=0.02+0.2*(1-d/max);ctx.fillStyle=ink;ctx.fillRect(x*c,y*c,c,c);ctx.globalAlpha=1}
      if(sim.isGoal(x,y)){ctx.globalAlpha=.22;ctx.fillStyle=accent;ctx.fillRect(x*c,y*c,c,c);ctx.globalAlpha=1}
      if(nums&&d<BIG){ctx.fillStyle=ink3;ctx.fillText(d,x*c+c/2,y*c+c/2+1)}
    }
    const path=(pts)=>{ctx.beginPath();pts.forEach(([x,y],i)=>i?ctx.lineTo(x*c+c/2,y*c+c/2):ctx.moveTo(x*c+c/2,y*c+c/2));ctx.stroke()};
    ctx.lineJoin='round';ctx.lineCap='round';
    if(sim.trail.length>1){ctx.globalAlpha=.6;ctx.strokeStyle=blue;ctx.lineWidth=Math.max(1.5,c*.1);path(sim.trail);ctx.globalAlpha=1}
    if(sim.runPath){ctx.strokeStyle=accent;ctx.lineWidth=Math.max(2,c*.16);path(sim.runPath)}
    // walls: known walls in ink, hidden real walls faint
    ctx.lineCap='square';
    for(let x=0;x<C;x++)for(let y=0;y<R;y++)for(let d=0;d<4;d++){
      const k=sim.known[x][y][d], r=sim.real[x][y][d]; if(!r&&!k)continue; if(!k&&!opt.reveal)continue;
      ctx.globalAlpha=k?1:.4;ctx.strokeStyle=k?ink:ink3;ctx.lineWidth=k?Math.max(1.5,c*.075):1;
      ctx.beginPath();const X=x*c,Y=y*c;
      if(d===0){ctx.moveTo(X,Y);ctx.lineTo(X+c,Y)}if(d===1){ctx.moveTo(X+c,Y);ctx.lineTo(X+c,Y+c)}if(d===2){ctx.moveTo(X,Y+c);ctx.lineTo(X+c,Y+c)}if(d===3){ctx.moveTo(X,Y);ctx.lineTo(X,Y+c)}ctx.stroke();
    }
    ctx.globalAlpha=1;
    // the mouse
    ctx.save();ctx.translate(sim.x*c+c/2,sim.y*c+c/2);ctx.rotate(sim.h*Math.PI/2);ctx.fillStyle=accent;ctx.strokeStyle=ink;ctx.lineWidth=Math.max(1,c*.05);ctx.lineJoin='miter';
    ctx.beginPath();ctx.moveTo(0,-c*.34);ctx.lineTo(c*.27,c*.27);ctx.lineTo(-c*.27,c*.27);ctx.closePath();ctx.fill();ctx.stroke();ctx.restore();
    ctx.setTransform(1,0,0,1,0,0);
  }

  global.Micromouse={Sim,draw};

  // Decorative mazes that run on their own: the grid is chosen to fill the frame with square cells.
  function mini(cv){
    const ctx=cv.getContext('2d'), ROWS=10; let sim=null, cols=0, on=false, last=0, wait=0, geo={W:0,ox:0,oy:0};
    const seed=()=>Math.floor(Math.random()*1e9);
    const paint=()=>{if(sim)draw(ctx,sim,geo.W,{reveal:true,numbers:true,ox:geo.ox,oy:geo.oy})};
    // whole square cells only: as many columns as fit, centred in the frame
    const fit=()=>{const r=cv.getBoundingClientRect(); if(!r.width||!r.height)return;
      const dpr=Math.min(2,window.devicePixelRatio||1), n=Math.max(10,Math.min(26,2*Math.floor(ROWS*r.width/r.height/2+.02)));
      if(n!==cols||!sim){cols=n;sim=new Sim(seed(),cols,ROWS)}
      cv.width=Math.round(r.width*dpr);cv.height=Math.round(r.height*dpr);
      const c=Math.min(cv.width/cols,cv.height/ROWS); geo={W:c*cols,ox:(cv.width-c*cols)/2,oy:(cv.height-c*ROWS)/2}; paint()};
    const loop=t=>{if(!on)return; if(sim&&t-last>80){last=t;
        if(wait){if(t>wait){wait=0;sim=new Sim(seed(),cols,ROWS)}}
        else if(!sim.step())wait=t+1600;
        paint()}
      requestAnimationFrame(loop)};
    fit();window.addEventListener('resize',fit);
    if(document.fonts&&document.fonts.ready)document.fonts.ready.then(fit);
    const still=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
    if(still){for(let i=0;i<60&&sim;i++)sim.step();paint();return}
    new IntersectionObserver(es=>es.forEach(e=>{const was=on;on=e.isIntersecting;if(on&&!was){if(!sim)fit();requestAnimationFrame(loop)}}),{threshold:.05}).observe(cv);
  }
  const start=()=>document.querySelectorAll('canvas[data-mini]').forEach(mini);
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();
})(window);
