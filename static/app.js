const form=document.getElementById('assessmentForm');
const inputs=[...form.querySelectorAll('input[type="radio"]')];
const total=new Set(inputs.map(i=>i.name)).size;
function updateProgress(){const answered=new Set(inputs.filter(i=>i.checked).map(i=>i.name)).size;const pct=Math.round(answered/total*100);document.getElementById('progressBar').style.width=pct+'%';document.getElementById('progressText').textContent=pct+'% complete';}
inputs.forEach(i=>i.addEventListener('change',updateProgress));updateProgress();
form.addEventListener('submit',e=>{const answered=new Set(inputs.filter(i=>i.checked).map(i=>i.name)).size;if(answered!==total){e.preventDefault();alert(`Please answer all ${total} items. You have completed ${answered}.`);}});
