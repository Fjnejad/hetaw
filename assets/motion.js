/* HETAW — scroll reveal + stat count-up. No dependencies; respects reduced motion. */
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var els = document.querySelectorAll('.reveal');
  if (reduce || !('IntersectionObserver' in window)) {
    els.forEach(function (e) { e.classList.add('in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
    });
  }, { rootMargin: '0px 0px -10% 0px', threshold: 0.12 });
  els.forEach(function (e) { io.observe(e); });

  // count-up for [data-count]
  var nums = document.querySelectorAll('[data-count]');
  var fmt = function (v, dec) { return dec ? v.toFixed(1) : Math.round(v).toString(); };
  var io2 = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      var el = en.target, target = parseFloat(el.getAttribute('data-count')), suf = el.getAttribute('data-suffix') || '';
      var dec = String(target).indexOf('.') > -1, t0 = null, dur = 1100;
      function step(ts) {
        if (!t0) t0 = ts;
        var p = Math.min(1, (ts - t0) / dur), e = 1 - Math.pow(1 - p, 3);
        el.textContent = fmt(target * e, dec) + suf;
        if (p < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
      io2.unobserve(el);
    });
  }, { threshold: 0.6 });
  nums.forEach(function (n) { io2.observe(n); });
})();

(function(){var h=document.querySelector(".masthead");if(!h)return;var f=function(){h.classList.toggle("scrolled",window.scrollY>8)};f();addEventListener("scroll",f,{passive:true})})();
