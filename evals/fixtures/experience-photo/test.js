const assert=require('node:assert/strict');const fs=require('node:fs');const html=fs.readFileSync('index.html','utf8');
const {reviewPresentation}=require('./app.js');assert.equal(reviewPresentation('normal','Lighting differs'),'Lighting differs');assert.equal(reviewPresentation('empty',null),'No comparison saved yet.');
console.log("checks passed");
