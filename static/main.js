let totalStart = null;
let totalTimer;
let restStart = null;
let restDuration = 0;

function saveTotal() {
  if (totalStart !== null) {
    localStorage.setItem('totalStart', totalStart.toString());
  } else {
    localStorage.removeItem('totalStart');
  }
}

function saveRest() {
  if (restStart !== null && restDuration > 0) {
    localStorage.setItem('restStart', restStart.toString());
    localStorage.setItem('restDuration', restDuration.toString());
  } else {
    localStorage.removeItem('restStart');
    localStorage.removeItem('restDuration');
  }
}

function startTotal() {
  if (totalStart !== null) return;
  totalStart = Date.now();
  saveTotal();
  updateTotal();
  totalTimer = setInterval(updateTotal, 1000);
  const btn = document.getElementById('start-btn');
  if (btn) btn.style.display = 'none';
}

function updateTotal() {
  if (totalStart === null) return;
  let diff = Date.now() - totalStart;
  let sec = Math.floor(diff / 1000);
  let m = Math.floor(sec / 60);
  let s = sec % 60;
  document.getElementById('total').textContent = `${m}:${s.toString().padStart(2,'0')}`;
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('start-btn');
  const savedTotal = localStorage.getItem('totalStart');
  if (savedTotal) {
    totalStart = parseInt(savedTotal, 10);
    updateTotal();
    totalTimer = setInterval(updateTotal, 1000);
    if (btn) btn.style.display = 'none';
  } else if (btn) {
    btn.addEventListener('click', startTotal);
  }

  const rs = localStorage.getItem('restStart');
  const rd = localStorage.getItem('restDuration');
  if (rs && rd) {
    restStart = parseInt(rs, 10);
    restDuration = parseInt(rd, 10);
    let remain = restDuration - Math.floor((Date.now() - restStart)/1000);
    if (remain > 0) {
      document.getElementById('rest').textContent = formatTime(remain);
      restInterval = setInterval(updateRest, 1000);
    } else {
      restStart = null;
      restDuration = 0;
      saveRest();
      document.getElementById('rest').textContent = '';
    }
  }
});

let restInterval;
function startRest(seconds) {
  clearInterval(restInterval);
  restStart = Date.now();
  restDuration = seconds;
  saveRest();
  updateRest();
  restInterval = setInterval(updateRest, 1000);
}
function updateRest() {
  if (restStart === null) return;
  const elapsed = Math.floor((Date.now() - restStart) / 1000);
  const remain = restDuration - elapsed;
  document.getElementById('rest').textContent = formatTime(Math.max(remain, 0));
  if (remain <= 0) {
    clearInterval(restInterval);
    restStart = null;
    restDuration = 0;
    saveRest();
  }
}
function formatTime(sec) {
  let m = Math.floor(sec/60);
  let s = sec%60;
  return `${m}:${s.toString().padStart(2,'0')}`;
}
