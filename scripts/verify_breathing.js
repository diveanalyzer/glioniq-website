'use strict';
const assert=require('node:assert/strict');
const {BreathingClock,breathingSnapshot,BREATHING_PATTERNS}=require('../assets/site.js');
let assertions=0;
function equal(a,b,label){assert.deepEqual(a,b,label);assertions++;}
const expected={
 'square-focus':[[0,'Inhale',4,0],[3999,'Inhale',1,null],[4000,'Hold',4,1],[8000,'Exhale',4,1],[12000,'Hold',4,0],[16000,'Inhale',4,0]],
 'sleep-calm':[[0,'Inhale',4,0],[4000,'Hold',2,1],[6000,'Exhale',6,1],[12000,'Inhale',4,0]],
 'neural-wave':[[0,'Inhale',4,0],[4000,'Exhale',6,1],[10000,'Inhale',4,0]],
};
for(const [method,cases] of Object.entries(expected)){
 for(const [ms,phase,remaining,expansion] of cases){const s=breathingSnapshot(method,ms);equal([s.phase,s.remaining],[phase,remaining],method+' boundary '+ms);if(expansion!==null)equal(s.expansion,expansion,'Continuous phase size');}
 const clock=new BreathingClock(method);clock.start(1000);clock.pause(3345.5);
 const before=clock.snapshot(3345.5);equal(clock.snapshot(999999),before,'Paused fraction does not drift');
 clock.pause(999999);equal(clock.snapshot(999999),before,'Repeated pause is idempotent');
 clock.resume(1000000);clock.resume(1000100);equal(clock.snapshot(1001000).elapsedMs,3345.5,'Resume excludes paused time');
 clock.start(2000000);equal(clock.snapshot(2000000).elapsedMs,0,'Restart starts a new cycle');
 const duration=BREATHING_PATTERNS[method].reduce((n,p)=>n+p[1],0)*1000;
 equal(clock.snapshot(2000000+duration*100+2500).cycle,101,'Large frame gap uses elapsed time');
 equal(clock.snapshot(2000000+duration*100+2500).remaining,2,'No countdown drift after large gap');
 clock.reset();clock.resume(3e6);equal([clock.running,clock.started,clock.value(9e6)],[false,false,0],'Exit/reset cannot resume accidentally');
 let previous=breathingSnapshot(method,0);
 for(let ms=20;ms<=duration;ms+=20){const state=breathingSnapshot(method,ms);assert(Math.abs(state.expansion-previous.expansion)<.02,'No abrupt size discontinuities');assert(state.remaining>0);previous=state;assertions+=2;}
}
assert.throws(()=>new BreathingClock('unknown'));assertions++;
console.log(`PASS: ${assertions} breathing assertions; exact boundaries, countdowns, continuity, pause fractions, resume, restart, exit and delayed-frame recovery.`);
