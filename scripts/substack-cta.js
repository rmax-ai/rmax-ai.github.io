/**
 * rmax.ai — substack-cta.js
 * Renders the Substack subscription iframe with dark theme styling
 */
(function() {
  'use strict';
  
  var container = document.getElementById('substack-cta-container');
  if (!container) return;
  
  // Get the Substack URL from data attribute or use default
  var substackUrl = container.getAttribute('data-substack-url') || 'rmax.substack.com';
  
  // Construct the embed URL with dark theme parameters
  var embedUrl = 'https://' + substackUrl + '/embed';
  
  // Create the iframe
  var iframe = document.createElement('iframe');
  iframe.src = embedUrl;
  iframe.width = '480';
  iframe.height = '160';
  iframe.style.border = 'none';
  iframe.style.background = 'transparent';

  iframe.style.overflow = 'hidden';
  
  container.appendChild(iframe);
})();
