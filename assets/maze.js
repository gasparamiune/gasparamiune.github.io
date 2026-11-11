// Micromouse floodfill simulator. Mirrors the firmware's Flood(): BFS from the four
// centre cells over the walls the mouse KNOWS; the mouse moves to the open neighbour
// with the lowest distance, preferring straight, then right/left, then back.
(function(global){
  const N=16, DX=[0,1,0,-1], DY=[-1,0,1,0]; // 0=N 1=E 2=S 3=W (y grows down)
  const GOALS=[[7,7],[7,8],[8,7],[8,8]];
  const isGoal=(x,y)=>(x===7||x===8)&&(y===7||y===8);
  function rng(seed){let s=seed>>>0||1;return()=>((s=Math.imul(s^s>>>15,s|1),s^=s+Math.imul(s^s>>>7,s|61),((s^s>>>14)>>>0))/4294967296)}

  function makeMaze(seed){
    const r=rng(seed), w=[...Array(N)].map(()=>[...Array(N)].map(()=>[1,1,1,1]));
    const seen=[...Array(N)].map(()=>Array(N).fill(false));
    const open=(x,y,d)=>{w[x][y][d]=0;const nx=x+DX[d],ny=y+DY[d];w[nx][ny][(d+2)%4]=0};
    // centre 2x2 is one open room with a single entrance
    open(7,7,1);open(7,7,2);open(8,8,0);open(8,8,3);
    GOALS.forEach(([x,y])=>seen[x][y]=true);
    const st=[[0,N-1]];seen[0][N-1]=true;
    while(st.length){const [x,y]=st[st.length-1];const opts=[];
      for(let d=0;d<4;d++){const nx=x+DX[d],ny=y+DY[d];if(nx>=0&&ny>=0&&nx<N&&ny<N&&!seen[nx][ny])opts.push(d)}
      if(!opts.length){st.pop();continue}const d=opts[Math.floor(r()*opts.length)];open(x,y,d);seen[x+DX[d]][y+DY[d]]=true;st.push([x+DX[d],y+DY[d]])}
    // entrance into the goal room
    const ent=[[7,7,0],[8,7,0],[8,7,1],[8,8,1],[8,8,2],[7,8,2],[7,8,3],[7,7,3]][Math.floor(r()*8)];open(...ent);
    // a few loops so shortest path is not trivial
    for(let k=0;k<26;k++){const x=1+Math.floor(r()*(N-2)),y=1+Math.floor(r()*(N-2)),d=Math.floor(r()*4);
      if(!isGoal(x,y)&&!isGoal(x+DX[d],y+DY[d]))open(x,y,d)}
    return w;
  }

  function Sim(seed){
    this.real=makeMaze(seed);
    this.known=[...Array(N)].map((_,x)=>[...Array(N)].map((_,y)=>[y===0?1:0,x===N-1?1:0,y===N-1?1:0,x===0?1:0]));
    this.dist=[...Array(N)].map(()=>Array(N).fill(65535));
    this.visited=[...Array(N)].map(()=>Array(N).fill(false));
    this.x=0;this.y=N-1;this.h=0;this.phase='explore';this.steps=0;this.trail=[[0,N-1]];this.runPath=null;this.target='goal';
    this.sense();this.flood();
  }
  Sim.prototype.setWall=function(x,y,d){this.known[x][y][d]=1;const nx=x+DX[d],ny=y+DY[d];if(nx>=0&&ny>=0&&nx<N&&ny<N)this.known[nx][ny][(d+2)%4]=1};
  Sim.prototype.sense=function(){this.visited[this.x][this.y]=true;for(let d=0;d<4;d++)if(this.real[this.x][this.y][d])this.setWall(this.x,this.y,d)};
  // Flood(): identical logic to the firmware listing, generalised to any target set
  Sim.prototype.flood=function(targets){
    const q=[];for(let i=0;i<N;i++)for(let j=0;j<N;j++)this.dist[i][j]=65535;
    (targets||GOALS).forEach(([x,y])=>{this.dist[x][y]=0;q.push([x,y])});
    while(q.length){const [x,y]=q.shift();
      for(let d=0;d<4;d++){const nx=x+DX[d],ny=y+DY[d];
        if(nx<0||nx>=N||ny<0||ny>=N)continue; if(this.known[x][y][d]===1)continue;
        if(this.dist[nx][ny]>this.dist[x][y]+1){this.dist[nx][ny]=this.dist[x][y]+1;q.push([nx,ny])}}}
  };
  Sim.prototype.targets=function(){return this.target==='goal'?GOALS:[[0,N-1]]};
  Sim.prototype.step=function(){
    if(this.phase==='done')return false;
    if(this.phase==='run'){ if(this.runIdx<this.runPath.length-1){this.runIdx++;[this.x,this.y]=this.runPath[this.runIdx];return true} this.phase='done';return false;}
    const here=this.dist[this.x][this.y];
    if(here===0){ // reached target
      if(this.target==='goal'){this.target='start';this.phase='return';this.flood(this.targets());return true}
      // back at start: plan the speed run on known walls only
      this.flood(GOALS);this.phase='run';this.runPath=[[this.x,this.y]];let cx=this.x,cy=this.y;
      while(this.dist[cx][cy]>0){for(let d=0;d<4;d++){const nx=cx+DX[d],ny=cy+DY[d];if(!this.known[cx][cy][d]&&nx>=0&&ny>=0&&nx<N&&ny<N&&this.dist[nx][ny]===this.dist[cx][cy]-1){cx=nx;cy=ny;break}}this.runPath.push([cx,cy])}
      this.runIdx=0;this.trail=[];return true;
    }
    const pref=[this.h,(this.h+1)%4,(this.h+3)%4,(this.h+2)%4];let best=-1,bd=65535;
    for(const d of pref){if(this.known[this.x][this.y][d])continue;const nx=this.x+DX[d],ny=this.y+DY[d];if(this.dist[nx][ny]<bd){bd=this.dist[nx][ny];best=d}}
    if(best<0)return false;
    this.h=best;this.x+=DX[best];this.y+=DY[best];this.steps++;this.trail.push([this.x,this.y]);
    this.sense();this.flood(this.targets());return true;
  };

  function draw(ctx,sim,W,opt){
    opt=opt||{};const c=W/N, css=getComputedStyle(document.documentElement);
    const col=k=>css.getPropertyValue(k).trim()||'#888';
    ctx.clearRect(0,0,W,W);ctx.fillStyle=opt.bg||col('--bg2');ctx.fillRect(0,0,W,W);
    const max=Math.max(1,...sim.dist.flat().filter(v=>v<65535));
    for(let x=0;x<N;x++)for(let y=0;y<N;y++){
      const d=sim.dist[x][y];
      if(opt.heat!==false&&d<65535){ctx.fillStyle=`hsla(${200-160*(1-d/max)},85%,55%,${0.08+0.30*(1-d/max)})`;ctx.fillRect(x*c,y*c,c,c)}
      if(isGoal(x,y)){ctx.fillStyle='rgba(255,181,71,.28)';ctx.fillRect(x*c,y*c,c,c)}
      if(opt.numbers&&d<65535&&c>=26){ctx.fillStyle=col('--muted');ctx.font=`${Math.floor(c*.32)}px JetBrains Mono,monospace`;ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(d,x*c+c/2,y*c+c/2)}
    }
    // trail
    if(sim.trail.length>1){ctx.strokeStyle='rgba(92,200,255,.55)';ctx.lineWidth=Math.max(1.5,c*.12);ctx.beginPath();sim.trail.forEach(([x,y],i)=>i?ctx.lineTo(x*c+c/2,y*c+c/2):ctx.moveTo(x*c+c/2,y*c+c/2));ctx.stroke()}
    if(sim.runPath){ctx.strokeStyle='#ffb547';ctx.lineWidth=Math.max(2,c*.18);ctx.lineJoin='round';ctx.beginPath();sim.runPath.forEach(([x,y],i)=>i?ctx.lineTo(x*c+c/2,y*c+c/2):ctx.moveTo(x*c+c/2,y*c+c/2));ctx.stroke()}
    // walls: unknown real walls faint, known walls bright
    for(let x=0;x<N;x++)for(let y=0;y<N;y++)for(let d=0;d<4;d++){
      const k=sim.known[x][y][d], r=sim.real[x][y][d]; if(!r&&!k)continue; if(!k&&!opt.reveal)continue;
      ctx.strokeStyle=k?(opt.wall||col('--text')):'rgba(147,160,182,.22)';ctx.lineWidth=k?Math.max(1.5,c*.09):1;
      ctx.beginPath();const X=x*c,Y=y*c;
      if(d===0){ctx.moveTo(X,Y);ctx.lineTo(X+c,Y)}if(d===1){ctx.moveTo(X+c,Y);ctx.lineTo(X+c,Y+c)}if(d===2){ctx.moveTo(X,Y+c);ctx.lineTo(X+c,Y+c)}if(d===3){ctx.moveTo(X,Y);ctx.lineTo(X,Y+c)}ctx.stroke();
    }
    // mouse
    ctx.save();ctx.translate(sim.x*c+c/2,sim.y*c+c/2);ctx.rotate(sim.h*Math.PI/2);ctx.fillStyle='#ffb547';ctx.shadowColor='#ffb547';ctx.shadowBlur=12;
    ctx.beginPath();ctx.moveTo(0,-c*.34);ctx.lineTo(c*.28,c*.28);ctx.lineTo(-c*.28,c*.28);ctx.closePath();ctx.fill();ctx.restore();
  }

  global.Micromouse={Sim,draw,N};

  // Decorative auto-running mini mazes
  function mini(cv){
    const dpr=Math.min(2,window.devicePixelRatio||1);let sim=new Sim(Math.floor(Math.random()*1e9));
    const fit=()=>{const r=cv.getBoundingClientRect();const s=Math.max(r.width,r.height);cv.width=s*dpr;cv.height=s*dpr;cv.style.objectFit='cover'};
    fit();window.addEventListener('resize',fit);const ctx=cv.getContext('2d');
    let last=0;const loop=t=>{if(t-last>70){last=t;if(!sim.step()){setTimeout(()=>{sim=new Sim(Math.floor(Math.random()*1e9))},1200)}draw(ctx,sim,cv.width,{reveal:true,bg:'#0d121b',wall:'#e8ecf3'})}requestAnimationFrame(loop)};
    requestAnimationFrame(loop);
  }
  document.addEventListener('DOMContentLoaded',()=>document.querySelectorAll('canvas[data-mini]').forEach(mini));
})(window);
