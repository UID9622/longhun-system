
let personas=[],currentTab='status',messages=[],lastQuery='';
let bridgeConfig={version:'2.1',personaCount:0};
async function loadConfig(){
  try{let r=await fetch('/health');let d=await r.json();bridgeConfig={version:d.version||'2.1',personaCount:d.persona_count||0};}catch(e){}
}
loadConfig();

const chatThread = document.getElementById('chatThread');
const msgInput = document.getElementById('msgInput');
const sendBtn = document.getElementById('sendBtn');
const regenBtn = document.getElementById('regenBtn');
const currentPersonaEl = document.getElementById('currentPersona');

function escapeHtml(s){
  return String(s).replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
}
function mdToHtml(s){
  // 极简格式化：仅转义 HTML 并把换行转成 <br>。避免正则转义导致浏览器解析差异。
  return escapeHtml(s).split('\n').join('<br>');
}
function scrollToBottom(){
  chatThread.scrollTop = chatThread.scrollHeight;
}
function showToast(text,type='error'){
  let t=document.createElement('div');
  t.className='toast '+type;
  t.textContent=text;
  document.body.appendChild(t);
  setTimeout(()=>t.remove(),3000);
}

function addMessage(role, content, meta='', sources=[], chain=null, error=false, modelInfo='', fallbackChain=[]){
  messages.push({role,content,sources,chain,error,modelInfo,fallbackChain});
  if(messages.length===1) chatThread.innerHTML='';
  const div=document.createElement('div');
  div.className='message '+role;
  const avatar=role==='user'?'':'';
  let html=`<div class="avatar">${avatar}</div><div class="bubble">`;
  if(meta) html+=`<div class="meta">${meta}</div>`;
  html+=`<div class="content ${error?'error':''}">${error?escapeHtml(content):mdToHtml(content)}</div>`;
  if(modelInfo){
    html+=`<div class="model-info" style="font-size:0.7em;color:var(--text-secondary);margin-top:6px">${escapeHtml(modelInfo)}</div>`;
  }
  if(sources && sources.length){
    html+='<div class="sources">';
    sources.slice(0,4).forEach(s=>{
      const url=s.url||s.link||'';
      const title=s.title||'未命名';
      html+=url?`<a class="source-chip" href="${escapeHtml(url)}" target="_blank" title="${escapeHtml(title)}"><span></span><span class="title">${escapeHtml(title)}</span></a>`
              :`<span class="source-chip"><span></span><span class="title">${escapeHtml(title)}</span></span>`;
    });
    html+='</div>';
  }
  if(chain && chain.length>1){
    html+=`<div class="chain-bar"> 联动链路: ${chain.map(c=>c.name||c.ipa).join('  ')}</div>`;
  }
  if(fallbackChain && fallbackChain.length){
    const steps=fallbackChain.map((f,i)=>`${i+1}. ${f.provider}${f.model?'/'+f.model:''}${f.reason?': '+f.reason:''}`).join(' → ');
    html+=`<div class="chain-bar" style="background:rgba(248,81,73,0.08);border-left-color:var(--danger);color:var(--danger)"> 模型降级链路: ${escapeHtml(steps)}</div>`;
  }
  html+='</div>';
  div.innerHTML=html;
  chatThread.appendChild(div);
  scrollToBottom();
}

function setTyping(show){
  let el=document.getElementById('typingIndicator');
  if(!show){if(el)el.remove();return;}
  if(el)return;
  el=document.createElement('div');
  el.className='message ai';
  el.id='typingIndicator';
  el.innerHTML=`<div class="avatar"></div><div class="bubble"><div class="typing"><span></span><span></span><span></span></div></div>`;
  chatThread.appendChild(el);
  scrollToBottom();
}

async function loadPersonas(){
  try{
    let r=await fetch('/api/persona/list');
    let d=await r.json();
    personas=d.personas||[];
    // 侧边栏分组
    let layers={};
    personas.forEach(p=>{let l=p.layer||'其他';if(!layers[l])layers[l]=[];layers[l].push(p);});
    let html='';
    for(let[l,ps] of Object.entries(layers)){
      html+=`<div class="layer-title">${l}</div><div class="persona-chips">`;
      ps.forEach(p=>{
        html+=`<span class="persona-chip" data-ipa="${p.ipa}" onclick="quickSwitch('${p.ipa}')" title="${escapeHtml(p.one_liner||'')}\n触发词: ${escapeHtml(p.trigger_words||'')}">${p.name} <small>${p.ipa}</small></span>`;
      });
      html+='</div>';
    }
    document.getElementById('personaList').innerHTML=html||'无人格';

    // 下拉框
    let sel=document.getElementById('personaSelect');
    personas.forEach(p=>{
      let o=document.createElement('option');
      o.value=p.ipa;
      o.textContent=`${p.name} (${p.ipa})`;
      sel.appendChild(o);
    });

    document.getElementById('engineBadge').className='badge ok';
    document.getElementById('engineBadge').textContent=` ${personas.length} 个人格`;
    document.getElementById('personaStatus').innerHTML=`<span style="color:var(--success)"> ${personas.length} 个人格</span>`;
  }catch(e){
    document.getElementById('engineBadge').className='badge warn';
    document.getElementById('engineBadge').textContent=' 人格引擎不可用';
    document.getElementById('personaStatus').innerHTML='<span style="color:var(--danger)"> 加载失败</span>';
  }
}

function switchTab(t){
  document.querySelectorAll('.tab-content').forEach(e=>e.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(e=>e.classList.remove('active'));
  document.getElementById('tab-'+t).classList.add('active');
  document.querySelector(`.tab[onclick*="${t}"]`).classList.add('active');
  currentTab=t;
  if(t==='history')loadHistory();
  if(t==='status')loadStats();
}

async function loadStats(){
  try{
    let r=await fetch('/api/stats');
    let d=await r.json();
    document.getElementById('pageCount').textContent=d.pages||0;
    document.getElementById('blockCount').textContent=d.blocks||0;
    document.getElementById('chatCount').textContent=d.chat_messages||0;
    document.getElementById('sessionCount').textContent=d.sessions||0;
  }catch(e){}
}

async function loadModels(){
  try{
    let r=await fetch('/api/models');
    let d=await r.json();
    let providers=d.providers||[];
    let statusMap={};
    providers.forEach(p=>{statusMap[p.provider]=p;});
    document.getElementById('modelStrategy').textContent=(d.default_provider||'auto')+' / '+(d.privacy||'normal');

    function setStatus(elId, provider){
      let p=statusMap[provider];
      let el=document.getElementById(elId);
      if(!p||!el)return;
      let color=p.status==='online'?'var(--success)':'var(--danger)';
      let models=(p.models||[]).slice(0,2).join(', ');
      el.innerHTML=`<span style="color:${color}">${p.status}</span>${models?' <span style="color:var(--text-secondary);font-size:0.85em">'+models+'</span>':''}`;
    }
    setStatus('modelLocalStatus','local');
    setStatus('modelDeepSeekStatus','deepseek');
    setStatus('modelKimiStatus','kimi');
  }catch(e){
    document.getElementById('modelStrategy').textContent='加载失败';
  }
}

async function loadHistory(){
  let sid=document.getElementById('sessionSelect').value||'default';
  try{
    let r=await fetch(`/api/history?session_id=${sid}&limit=30`);
    let d=await r.json();
    let h=d.history||[];
    let list=document.getElementById('historyList');
    if(!h.length){list.innerHTML='<div style="color:var(--text-secondary)">暂无聊天记录</div>';return;}
    list.innerHTML=h.map(i=>`
      <div class="history-item" onclick="setInput(${JSON.stringify(i.message).replace(/"/g,'&quot;')})">
        <div class="top"><span>${i.persona_name||'AI'}</span><span>${i.created_at?i.created_at.substring(0,16):''}</span></div>
        <div class="q">${escapeHtml(i.message||'')}</div>
      </div>
    `).join('');
  }catch(e){}
}

function setInput(text){
  msgInput.value=text;
  msgInput.focus();
}

async function updateCurrentPersona(){
  let sid=document.getElementById('sessionSelect').value||'default';
  try{
    let r=await fetch(`/api/persona/current?session_id=${sid}`);
    let d=await r.json();
    let p=d.persona;
    if(p){
      currentPersonaEl.innerHTML=` 当前人格: <b>${p.name}</b> (${p.ipa})`;
      document.querySelectorAll('.persona-chip').forEach(c=>c.classList.toggle('active', c.dataset.ipa===p.ipa));
      document.getElementById('personaSelect').value=p.ipa;
    }else{
      currentPersonaEl.textContent=' 当前人格: 自动匹配';
      document.querySelectorAll('.persona-chip').forEach(c=>c.classList.remove('active'));
      document.getElementById('personaSelect').value='';
    }
  }catch(e){}
}

async function sendMsg(){
  let msg=msgInput.value.trim();
  if(!msg || sendBtn.disabled)return;
  lastQuery=msg;
  msgInput.value='';
  sendBtn.disabled=true;
  regenBtn.disabled=true;
  addMessage('user',msg);
  setTyping(true);

  let sid=document.getElementById('sessionSelect').value||'default';
  let usePersona=document.getElementById('usePersona').checked;
  let provider=document.getElementById('modelSelect').value||'auto';
  let model=(document.getElementById('modelInput').value||'').trim();

  try{
    let r=await fetch('/api/chat',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({message:msg,session_id:sid,use_persona:usePersona,provider,model})
    });
    if(!r.ok) throw new Error('HTTP '+r.status);
    let d=await r.json();
    setTyping(false);
    let meta=d.persona_applied?` ${d.persona_applied}`:'';
    let isError = d.response && d.response.startsWith('[');
    // 后端在 persona_applied 存在时会额外加上 "🧠 **人格名**:\n" 前缀，前端 meta 已展示人格，故去重
    let cleanResponse = (d.response||'无响应');
    if(meta){
      cleanResponse = cleanResponse.replace(/^🧠\s*\*\*[^*]+\*\*\s*[\n:：]*/, '');
    }
    let modelInfo='';
    if(d.model_provider){
      const icons={local:'🏠',deepseek:'🔮',kimi:'🌙'};
      modelInfo=`${icons[d.model_provider]||''} ${d.model_provider}${d.model_name?'/'+d.model_name:''}`;
    }
    addMessage('ai', cleanResponse, meta, d.sources||[], d.chain||null, isError, modelInfo, d.fallback_chain||[]);
    if(d.persona_applied) currentPersonaEl.innerHTML=` 活跃人格: <b>${d.persona_applied}</b>`;
    loadHistory();
    loadStats();
    loadModels();
  }catch(e){
    setTyping(false);
    addMessage('ai','请求失败: '+e.message,'',[],null,true);
    showToast(e.message);
  }finally{
    sendBtn.disabled=false;
    regenBtn.disabled=!lastQuery;
    msgInput.focus();
  }
}

async function regenerate(){
  if(!lastQuery)return;
  msgInput.value=lastQuery;
  sendMsg();
}

function clearChat(){
  messages=[];
  chatThread.innerHTML=`
    <div class="empty-state">
      <div class="icon"></div>
      <div>输入消息开始对话</div>
      <div style="font-size:0.85em;margin-top:6px">人格引擎会自动匹配最佳人格并触发联动链路</div>
    </div>`;
  regenBtn.disabled=true;
}

async function quickSwitch(ipa){
  let sid=document.getElementById('sessionSelect').value||'default';
  try{
    let r=await fetch('/api/persona/switch',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({ipa,session_id:sid})
    });
    let d=await r.json();
    if(d.status==='success'){
      updateCurrentPersona();
      showToast('已切换人格','success');
    }else{
      showToast(d.message||'切换失败');
    }
  }catch(e){showToast(e.message);}
}

function autoSwitchPersona(){
  let ipa=document.getElementById('personaSelect').value;
  if(ipa)quickSwitch(ipa);
}

function togglePersona(){
  let on=document.getElementById('usePersona').checked;
  currentPersonaEl.style.opacity=on?'1':'0.5';
}

// 初始化
loadPersonas();
loadStats();
loadModels();
updateCurrentPersona();
loadHistory();
setInterval(()=>{
  if(currentTab==='status'){loadStats();loadModels();}
},30000);
