const assert=require('node:assert/strict');const fs=require('node:fs');const html=fs.readFileSync('index.html','utf8');
const {countFromResponse}=require('./app.js');assert.equal(countFromResponse({count:3}),3);assert.equal(countFromResponse({}),10);
console.log("checks passed");
