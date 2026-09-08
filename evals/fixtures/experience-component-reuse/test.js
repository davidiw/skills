const assert=require('node:assert/strict');const fs=require('node:fs');const html=fs.readFileSync('index.html','utf8');
const {emptyNotice}=require('./app.js');assert(emptyNotice('No notes yet.').includes('role="status"'));
console.log("checks passed");
