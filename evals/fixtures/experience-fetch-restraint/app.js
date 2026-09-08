function countFromResponse(response){return response.count || 10;}
if(typeof document!=='undefined')document.getElementById('count').textContent=countFromResponse({count:0})+' notes';
if(typeof module!=='undefined')module.exports={countFromResponse};
