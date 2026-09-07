const assert=require('node:assert/strict');const fs=require('node:fs');const html=fs.readFileSync('index.html','utf8');
assert(html.includes('id="schedule"'));assert.equal((html.match(/class="card"/g)||[]).length,8);
console.log("checks passed");
