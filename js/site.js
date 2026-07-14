/* Site-wide progressive enhancement. Nothing here is required for navigation:
   every link is present in the HTML. This only adds the mobile menu toggle,
   the current-page highlight, and the copyright year. */
(function () {
  "use strict";

  // Mobile menu
  var toggle = document.querySelector("[data-os-nav-toggle]");
  var menu = document.getElementById("os-nav-menu");
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var open = menu.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
    });
    // Close the menu when a link inside it is followed.
    menu.addEventListener("click", function (e) {
      if (e.target.closest("a") && menu.classList.contains("is-open")) {
        menu.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  // Current-page highlight
  var path = window.location.pathname;
  if (path === "/index.html") path = "/";
  document.querySelectorAll(".os-nav__link[data-nav]").forEach(function (link) {
    if (link.getAttribute("data-nav") === path) {
      link.setAttribute("aria-current", "page");
    }
  });

  // Copyright year
  document.querySelectorAll("[data-os-year]").forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });

  // Decorative looping videos: play only while on screen, and never under a
  // reduced-motion preference (the poster frame stands in for it).
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var vids = document.querySelectorAll("video[data-os-autoplay]");
  if (vids.length && !reduceMotion && "IntersectionObserver" in window) {
    var vo = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (e) {
          var v = e.target;
          if (e.isIntersecting) {
            var p = v.play();
            if (p && p.catch) p.catch(function () {});
          } else {
            v.pause();
          }
        });
      },
      { rootMargin: "200px 0px" }
    );
    vids.forEach(function (v) {
      vo.observe(v);
    });
  }

  // Carousels. The track is a scrollable list on its own; this only wires the
  // arrow buttons and disables them at the ends.
  document.querySelectorAll("[data-os-carousel]").forEach(function (root) {
    var track = root.querySelector("[data-os-carousel-track]");
    var prev = root.querySelector("[data-os-carousel-prev]");
    var next = root.querySelector("[data-os-carousel-next]");
    if (!track || !prev || !next) return;

    function step() {
      var card = track.firstElementChild;
      if (!card) return track.clientWidth;
      var gap = parseFloat(getComputedStyle(track).columnGap || "16") || 16;
      // Advance by whole cards, never leaving one half-shown.
      var per = Math.max(1, Math.floor(track.clientWidth / (card.offsetWidth + gap)));
      return per * (card.offsetWidth + gap);
    }

    function sync() {
      // 1px of slack: sub-pixel layout can leave scrollLeft a hair short of the end.
      var atStart = track.scrollLeft <= 1;
      var atEnd = track.scrollLeft + track.clientWidth >= track.scrollWidth - 1;
      prev.disabled = atStart;
      next.disabled = atEnd;
    }

    function glide(to) {
      var max = track.scrollWidth - track.clientWidth;
      var target = Math.max(0, Math.min(to, max));
      var from = track.scrollLeft;
      if (Math.abs(target - from) < 1) return;

      var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      if (reduce) {
        track.scrollLeft = target;
        sync();
        return;
      }

      track.scrollTo({ left: target, behavior: "smooth" });

      // Smooth scrolling is driven by the frame loop, which does not run when the
      // page is not being rendered (a background tab, say). Assigning scrollLeft
      // always works, so if the smooth scroll never got off the ground, jump
      // instead -- the arrow must never look dead.
      setTimeout(function () {
        if (track.scrollLeft === from && from !== target) track.scrollLeft = target;
        sync();
      }, 240);
    }

    prev.addEventListener("click", function () {
      glide(track.scrollLeft - step());
    });
    next.addEventListener("click", function () {
      glide(track.scrollLeft + step());
    });
    track.addEventListener("scroll", sync, { passive: true });
    window.addEventListener("resize", sync);
    sync();
  });
})();
