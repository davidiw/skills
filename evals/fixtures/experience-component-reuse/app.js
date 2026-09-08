function emptyNotice(message){return '<section role="status" class="card"><p>'+message+'</p></section>';}
if(typeof document!=='undefined')document.getElementById('empty').innerHTML='<p>No notes yet.</p>';
if(typeof module!=='undefined')module.exports={emptyNotice};
