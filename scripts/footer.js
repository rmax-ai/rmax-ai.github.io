/**
 * rmax.ai — footer.js
 * Shared footer engine: updates year and chooses a randomized synthesized agent thought.
 * Usage: pages set window.footerThoughts = [ ... ] (array of string or {text,agent}) and include this script.
 */
(function() {
  'use strict';

  // Update year
  var yearEl = document.getElementById('year');
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

  // Pick a thought
  var thoughtEl = document.getElementById('agent-thought');
  var nameEl = document.getElementById('agent-name');

  // Allow either array of strings or array of objects {text, agent}
  var raw = window.footerThoughts || [
    { text: 'I compute to clarify intent, not to replace it.', agent: 'Agent Orchestrator' },
    { text: 'My steps are logs of trust being measured.', agent: 'Agent Auditor' },
    { text: 'I halt when clarity is scarce; I learn when data is plentiful.', agent: 'Agent Learner' }
  ];

  if (thoughtEl && raw && raw.length) {
    var i = Math.floor(Math.random() * raw.length);
    var sel = raw[i];
    if (typeof sel === 'string') {
      thoughtEl.textContent = sel;
      if (nameEl) nameEl.textContent = 'Agent';
    } else if (sel && sel.text) {
      thoughtEl.textContent = sel.text;
      if (nameEl) nameEl.textContent = sel.agent || 'Agent';
    }

    // Small visual reveal
    thoughtEl.style.opacity = '0';
    thoughtEl.style.transition = 'opacity 320ms ease-in-out';
    requestAnimationFrame(function() { thoughtEl.style.opacity = '1'; });
    if (nameEl) {
      nameEl.style.opacity = '0';
      nameEl.style.transition = 'opacity 420ms ease-in-out';
      requestAnimationFrame(function() { nameEl.style.opacity = '1'; });
    }
  }
})();
