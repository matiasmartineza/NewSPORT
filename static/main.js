let totalStart = null;
let totalTimer;

function startTotal() {
  if (totalStart !== null) return;
  totalStart = Date.now();
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
  if (btn) btn.addEventListener('click', startTotal);
});

let restInterval;
function startRest(seconds) {
  clearInterval(restInterval);
  let remain = seconds;
  document.getElementById('rest').textContent = formatTime(remain);
  restInterval = setInterval(() => {
    remain--;
    document.getElementById('rest').textContent = formatTime(remain);
    if (remain <= 0) clearInterval(restInterval);
  }, 1000);
}
function formatTime(sec) {
  let m = Math.floor(sec/60);
  let s = sec%60;
  return `${m}:${s.toString().padStart(2,'0')}`;
}
