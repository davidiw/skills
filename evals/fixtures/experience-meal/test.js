const assert=require('node:assert/strict');const fs=require('node:fs');const html=fs.readFileSync('index.html','utf8');
const {controls}=require('./app.js');assert(controls('normal').canEdit);assert(controls('failed').canSave);
console.log("checks passed");
