const assert=require('node:assert/strict');const fs=require('node:fs');const html=fs.readFileSync('index.html','utf8');
assert(html.includes('id="save"'));
console.log("checks passed");
