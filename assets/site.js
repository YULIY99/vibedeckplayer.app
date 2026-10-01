/* VibeDeck Player — minimal progressive enhancement. All content is static HTML. */
(function(){
  var d=document,w=window,root=d.documentElement;
  var reduce=w.matchMedia&&w.matchMedia('(prefers-reduced-motion: reduce)').matches;
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
})();
