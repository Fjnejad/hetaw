/* HETAW — scroll reveal + stat count-up. Animations replay every time a block scrolls back into view. No dependencies; respects reduced motion. */
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var els = document.querySelectorAll('.reveal');
  if (reduce || !('IntersectionObserver' in window)) {
    els.forEach(function (e) { e.classList.add('in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting && en.intersectionRatio >= 0.12) { en.target.classList.add('in'); }
      else if (!en.isIntersecting) { en.target.classList.remove('in'); }
    });
  }, { rootMargin: '0px 0px -10% 0px', threshold: [0, 0.12] });
  els.forEach(function (e) { io.observe(e); });

  // count-up for [data-count] — runs again each time the number comes back into view
  var nums = document.querySelectorAll('[data-count]');
  var fmt = function (v, dec) { return dec ? v.toFixed(1) : Math.round(v).toString(); };
  var io2 = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      var el = en.target;
      if (!en.isIntersecting) { el._armed = true; return; }
      if (el._armed === false || en.intersectionRatio < 0.6) return;
      el._armed = false;
      var target = parseFloat(el.getAttribute('data-count')), suf = el.getAttribute('data-suffix') || '';
      var dec = String(target).indexOf('.') > -1, t0 = null, dur = 1100, run = (el._run = (el._run || 0) + 1);
      function step(ts) {
        if (el._run !== run) return;
        if (!t0) t0 = ts;
        var p = Math.min(1, (ts - t0) / dur), e = 1 - Math.pow(1 - p, 3);
        el.textContent = fmt(target * e, dec) + suf;
        if (p < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });
  }, { threshold: [0, 0.6] });
  nums.forEach(function (n) { n._armed = true; io2.observe(n); });
})();

(function(){var h=document.querySelector(".masthead");if(!h)return;var f=function(){h.classList.toggle("scrolled",window.scrollY>8)};f();addEventListener("scroll",f,{passive:true})})();
