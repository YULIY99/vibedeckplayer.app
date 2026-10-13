/* Regression tests for the actual plain-JS pitch demo. Run: node _build/test_pitch.js */
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const listeners={},input={value:'0',setAttribute(k,v){this[k]=v},addEventListener(k,v){listeners[k]=v}};
const value={},bpm={},thumb={style:{}},reset={addEventListener(k,v){listeners.reset=v}};
const demo={getAttribute(){return '124'},querySelector(s){return {'.pitch-input':input,'[data-pitch-value]':value,'[data-pitch-bpm]':bpm,'.slider-thumb':thumb,'[data-pitch-reset]':reset}[s]}};
const counter={getAttribute(){return '.cards > li'},closest(){return {querySelectorAll(){return Array(18)}}}};
const document={documentElement:{},querySelector(){return null},querySelectorAll(s){return s==='[data-pitch-demo]'?[demo]:s==='[data-section-count]'?[counter]:[]}};
const window={matchMedia(){return {matches:true}},addEventListener(){},innerHeight:1000,scrollY:0};
vm.runInNewContext(fs.readFileSync(require('path').join(__dirname,'../assets/site.js'),'utf8'),{document,window});
assert.strictEqual(value.textContent,'+0.0 st');
assert.strictEqual(bpm.textContent,'BPM 124.0');
assert.strictEqual(counter.textContent,'/ 18');
for(let i=-80;i<=80;i++){
 const st=i/10;input.value=String(st);listeners.input();
 assert.strictEqual(value.textContent,(st>=0?'+':'')+st.toFixed(1)+' st');
 assert.strictEqual(bpm.textContent,'BPM '+(124*2**(st/12)).toFixed(1));
 assert.strictEqual(input['aria-valuetext'],value.textContent);
 assert.strictEqual(thumb.style.left,((st+8)/16*100)+'%');
}
listeners.reset();assert.strictEqual(input.value,'0');assert.strictEqual(bpm.textContent,'BPM 124.0');
console.log('PASS: 161 pitch values, BPM, thumb, accessible value, RESET and section count.');
