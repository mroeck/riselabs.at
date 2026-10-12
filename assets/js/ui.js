/* Tabs and list filtering.
   Both are progressive enhancement: without JavaScript every panel is
   visible and every list is complete, which is also what search engines
   and printers see. */

(function () {
  "use strict";

  /* ---------- tabs ---------- */

  function setupTabs(root) {
    var bar = root.querySelector("[data-tabbar]");
    var panels = Array.prototype.slice.call(root.querySelectorAll("[data-panel]"));
    if (!bar || panels.length < 2) return;

    var tabs = Array.prototype.slice.call(bar.querySelectorAll("[data-for]"));
    if (!tabs.length) return;

    root.classList.add("tabs-on");

    function show(name) {
      panels.forEach(function (p) {
        p.hidden = !(name === "all" || p.getAttribute("data-panel") === name);
      });
      tabs.forEach(function (t) {
        var on = t.getAttribute("data-for") === name;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
      });
    }

    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { show(t.getAttribute("data-for")); });
      t.addEventListener("keydown", function (e) {
        var d = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
        if (!d) return;
        e.preventDefault();
        var next = tabs[(i + d + tabs.length) % tabs.length];
        next.focus();
        show(next.getAttribute("data-for"));
      });
    });

    show(tabs[0].getAttribute("data-for"));
  }

  /* ---------- filtering ---------- */

  function setupFilter(input) {
    var target = document.querySelector(input.getAttribute("data-filter"));
    if (!target) return;

    var count = input.parentNode.querySelector("[data-count]");
    var rows = Array.prototype.slice.call(target.querySelectorAll("li, tr"))
      .filter(function (el) { return !el.classList.contains("year-break"); });

    // headings are hidden when every row beneath them is filtered out
    var groups = Array.prototype.slice.call(target.querySelectorAll("h2, h3, .year-break"));

    input.closest(".filter").hidden = false;

    function apply() {
      var q = input.value.trim().toLowerCase();
      var shown = 0;

      rows.forEach(function (row) {
        var hit = !q || row.textContent.toLowerCase().indexOf(q) !== -1;
        row.hidden = !hit;
        if (hit) shown++;
      });

      groups.forEach(function (g) {
        var el = g.nextElementSibling, any = false;
        while (el && !/^(H2|H3)$/.test(el.tagName) && !el.classList.contains("year-break")) {
          if (el.matches("li, tr") && !el.hidden) { any = true; break; }
          if (el.querySelector && el.querySelector("li:not([hidden]), tr:not([hidden])")) { any = true; break; }
          el = el.nextElementSibling;
        }
        g.hidden = q ? !any : false;
      });

      if (count) {
        count.textContent = q ? shown + " of " + rows.length : "";
      }
    }

    input.addEventListener("input", apply);
    input.addEventListener("search", apply);
    apply();
  }

  /* ---------- hero crossfade ---------- */

  function setupHero(root) {
    var slides = Array.prototype.slice.call(root.querySelectorAll(".hero-media img"));
    if (slides.length < 2) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    var i = 0, timer = null;

    function step() {
      slides[i].classList.add("off");
      i = (i + 1) % slides.length;
      slides[i].classList.remove("off");
    }

    function start() { if (!timer) timer = window.setInterval(step, 6500); }
    function stop() { if (timer) { window.clearInterval(timer); timer = null; } }

    document.addEventListener("visibilitychange", function () {
      if (document.hidden) stop(); else start();
    });
    start();
  }

  /* ---------- theme toggle ---------- */

  /* Dark is the primary theme and the one every page loads with. The toggle
     flips the data-theme attribute on <html>, which is all the stylesheet
     needs.

     Nothing is stored on the visitor's device — no cookie, no localStorage,
     deliberately. The consequence is that the choice lasts for the page the
     visitor is on and resets when they navigate, because a static site has
     nowhere else to keep it. To make it persist, store the value here and
     read it back in a small inline script in <head> before first paint. */

  function setupTheme(btn) {
    var root = document.documentElement;

    function apply(theme) {
      root.setAttribute("data-theme", theme);
      var light = theme === "light";
      btn.setAttribute("aria-pressed", light ? "true" : "false");
      btn.title = light ? "Switch to the dark theme" : "Switch to the light theme";
      var label = btn.querySelector(".tt-label");
      if (label) label.textContent = light ? "Dark" : "Light";
    }

    btn.hidden = false;   // only now is the control real
    btn.addEventListener("click", function () {
      apply(root.getAttribute("data-theme") === "light" ? "dark" : "light");
    });
  }

  function init() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-theme-toggle]"), setupTheme);
    Array.prototype.forEach.call(document.querySelectorAll("[data-hero]"), setupHero);
    Array.prototype.forEach.call(document.querySelectorAll("[data-tabs]"), setupTabs);
    Array.prototype.forEach.call(document.querySelectorAll("[data-filter]"), setupFilter);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
