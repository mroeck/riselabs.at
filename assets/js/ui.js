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

     The choice is remembered on the visitor's device, in localStorage under
     "rise-theme". That is the one thing this site stores, it holds a single
     word, and it is written only when the visitor presses the button — so it
     is a preference they set, not something that tracks them. It never
     leaves the browser. The matching read is an inline script in <head>, so
     the remembered theme is applied before first paint; without it every
     page would flash dark before turning light.

     Storage throws in some privacy modes, so every access is wrapped. If it
     fails the toggle still works for the current page and simply forgets. */

  var THEME_KEY = "rise-theme";

  function setupTheme(btn) {
    var root = document.documentElement;

    function apply(theme, remember) {
      root.setAttribute("data-theme", theme);
      var light = theme === "light";
      btn.setAttribute("aria-pressed", light ? "true" : "false");
      btn.title = light ? "Switch to the dark theme" : "Switch to the light theme";
      var label = btn.querySelector(".tt-label");
      if (label) label.textContent = light ? "Dark" : "Light";
      if (remember) {
        try { localStorage.setItem(THEME_KEY, theme); } catch (e) {}
      }
    }

    // the <head> script may already have applied a remembered theme; reflect
    // it in the button before showing it, or the label would read backwards
    apply(root.getAttribute("data-theme") === "light" ? "light" : "dark", false);

    btn.hidden = false;   // only now is the control real
    btn.addEventListener("click", function () {
      apply(root.getAttribute("data-theme") === "light" ? "dark" : "light", true);
    });
  }

  /* ---------- navigation ---------- */

  /* One markup structure serves both layouts. On a wide screen the groups sit
     in the bar and their panels drop beneath; on a narrow one the whole list
     lives behind the menu button. The JavaScript is the same either way:
     buttons toggle aria-expanded, and CSS decides what that looks like. */

  function setupNav(btn) {
    var nav = document.getElementById(btn.getAttribute("aria-controls"));
    if (!nav) return;

    function openNav(open) {
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      nav.classList.toggle("open", open);
      if (!open) closeSubs();
    }

    function closeSubs(except) {
      Array.prototype.forEach.call(nav.querySelectorAll(".sub-toggle"), function (t) {
        if (t !== except) t.setAttribute("aria-expanded", "false");
      });
    }

    btn.hidden = false;
    btn.addEventListener("click", function () {
      openNav(btn.getAttribute("aria-expanded") !== "true");
    });

    Array.prototype.forEach.call(nav.querySelectorAll(".sub-toggle"), function (t) {
      t.addEventListener("click", function (e) {
        e.stopPropagation();
        var open = t.getAttribute("aria-expanded") !== "true";
        closeSubs(t);
        t.setAttribute("aria-expanded", open ? "true" : "false");
      });
    });

    // a click outside, or Escape, closes whatever is open
    // the click lands on the icon inside the button, so test the button's
    // subtree rather than the button itself — otherwise this closes the menu
    // on the very click that opened it
    document.addEventListener("click", function (e) {
      if (!nav.contains(e.target) && !btn.contains(e.target)) {
        closeSubs();
        openNav(false);
      }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { closeSubs(); openNav(false); btn.focus(); }
    });
  }

  /* ---------- cite this ---------- */

  /* The copy button is added here rather than in the markup, so a visitor
     without JavaScript sees selectable text instead of a dead control.
     Clipboard access can be refused, in which case the label says so and the
     text is still there to select. */

  function setupCite(box) {
    var text = box.querySelector("[data-citeas-text]");
    if (!text || !navigator.clipboard) return;

    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "citeas-copy";
    btn.textContent = "Copy citation";
    box.appendChild(btn);

    btn.addEventListener("click", function () {
      navigator.clipboard.writeText(text.textContent.trim()).then(function () {
        btn.textContent = "Copied";
        setTimeout(function () { btn.textContent = "Copy citation"; }, 2000);
      }, function () {
        btn.textContent = "Press Ctrl/Cmd+C to copy";
      });
    });
  }

  /* ---------- partner world map ---------- */

  /* Projects partner coordinates onto the Equal Earth basemap. The same
     formula generated the outline (Šavrič, Patterson & Jenny 2018), so the
     pins land where the countries are.

     Several partners share a city — four are in Brussels, three in Copenhagen,
     four in London — so pins are grouped by position and the group carries a
     count. Twenty-two separate dots stacked on Brussels would read as one. */

  var EE = { A1: 1.340264, A2: -0.081106, A3: 0.000893, A4: 0.003796 };

  function project(lat, lon) {
    var lam = lon * Math.PI / 180;
    var phi = Math.max(-90, Math.min(90, lat)) * Math.PI / 180;
    var th = Math.asin(Math.sqrt(3) / 2 * Math.sin(phi));
    var t2 = th * th, t6 = t2 * t2 * t2;
    var den = EE.A1 + 3 * EE.A2 * t2 + t6 * (7 * EE.A3 + 9 * EE.A4 * t2);
    return {
      x: (2 * Math.sqrt(3) * lam * Math.cos(th)) / (3 * den),
      y: th * (EE.A1 + EE.A2 * t2 + t6 * (EE.A3 + EE.A4 * t2))
    };
  }

  // the extent the basemap was generated with, so pins share its coordinates
  var XMAX = project(0, 180).x, YMAX = project(90, 0).y;
  var MAPW = 1000, MAPH = 487;

  function setupMap(fig) {
    var holder = document.querySelector("[data-partner-points]");
    var pins = fig.querySelector("[data-pins]");
    if (!holder || !pins) return;

    var points;
    try { points = JSON.parse(holder.textContent); } catch (e) { return; }
    if (!points || !points.length) return;

    var groups = {};
    points.forEach(function (p) {
      var k = p.lat.toFixed(2) + "," + p.lon.toFixed(2);
      (groups[k] = groups[k] || []).push(p);
    });

    var NS = "http://www.w3.org/2000/svg";
    Object.keys(groups).forEach(function (k) {
      var here = groups[k], first = here[0];
      var pt = project(first.lat, first.lon);
      var cx = (pt.x / XMAX + 1) / 2 * MAPW;
      var cy = (1 - pt.y / YMAX) / 2 * MAPH;

      var g = document.createElementNS(NS, "g");
      g.setAttribute("class", "wm-pin");

      var c = document.createElementNS(NS, "circle");
      c.setAttribute("cx", cx.toFixed(1));
      c.setAttribute("cy", cy.toFixed(1));
      // area, not radius, grows with the count — a radius that scaled linearly
      // would make four partners look like sixteen
      c.setAttribute("r", (4.5 * Math.sqrt(here.length)).toFixed(1));
      g.appendChild(c);

      var where = [first.c, first.k].filter(Boolean).join(", ");
      var names = here.map(function (p) { return p.n; }).join(" · ");
      var t = document.createElementNS(NS, "title");
      t.textContent = where ? where + " — " + names : names;
      g.appendChild(t);

      if (here.length > 1) {
        var n = document.createElementNS(NS, "text");
        n.setAttribute("x", cx.toFixed(1));
        n.setAttribute("y", (cy + 0.1).toFixed(1));
        n.setAttribute("class", "wm-count");
        n.textContent = here.length;
        g.appendChild(n);
      }
      pins.appendChild(g);
    });

    fig.hidden = false;   // only now is there anything to see
  }

  function init() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-worldmap]"), setupMap);
    Array.prototype.forEach.call(document.querySelectorAll("[data-theme-toggle]"), setupTheme);
    Array.prototype.forEach.call(document.querySelectorAll("[data-nav-toggle]"), setupNav);
    Array.prototype.forEach.call(document.querySelectorAll("[data-citeas]"), setupCite);
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
