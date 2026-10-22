(() => {
  "use strict";
  document.documentElement.classList.remove("no-js");

  /* Header border once the page scrolls */
  const header = document.querySelector(".site-header");
  if (header) {
    const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* Fade sections in as they enter the viewport */
  const reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add("is-in"));
  }

  /* Footer year */
  document.querySelectorAll("[data-year]").forEach((el) => { el.textContent = new Date().getFullYear(); });

  /* Character level = current age, ticking over on each birthday */
  document.querySelectorAll("[data-level]").forEach((el) => {
    const [y, m, d] = el.dataset.born.split("-").map(Number);
    const now = new Date();
    const hadBirthday = now.getMonth() + 1 > m || (now.getMonth() + 1 === m && now.getDate() >= d);
    el.textContent = now.getFullYear() - y - (hadBirthday ? 0 : 1);
  });

  /* Easter egg: click the portrait to reveal the hidden "Side Character" entry */
  const egg = document.querySelector("[data-egg]");
  const secret = document.querySelector(".exp .secret");
  if (egg && secret) {
    egg.addEventListener("click", () => {
      secret.hidden = false;
      secret.open = true;
      secret.scrollIntoView({ behavior: "smooth", block: "center" });
    });
  }

  /* Click-to-load YouTube players (no third-party iframes until asked) */
  document.querySelectorAll(".player[data-yt]").forEach((player) => {
    const id = player.dataset.yt;
    const img = player.querySelector("img");
    // Upgrade to the HD thumbnail if YouTube has one (missing ones come back as a 120px placeholder)
    if (img && player.dataset.hd !== "false") {
      const hd = new Image();
      hd.onload = () => { if (hd.naturalWidth > 120) img.src = hd.src; };
      hd.src = `https://i.ytimg.com/vi/${id}/maxresdefault.jpg`;
    }
    const btn = player.querySelector(".player-btn");
    if (!btn) return;
    btn.addEventListener("click", () => {
      const iframe = document.createElement("iframe");
      iframe.src = `https://www.youtube-nocookie.com/embed/${id}?autoplay=1&rel=0`;
      iframe.title = btn.getAttribute("aria-label") || "YouTube video";
      iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
      iframe.allowFullscreen = true;
      player.replaceChildren(iframe);
      iframe.focus();
    });
  });

  /* Photography filters */
  const shots = Array.from(document.querySelectorAll(".shot"));
  const filters = document.querySelectorAll(".filter");
  filters.forEach((btn) => {
    btn.addEventListener("click", () => {
      const cat = btn.dataset.filter;
      filters.forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
      shots.forEach((s) => { s.hidden = cat !== "all" && s.dataset.cat !== cat; });
    });
  });

  /* Lightbox */
  const lb = document.querySelector(".lightbox");
  if (lb && shots.length && typeof lb.showModal === "function") {
    const lbImg = lb.querySelector(".lb-stage img");
    const lbCap = lb.querySelector(".lb-caption");
    const lbCount = lb.querySelector(".lb-count");
    let list = [];
    let index = 0;

    const show = (i) => {
      index = (i + list.length) % list.length;
      const link = list[index].querySelector("a");
      const thumb = link.querySelector("img");
      lbImg.src = thumb.currentSrc || thumb.src;   // instant, already loaded
      lbImg.alt = thumb.alt;
      const full = new Image();
      full.onload = () => { if (list[index].querySelector("a") === link) lbImg.src = full.src; };
      full.src = link.href;
      lbCap.textContent = thumb.alt;
      lbCount.textContent = `${String(index + 1).padStart(2, "0")} / ${String(list.length).padStart(2, "0")}`;
      // Warm the neighbours
      [index + 1, index - 1].forEach((n) => {
        const a = list[(n + list.length) % list.length].querySelector("a");
        new Image().src = a.href;
      });
    };

    shots.forEach((shot) => {
      shot.querySelector("a").addEventListener("click", (e) => {
        e.preventDefault();
        list = shots.filter((s) => !s.hidden);
        lb.showModal();
        show(list.indexOf(shot));
      });
    });

    lb.querySelector(".lb-prev").addEventListener("click", () => show(index - 1));
    lb.querySelector(".lb-next").addEventListener("click", () => show(index + 1));
    lb.querySelector(".lb-close").addEventListener("click", () => lb.close());
    lb.addEventListener("click", (e) => { if (e.target === lb || e.target.classList.contains("lb-stage")) lb.close(); });
    lb.addEventListener("keydown", (e) => {
      if (e.key === "ArrowRight") show(index + 1);
      if (e.key === "ArrowLeft") show(index - 1);
    });

    let startX = null;
    lb.addEventListener("touchstart", (e) => { startX = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener("touchend", (e) => {
      if (startX === null) return;
      const dx = e.changedTouches[0].clientX - startX;
      if (Math.abs(dx) > 50) show(index + (dx < 0 ? 1 : -1));
      startX = null;
    });
    lb.addEventListener("close", () => { lbImg.removeAttribute("src"); });
  }
})();
