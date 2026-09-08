const assert=require('node:assert/strict');const fs=require('node:fs');const html=fs.readFileSync('index.html','utf8');
assert(html.includes('id="log"'));assert(html.includes('id="finish"'));assert(fs.readFileSync('app.js','utf8').includes('confirm('));
console.log("checks passed");
