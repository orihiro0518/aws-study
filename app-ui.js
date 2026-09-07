// Small navigation/scroll UX fixes kept separate from quiz logic.
(function(){
  function isVisible(el){return el&&!el.classList.contains('hidden')}
  function scrollToSection(el){
    if(!el)return;
    requestAnimationFrame(()=>el.scrollIntoView({behavior:'smooth',block:'start'}));
  }

  // Visual-only quiz progress bar. Reads existing qnum text; quiz logic is untouched.
  const quiz=document.getElementById('quiz');
  const qmeta=quiz?.querySelector('.qmeta');
  const qnum=document.getElementById('qnum');
  if(quiz&&qmeta&&qnum&&!document.getElementById('awsQuizProgress')){
    const style=document.createElement('style');
    style.id='awsQuizProgressStyle';
    style.textContent=`
      #awsQuizProgress{height:8px;background:#07111f;border:1px solid #263a55;border-radius:999px;overflow:hidden;margin:0 2px 16px}
      #awsQuizProgressFill{height:100%;width:0;background:#ff9900;border-radius:999px;transition:width .2s ease}
    `;
    document.head.appendChild(style);

    const track=document.createElement('div');
    track.id='awsQuizProgress';
    track.setAttribute('aria-hidden','true');
    const fill=document.createElement('div');
    fill.id='awsQuizProgressFill';
    track.appendChild(fill);
    qmeta.insertAdjacentElement('afterend',track);

    const updateProgress=()=>{
      const m=(qnum.textContent||'').match(/(\d+)\s*[\/／]\s*(\d+)/);
      if(!m)return;
      const current=Number(m[1]),total=Number(m[2]);
      const pct=total>0?Math.max(0,Math.min(100,current/total*100)):0;
      fill.style.width=pct+'%';
    };
    new MutationObserver(updateProgress).observe(qnum,{subtree:true,childList:true,characterData:true});
    updateProgress();
  }

  const ver=document.querySelector('.version');
  if(ver)ver.textContent='ver 3.4.3';

  // Practice buttons use inline handlers. By the time this bubbles to document,
  // the selected mode has already opened the quiz (or another section).
  document.addEventListener('click',e=>{
    const practiceButton=e.target.closest('#practiceMenu .btn');
    if(practiceButton){
      requestAnimationFrame(()=>{
        const quiz=document.getElementById('quiz');
        if(isVisible(quiz)){
          // Do not leave the mode-selection buttons above the newly started quiz.
          document.getElementById('practiceMenu')?.classList.add('hidden');
          scrollToSection(quiz);
        }
      });
    }

    // After moving to the next question, bring the new question back into view.
    if(e.target.closest('#next')){
      requestAnimationFrame(()=>{
        const quiz=document.getElementById('quiz');
        const result=document.getElementById('result');
        if(isVisible(quiz))scrollToSection(quiz);
        else if(isVisible(result))scrollToSection(result);
      });
    }
  });
})();
