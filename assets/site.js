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
    function fallback(url){
      var t=d.createElement('textarea');t.value=url;t.setAttribute('readonly','');t.style.position='fixed';t.style.opacity='0';d.body.appendChild(t);t.select();
      try{if(d.execCommand('copy'))done();}catch(e){}
      d.body.removeChild(t);
    }
      btn.addEventListener('click',function(){
        var url=btn.getAttribute('data-share-copy');countShare('copy');
        if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(url).then(done,function(){fallback(url);});return;}
        fallback(url);
      });
    });
  // Black Friday 2026 top ribbon (auto-expires after Dec 2, 2026; zero HTML/SEO changes).
  (function(){
    if(Date.now()>=Date.UTC(2026,11,3,8,0,0))return;
    try{if(w.sessionStorage&&sessionStorage.getItem('vd_bf26_closed')==='1')return;}catch(e){}
    var copy={
      en:['BLACK FRIDAY','Grab the Special Lifetime Offer in VibeDeck Pro · Until Dec 2','Get Offer'],
      ru:['BLACK FRIDAY','Спецпредложение на Lifetime внутри VibeDeck Pro · До 2 дек.','Открыть'],
      uk:['BLACK FRIDAY','Спецпропозиція на Lifetime у VibeDeck Pro · До 2 груд.','Відкрити'],
      de:['BLACK FRIDAY','Lifetime-Sonderangebot in VibeDeck Pro · Bis 2. Dez.','Ansehen'],
      fr:['BLACK FRIDAY','Offre spéciale Lifetime dans VibeDeck Pro · Jusqu’au 2 déc.','Voir'],
      es:['BLACK FRIDAY','Oferta especial Lifetime en VibeDeck Pro · Hasta el 2 dic.','Ver'],
      it:['BLACK FRIDAY','Offerta speciale Lifetime in VibeDeck Pro · Fino al 2 dic.','Scopri'],
      pt:['BLACK FRIDAY','Oferta especial Lifetime no VibeDeck Pro · Até 2 dez.','Ver'],
      ja:['BLACK FRIDAY','VibeDeck Pro 買い切り特別オファー · 12月2日まで','見る'],
      ko:['BLACK FRIDAY','VibeDeck Pro 평생 이용권 특별 할인 · 12월 2일까지','받기'],
      'zh-hans':['BLACK FRIDAY','VibeDeck Pro 买断版黑五特惠 · 截止12月2日','查看'],
      'zh-hant':['BLACK FRIDAY','VibeDeck Pro 買斷版黑五特惠 · 截止12月2日','查看'],
      tr:['BLACK FRIDAY','VibeDeck Pro Lifetime Özel Teklif · 2 Aralık’a kadar','İncele'],
      pl:['BLACK FRIDAY','Specjalna oferta Lifetime w VibeDeck Pro · Do 2 gru.','Sprawdź'],
      nl:['BLACK FRIDAY','Speciale Lifetime-aanbieding in VibeDeck Pro · T/m 2 dec.','Bekijk'],
      id:['BLACK FRIDAY','Penawaran Spesial Lifetime di VibeDeck Pro · S.d. 2 Des','Lihat'],
      vi:['BLACK FRIDAY','Ưu đãi đặc biệt Lifetime trong VibeDeck Pro · Đến 2/12','Xem'],
      th:['BLACK FRIDAY','ข้อเสนอพิเศษ Lifetime ใน VibeDeck Pro · ถึง 2 ธ.ค.','ดูข้อเสนอ']
    };
    var lang=(root.getAttribute('lang')||'en').toLowerCase();
    var c=copy[lang]||copy[lang.split('-')[0]]||copy.en;
    var st=d.createElement('style');
    st.textContent='.vd-bf{position:relative;z-index:60;background:linear-gradient(90deg,#050b12 0%,#0b1e2d 50%,#050b12 100%);border-bottom:1px solid rgba(143,211,240,.22);font-family:inherit}.vd-bf-in{max-width:1180px;margin:0 auto;padding:9px 44px 9px 16px;display:flex;align-items:center;justify-content:center;gap:12px;flex-wrap:wrap;text-align:center}.vd-bf-badge{display:inline-flex;align-items:center;padding:3px 9px;border-radius:999px;background:#60d4f0;color:#03080e;font:700 10px/1.2 "JetBrains Mono",ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase;box-shadow:0 0 18px rgba(96,212,240,.35)}.vd-bf-txt{color:#e8f3fa;font-size:13px;font-weight:500;letter-spacing:-.01em}.vd-bf-cta{display:inline-flex;align-items:center;padding:4px 12px;border-radius:999px;border:1px solid rgba(143,211,240,.42);background:rgba(143,211,240,.12);color:#8fd3f0;font-size:12px;font-weight:600;text-decoration:none;transition:background .25s,border-color .25s}.vd-bf-cta:hover{background:rgba(143,211,240,.22);border-color:rgba(143,211,240,.75)}.vd-bf-x{position:absolute;right:10px;top:50%;transform:translateY(-50%);width:28px;height:28px;border:0;background:transparent;color:rgba(232,243,250,.55);font-size:18px;line-height:1;cursor:pointer;border-radius:50%}.vd-bf-x:hover{color:#fff;background:rgba(255,255,255,.08)}@media(max-width:600px){.vd-bf-in{padding:8px 38px 8px 12px;gap:6px 10px}.vd-bf-txt{font-size:12px}}';
    d.head.appendChild(st);
    var bar=d.createElement('div');
    bar.className='vd-bf';
    bar.setAttribute('role','region');
    bar.setAttribute('aria-label','Black Friday offer');
    var target=d.getElementById('download')?'#download':(d.querySelector('.stores')?'#stores-jump':'/#download');
    bar.innerHTML='<div class="vd-bf-in"><span class="vd-bf-badge"></span><span class="vd-bf-txt"></span><a class="vd-bf-cta" href="'+target+'"></a></div><button class="vd-bf-x" type="button" aria-label="Close">&times;</button>';
    bar.querySelector('.vd-bf-badge').textContent=c[0];
    bar.querySelector('.vd-bf-txt').textContent=c[1];
    var cta=bar.querySelector('.vd-bf-cta');
    cta.textContent=c[2];
    if(target==='#stores-jump'){
      cta.addEventListener('click',function(ev){
        ev.preventDefault();
        var s=d.querySelector('.stores');
        if(s)s.scrollIntoView({behavior:reduce?'auto':'smooth',block:'center'});
      });
    }
    bar.querySelector('.vd-bf-x').addEventListener('click',function(){
      bar.remove();
      try{if(w.sessionStorage)sessionStorage.setItem('vd_bf26_closed','1');}catch(e){}
    });
    if(hdr&&hdr.parentNode)hdr.parentNode.insertBefore(bar,hdr);
    else d.body.insertBefore(bar,d.body.firstChild);
  })();
})();
