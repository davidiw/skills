const assert=require('node:assert/strict');const fs=require('node:fs');const html=fs.readFileSync('index.html','utf8');
assert(html.includes('id="schedule"'));assert.equal((html.match(/class="card"/g)||[]).length,8);
console.log("checks passed");
const {stepHistory,averageSteps}=require('./app');
assert.equal(stepHistory.length,7);assert.equal(averageSteps(stepHistory),5800);assert.equal(averageSteps([]),null);
