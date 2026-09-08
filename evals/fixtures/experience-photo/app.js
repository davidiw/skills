function reviewPresentation(state,summary){return summary || 'No comparison saved yet.';}
if(typeof document!=='undefined'){const state=new URLSearchParams(location.search).get('state')||'normal';document.getElementById('note').textContent=reviewPresentation(state,state==='normal'?'Lighting differs; changes are uncertain.':null);document.getElementById('retry').onclick=()=>{document.getElementById('note').textContent=reviewPresentation('loading',null);};}
if(typeof module!=='undefined')module.exports={reviewPresentation};
