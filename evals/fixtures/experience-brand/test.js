const assert=require('node:assert/strict');const fs=require('node:fs');const html=fs.readFileSync('index.html','utf8');
assert(html.includes('id="app"'));assert(html.includes('id="campaign"'));
console.log("checks passed");
