// Attach timers to the window so other inline scripts can access them
window.totalStart = null;
let totalTimer;
window.restStart = null;
let restDuration = 0;

function key(name) {
  return window.username ? `${name}_${window.username}` : name;
}

function saveTotal() {
  if (window.totalStart !== null) {
    localStorage.setItem(key('totalStart'), window.totalStart.toString());
  } else {
    localStorage.removeItem(key('totalStart'));
  }
}

function saveRest() {
  if (window.restStart !== null && restDuration > 0) {
    localStorage.setItem(key('restStart'), window.restStart.toString());
    localStorage.setItem(key('restDuration'), restDuration.toString());
  } else {
    localStorage.removeItem(key('restStart'));
    localStorage.removeItem(key('restDuration'));
  }
}

function startTotal() {
  if (window.totalStart !== null) return;
  window.totalStart = Date.now();
  saveTotal();
  updateTotal();
  totalTimer = setInterval(updateTotal, 1000);
  const btn = document.getElementById('start-btn');
  if (btn) btn.style.display = 'none';
  const finish = document.getElementById('finish-btn');
  if (finish) finish.style.display = '';
  document.querySelectorAll('.day-back-btn').forEach(b => b.style.display = 'none');
}

function stopTotal() {
  if (window.totalStart === null) return;
  clearInterval(totalTimer);
  window.totalStart = null;
  saveTotal();
  document.getElementById('total').textContent = '0:00';
  document.querySelectorAll('.day-back-btn').forEach(b => b.style.display = '');
}

function finishRoutine() {
  if (window.totalStart === null) return;
  const diff = Date.now() - window.totalStart;
  const timeSec = Math.floor(diff / 1000);
  const checked = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'));
  const indices = checked.map(cb => cb.dataset.idx);
  stopTotal();
  if (window.currentDay) {
    fetch(`/reset/${window.currentDay}`, {method: 'POST'}).finally(() => {
      const params = new URLSearchParams();
      params.set('time', timeSec.toString());
      if (indices.length) params.set('done', indices.join(','));
      window.location.href = `/summary/${window.currentDay}?` + params.toString();
    });
  }
}

function updateTotal() {
  if (window.totalStart === null) return;
  let diff = Date.now() - window.totalStart;
  let sec = Math.floor(diff / 1000);
  let m = Math.floor(sec / 60);
  let s = sec % 60;
  document.getElementById('total').textContent = `${m}:${s.toString().padStart(2,'0')}`;
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('start-btn');
  const finishBtn = document.getElementById('finish-btn');
  const savedTotal = localStorage.getItem(key('totalStart'));
  if (savedTotal) {
    window.totalStart = parseInt(savedTotal, 10);
    updateTotal();
    totalTimer = setInterval(updateTotal, 1000);
    if (btn) btn.style.display = 'none';
    if (finishBtn) finishBtn.style.display = '';
    document.querySelectorAll('.day-back-btn').forEach(b => b.style.display = 'none');
  } else if (btn) {
    btn.addEventListener('click', startTotal);
  }
  if (finishBtn) finishBtn.addEventListener('click', finishRoutine);

  const rs = localStorage.getItem(key('restStart'));
  const rd = localStorage.getItem(key('restDuration'));
  if (rs && rd) {
    window.restStart = parseInt(rs, 10);
    restDuration = parseInt(rd, 10);
    let remain = restDuration - Math.floor((Date.now() - window.restStart)/1000);
    if (remain > 0) {
      document.getElementById('rest').textContent = formatTime(remain);
      restInterval = setInterval(updateRest, 1000);
    } else {
      window.restStart = null;
      restDuration = 0;
      saveRest();
      document.getElementById('rest').textContent = '';
    }
  }
});

let restInterval;
function startRest(seconds) {
  clearInterval(restInterval);
  window.restStart = Date.now();
  restDuration = seconds;
  saveRest();
  updateRest();
  restInterval = setInterval(updateRest, 1000);
}
function updateRest() {
  if (window.restStart === null) return;
  const elapsed = Math.floor((Date.now() - window.restStart) / 1000);
  const remain = restDuration - elapsed;
  document.getElementById('rest').textContent = formatTime(Math.max(remain, 0));
  if (remain <= 0) {
    clearInterval(restInterval);
    window.restStart = null;
    restDuration = 0;
    saveRest();
  }
}
function formatTime(sec) {
  let m = Math.floor(sec/60);
  let s = sec%60;
  return `${m}:${s.toString().padStart(2,'0')}`;
}
