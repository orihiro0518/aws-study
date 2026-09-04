// Small navigation/scroll UX fixes kept separate from quiz logic.
(function(){
  function isVisible(el){return el&&!el.classList.contains('hidden')}
  function scrollToSection(el){
    if(!el)return;
    requestAnimationFrame(()=>el.scrollIntoView({behavior:'smooth',block:'start'}));
  }

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
