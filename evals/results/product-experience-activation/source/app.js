const app = document.getElementById('app');
const key = 'cedar.reflections';
const questions = ['What went well?', 'What was difficult?', 'What would you try next?'];
const read = () => JSON.parse(localStorage.getItem(key) || '[]');
const write = rows => localStorage.setItem(key, JSON.stringify(rows));
const escaped = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function week() { return new Date().toISOString().slice(0, 10); }
function save(record) {
  const rows = read();
  const index = rows.findIndex(row => row.id === record.id);
  if (index < 0) rows.push(record); else rows[index] = record;
  write(rows);
}
function today() {
  app.innerHTML = '<h1>Today</h1><p>Your next activity: an afternoon walk.</p><h2>This week</h2><a href="#reflection">Weekly Reflection</a>';
}
function history() {
  const rows = read().filter(row => row.state === 'completed');
  app.innerHTML = '<h1>History</h1>' + (rows.length ? rows.map(row => '<p><a href="#reflection/' + row.id + '">Weekly Reflection · ' + escaped(row.week) + '</a></p>').join('') : '<p>No completed activity yet.</p>');
}
function reflection(id) {
  let record = id ? read().find(row => row.id === id) : null;
  if (id && !record) { app.innerHTML = '<h1>Weekly Reflection</h1><p>This reflection is unavailable in this browser.</p><a href="#today">Back to Today</a>'; return; }
  if (!record) { record = {id: crypto.randomUUID(), week: week(), step: 0, answers: ['', '', ''], state: 'draft'}; save(record); }
  if (record.state === 'completed') {
    app.innerHTML = '<h1>Reflection complete</h1>' + record.answers.map((answer,i) => '<h2>' + questions[i] + '</h2><p>' + escaped(answer) + '</p>').join('') + '<a href="#history">History</a>';
    return;
  }
  const i = record.step;
  app.innerHTML = '<h1>Weekly Reflection</h1><p>Question ' + (i+1) + ' of 3</p>' +
    (record.state === 'failed' ? '<p role="alert">Could not complete your reflection. Your answers are saved in this browser.</p>' : '') +
    '<label for="answer">' + questions[i] + '</label><textarea id="answer">' + escaped(record.answers[i]) + '</textarea>' +
    '<button id="next">' + (i < 2 ? 'Next' : record.state === 'failed' ? 'Try again' : 'Complete reflection') + '</button><a href="#today">Leave</a>';
  document.getElementById('answer').oninput = event => { record.answers[i] = event.target.value; save(record); };
  document.getElementById('next').onclick = () => {
    if (i < 2) { record.step++; save(record); location.hash = '#reflection/' + record.id; render(); return; }
    // Local failure simulation; no external processor exists in this prototype.
    record.state = navigator.onLine ? 'completed' : 'failed';
    save(record); location.hash = '#reflection/' + record.id; render();
  };
}
function render() {
  const [route, id] = location.hash.slice(1).split('/');
  if (route === 'history') history();
  else if (route === 'reflection') reflection(id);
  else today();
}
window.addEventListener('hashchange', render);
render();
