/* Idle motion regression, no dependencies. Run: node _build/test_pitch_idle.js */
const fs=require('fs'),vm=require('vm'),assert=require('assert');
function setup(reduce){
 let time=0,id=0,frames=new Map(),events={},input={value:'0',setAttribute(k,v){this[k]=v},addEventListener(k,v){events[k]=v}};
 const value={},bpm={},thumb={style:{}},reset={addEventListener(k,v){events.reset=v}};
 const demo={getAttribute(){return '124'},querySelector(s){return {'.pitch-input':input,'[data-pitch-value]':value,'[data-pitch-bpm]':bpm,'.slider-thumb':thumb,'[data-pitch-reset]':reset}[s]}};
 const document={documentElement:{},querySelector(){return null},querySelectorAll(s){return s==='[data-pitch-demo]'?[demo]:[]}};
 const window={matchMedia(){return {matches:reduce}},addEventListener(){},innerHeight:1000,scrollY:0,requestAnimationFrame(fn){frames.set(++id,fn);return id},cancelAnimationFrame(id){frames.delete(id)}};
 vm.runInNewContext(fs.readFileSync(require('path').join(__dirname,'../assets/site.js'),'utf8'),{document,window});
 function advance(n){for(let i=0;i<n;i++){time+=16;const pending=[...frames.values()];frames.clear();pending.forEach(fn=>fn(time));}}
 return {advance,input,value,bpm,thumb,events};
}
let s=setup(false);s.advance(190);assert(Number(s.input.value)>=.3);assert.strictEqual(s.bpm.textContent,'BPM '+(124*2**(Number(s.input.value)/12)).toFixed(1));
s.advance(375);assert(Number(s.input.value)<=-.3);
s.events.pointerdown();let frozen=s.input.value;s.advance(750);assert.strictEqual(s.input.value,frozen);
s.input.value='2.5';s.events.input();s.advance(750);assert.strictEqual(s.value.textContent,'+2.5 st');
s.events.reset();assert.strictEqual(s.input.value,'0');assert.strictEqual(s.bpm.textContent,'BPM 124.0');s.advance(190);assert(Number(s.input.value)>=.3);
s.events.focus();frozen=s.input.value;s.advance(750);assert.strictEqual(s.input.value,frozen);
s=setup(true);s.advance(1000);assert.strictEqual(s.input.value,'0');assert.strictEqual(s.bpm.textContent,'BPM 124.0');
console.log('PASS: idle motion, BPM sync, pointer/focus takeover, manual control, RESET resume, reduced motion.');
