/* VibeDeck Player — minimal progressive enhancement. All content is static HTML. */
(function(){
  var d=document,w=window,root=d.documentElement;
  var reduce=w.matchMedia&&w.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // Pitch demo: playback-rate BPM preview, not an audio player.
  [].slice.call(d.querySelectorAll('[data-pitch-demo]')).forEach(function(demo){
    var input=demo.querySelector('.pitch-input');
    var value=demo.querySelector('[data-pitch-value]');
    var bpm=demo.querySelector('[data-pitch-bpm]');
    var thumb=demo.querySelector('.slider-thumb');
    var base=Number(demo.getAttribute('data-base-bpm'));
    if(!input||!value||!bpm||!isFinite(base)||base<=0)return;
    var idleFrame=0,idleElapsed=0,lastTime=0,manual=false;
    function update(visualSt){
      var st=Number(input.value),label=(st>=0?'+':'')+st.toFixed(1)+' st';
      if(value.textContent!==label)value.textContent=label;
      input.setAttribute('aria-valuetext',label);
      bpm.textContent='BPM '+(base*Math.pow(2,st/12)).toFixed(1);
      if(thumb)thumb.style.left=(((typeof visualSt==='number'?visualSt:st)+8)/16*100)+'%';
    }
    // One slow, small breath: +/-0.4 st over 12 seconds. Numbers stay on 0.1 st steps.
    function idle(time){
      if(manual||reduce)return;
      if(lastTime)idleElapsed+=Math.min(time-lastTime,50);
      lastTime=time;
      var st=Math.sin(idleElapsed/12000*Math.PI*2)*.4;
      input.value=(Math.round(st*10)/10).toFixed(1);
      update(st);
      idleFrame=w.requestAnimationFrame(idle);
    }
    function startIdle(){
      idleElapsed=0;lastTime=0;
      if(!reduce&&w.requestAnimationFrame)idleFrame=w.requestAnimationFrame(idle);
    }
    function takeControl(){
      manual=true;
      if(idleFrame){w.cancelAnimationFrame(idleFrame);idleFrame=0;}
      update();
    }
    ['pointerdown','touchstart','focus','keydown'].forEach(function(event){input.addEventListener(event,takeControl);});
    input.addEventListener('input',takeControl);
    demo.querySelector('[data-pitch-reset]').addEventListener('click',function(){
      takeControl();manual=false;input.value='0';update();startIdle();
    });
    update();startIdle();
  });
  // Derive labels from the actual section content, not a manual total.
  [].slice.call(d.querySelectorAll('[data-section-count]')).forEach(function(counter){
    var section=counter.closest('section');
    if(section)counter.textContent='/ '+section.querySelectorAll(counter.getAttribute('data-section-count')).length;
  });
  // header hairline on scroll
  var hdr=d.querySelector('.site-header');
  // scroll reveal
  var els=[].slice.call(d.querySelectorAll('[data-reveal]'));
  if(!('IntersectionObserver' in w)||reduce){els.forEach(function(e){e.classList.add('is-in')});}
  else{
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-in');io.unobserve(e.target);}})},{rootMargin:'0px 0px -8% 0px',threshold:.08});
    els.forEach(function(e){io.observe(e)});
    setTimeout(function(){els.forEach(function(e){e.classList.add('is-in')})},6000);
  }
  // parallax (transform only)
  var px=reduce?[]:[].slice.call(d.querySelectorAll('[data-parallax]'));
  var ticking=false;
  function frame(){
    ticking=false;var vh=w.innerHeight;
    if(hdr)hdr.classList.toggle('is-scrolled',w.scrollY>8);
    for(var i=0;i<px.length;i++){
      var el=px[i],r=el.getBoundingClientRect();
      if(r.bottom<-200||r.top>vh+200)continue;
      var k=parseFloat(el.getAttribute('data-parallax'))||.06;
      var c=(r.top+r.height/2-vh/2);
      el.style.transform='translate3d(0,'+(-c*k).toFixed(1)+'px,0)';
    }
  }
  function onScroll(){if(!ticking){ticking=true;w.requestAnimationFrame(frame);}}
  w.addEventListener('scroll',onScroll,{passive:true});w.addEventListener('resize',onScroll);frame();
  // showcase rail: tabs + arrows
  var rail=d.querySelector('.rail');
  if(rail){
    var tabs=[].slice.call(d.querySelectorAll('.tabs a'));
    var shots=[].slice.call(rail.querySelectorAll('.shot'));
    function go(el){rail.scrollTo({left:el.offsetLeft-rail.firstElementChild.offsetLeft,behavior:reduce?'auto':'smooth'});}
    tabs.forEach(function(t,i){t.addEventListener('click',function(ev){ev.preventDefault();go(shots[i]);});});
    function current(){var l=rail.scrollLeft,best=0,bd=1e9;shots.forEach(function(s,i){var dd=Math.abs(s.offsetLeft-rail.firstElementChild.offsetLeft-l);if(dd<bd){bd=dd;best=i;}});return best;}
    var raf=0;
    rail.addEventListener('scroll',function(){cancelAnimationFrame(raf);raf=requestAnimationFrame(function(){var c=current();tabs.forEach(function(t,i){t.classList.toggle('is-active',i===c);if(i===c)t.setAttribute('aria-current','true');else t.removeAttribute('aria-current');});});},{passive:true});
    var prev=d.querySelector('[data-rail="prev"]'),next=d.querySelector('[data-rail="next"]');
    if(prev)prev.addEventListener('click',function(){go(shots[Math.max(0,current()-1)]);});
    if(next)next.addEventListener('click',function(){go(shots[Math.min(shots.length-1,current()+1)]);});
  }
  // Share block: copy the link, count share clicks as GoatCounter events (no third-party scripts).
  function countShare(net){if(w.goatcounter&&w.goatcounter.count)w.goatcounter.count({path:'share-'+net,title:'Share: '+net,event:true});}
  [].slice.call(d.querySelectorAll('[data-share]')).forEach(function(a){a.addEventListener('click',function(){countShare(a.getAttribute('data-share'));});});
  if(navigator.share&&w.matchMedia&&w.matchMedia('(pointer: coarse)').matches){
    [].slice.call(d.querySelectorAll('[data-share-native]')).forEach(function(btn){
      btn.parentNode.hidden=false;
      btn.addEventListener('click',function(){
        countShare('native');
        navigator.share({title:'VibeDeck Player',text:btn.getAttribute('data-text'),url:btn.getAttribute('data-url')}).catch(function(){});
      });
    });
  }
  [].slice.call(d.querySelectorAll('[data-share-copy]')).forEach(function(btn){
    var label=btn.querySelector('span'),text=label.textContent;
    function done(){label.textContent=btn.getAttribute('data-copied');btn.classList.add('is-done');setTimeout(function(){label.textContent=text;btn.classList.remove('is-done');},2000);}
    btn.addEventListener('click',function(){
      var url=btn.getAttribute('data-share-copy');countShare('copy');
      if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(url).then(done,function(){});return;}
      var t=d.createElement('textarea');t.value=url;t.setAttribute('readonly','');t.style.position='fixed';t.style.opacity='0';d.body.appendChild(t);t.select();
      try{if(d.execCommand('copy'))done();}catch(e){}
      d.body.removeChild(t);
    });
  });
})();
