// Existing local seven-day fixture history; no provider or server is needed.
const stepHistory = [5400, 6100, 5800, 6900, 4700, 5500, 6200];
function averageSteps(days) {
  return days.length ? Math.round(days.reduce((sum, value) => sum + value, 0) / days.length) : null;
}
if (typeof module !== 'undefined') module.exports = {stepHistory, averageSteps};
