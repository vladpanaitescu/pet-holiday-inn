/* Pet Holiday — interacțiuni și animații */
(() => {
  // Datele de contact reale se completează aici (apar automat în tot site-ul)
  const CONFIG = { phone: "+40 778 393 527", email: "petholidayinn@gmail.com" };

  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const finePointer = matchMedia("(hover: hover) and (pointer: fine)").matches;
  const hasGsap = typeof window.gsap !== "undefined" && typeof window.ScrollTrigger !== "undefined";

  $("#year").textContent = new Date().getFullYear();

  if (CONFIG.phone) $$('[data-cfg="phone"]').forEach(a => { a.textContent = CONFIG.phone; a.href = "tel:" + CONFIG.phone.replace(/[^\d+]/g, ""); });
  if (CONFIG.email) $$('[data-cfg="email"]').forEach(a => { a.textContent = CONFIG.email; a.href = "mailto:" + CONFIG.email; });

  /* ---------- Split text în cuvinte ---------- */
  $$("[data-split]").forEach(el => {
    if (el.classList.contains("hero__title")) {
      $$(".line", el).forEach(l => { l.innerHTML = `<span>${l.innerHTML}</span>`; });
      return;
    }
    el.innerHTML = el.textContent.trim().split(/\s+/).map(w => `<span class="w"><span>${w}</span></span>`).join(" ");
  });

  /* ---------- Loader ---------- */
  let started = false;
  const start = () => {
    if (started) return; started = true;
    document.documentElement.classList.add("is-loaded");
    if (hasGsap && !reduce) heroIntro();
  };
  window.addEventListener("load", () => setTimeout(start, 350));
  setTimeout(start, 2800);

  /* ---------- Nav ---------- */
  const nav = $("#nav");
  let lastY = 0;
  const onScroll = y => {
    nav.classList.toggle("is-solid", y > 40);
    nav.classList.toggle("is-hidden", y > 500 && y > lastY && !document.body.classList.contains("menu-open"));
    lastY = y;
    $(".fab").classList.toggle("is-on", y > innerHeight * .8 && y < document.body.scrollHeight - innerHeight * 1.8);
  };

  const burger = $(".burger");
  const toggleMenu = open => {
    document.body.classList.toggle("menu-open", open);
    burger.setAttribute("aria-expanded", open);
    $("#menu").setAttribute("aria-hidden", !open);
    if (lenis) open ? lenis.stop() : lenis.start();
  };
  burger.addEventListener("click", () => toggleMenu(!document.body.classList.contains("menu-open")));
  $$("#menu a").forEach(a => a.addEventListener("click", () => toggleMenu(false)));

  // Link activ în meniu
  const links = $$(".nav__links a");
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) links.forEach(l => l.classList.toggle("is-active", l.getAttribute("href") === "#" + e.target.id));
  }), { rootMargin: "-45% 0px -50% 0px" });
  $$("section[id]").forEach(s => io.observe(s));

  /* ---------- Smooth scroll ---------- */
  let lenis = null;
  if (window.Lenis && !reduce) {
    lenis = new Lenis({ lerp: .1, smoothWheel: true });
    lenis.on("scroll", ({ scroll }) => onScroll(scroll));
    if (hasGsap) {
      lenis.on("scroll", ScrollTrigger.update);
      gsap.ticker.add(t => lenis.raf(t * 1000));
      gsap.ticker.lagSmoothing(0);
    } else {
      const raf = t => { lenis.raf(t); requestAnimationFrame(raf); };
      requestAnimationFrame(raf);
    }
  } else {
    addEventListener("scroll", () => onScroll(scrollY), { passive: true });
  }
  $$('a[href^="#"]').forEach(a => a.addEventListener("click", e => {
    const id = a.getAttribute("href");
    const t = id.length > 1 && $(id);
    if (!t) return;
    e.preventDefault();
    if (lenis) lenis.scrollTo(t, { offset: id === "#acasa" ? 0 : -70, duration: 1.4 });
    else t.scrollIntoView({ behavior: reduce ? "auto" : "smooth" });
  }));

  /* ---------- Contoare ---------- */
  const fmt = (n, sep) => sep ? Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, sep) : Math.round(n);
  const setCount = (el, v) => { el.textContent = fmt(v, el.dataset.sep) + (el.dataset.suffix || ""); };
  const counters = $$("[data-count]");

  /* ---------- Animații GSAP ---------- */
  function heroIntro() {
    const tl = gsap.timeline({ defaults: { ease: "expo.out" } });
    tl.from(".hero__media img", { scale: 1.25, duration: 2.2, ease: "power3.out" }, 0)
      .fromTo(".hero__title .line > span", { yPercent: 110, rotate: 4 }, { yPercent: 0, rotate: 0, duration: 1.3, stagger: .12 }, .15)
      .from(".hero__tag", { y: 20, opacity: 0, duration: 1 }, .3)
      .from(".hero__lead, .hero__ctas", { y: 30, opacity: 0, duration: 1.1, stagger: .1 }, .6)
      .from(".nav", { opacity: 0, duration: 1 }, .5)
      .from(".hero__note", { scale: 0, rotate: -30, duration: 1.2, ease: "back.out(1.8)" }, .9)
      .from(".hero__seal", { scale: 0, rotate: -120, duration: 1.4, ease: "back.out(1.5)" }, 1)
      .from(".hero__scroll", { opacity: 0, duration: 1 }, 1.3);
  }

  if (hasGsap && !reduce) {
    gsap.registerPlugin(ScrollTrigger);
    document.documentElement.classList.add("has-gsap");

    // Parallax hero
    gsap.to(".hero__media img", { yPercent: 12, ease: "none", scrollTrigger: { trigger: ".hero", start: "top top", end: "bottom top", scrub: true } });
    gsap.to(".hero__inner", { y: -80, opacity: .2, ease: "none", scrollTrigger: { trigger: ".hero", start: "40% top", end: "bottom top", scrub: true } });
    gsap.to(".hero__note", { y: -140, rotate: 6, ease: "none", scrollTrigger: { trigger: ".hero", start: "top top", end: "bottom top", scrub: true } });

    // Marquee accelerează cu scroll-ul
    // Banda rulează din GSAP (nu din CSS), ca viteza să se schimbe lin, fără salturi
    const loop = gsap.to(".marquee__track", { xPercent: -50, duration: 32, ease: "none", repeat: -1 });
    ScrollTrigger.create({ onUpdate: s => {
      gsap.to(loop, { timeScale: 1 + Math.min(Math.abs(s.getVelocity()) / 1200, 2.5), duration: .25, overwrite: true,
        onComplete: () => gsap.to(loop, { timeScale: 1, duration: 1.2, ease: "power2.out", overwrite: true }) });
    } });

    // Titluri: cuvintele urcă din mască
    $$("[data-split]:not(.hero__title)").forEach(el => {
      gsap.from($$(".w > span", el), { yPercent: 110, rotate: 3, duration: 1.1, ease: "expo.out", stagger: .06,
        scrollTrigger: { trigger: el, start: "top 88%" } });
    });

    // Elemente care apar de jos
    const ups = ".eyebrow, .about__copy > p:not(.eyebrow), .about__script, .stats li, .cabins__lead, .yard__copy > *, .cats__copy > p, .cats__copy .btn, .faq__aside, .contact__info > p, .contact__list li, .form, .map__frame, .band__sig, .insta__head .btn";
    $$(ups).forEach(el => {
      gsap.from(el, { y: 40, opacity: 0, duration: 1, ease: "power3.out", scrollTrigger: { trigger: el, start: "top 90%" } });
    });

    // Imagini cu reveal pe mască
    $$(".reveal-img").forEach(el => {
      const img = $("img", el);
      gsap.timeline({ scrollTrigger: { trigger: el, start: "top 82%" } })
        .from(el, { clipPath: "inset(100% 0% 0% 0% round 30px)", duration: 1.4, ease: "expo.inOut" })
        .from(img, { scale: 1.35, duration: 1.8, ease: "expo.out" }, "-=1");
    });
    gsap.from(".about__sticker", { x: 60, opacity: 0, rotate: 6, duration: 1.2, ease: "back.out(1.4)", scrollTrigger: { trigger: ".about__media", start: "top 50%" } });
    gsap.to(".about__media img", { yPercent: -6, ease: "none", scrollTrigger: { trigger: ".about", scrub: true } });

    // Contoare
    counters.forEach(el => {
      const o = { v: 0 };
      gsap.to(o, { v: +el.dataset.count, duration: 2.2, ease: "power2.out", onUpdate: () => setCount(el, o.v),
        scrollTrigger: { trigger: el, start: "top 90%" } });
    });

    // Cabane: scroll orizontal pe desktop
    const mm = gsap.matchMedia();
    mm.add("(min-width: 861px)", () => {
      const track = $(".cabins__track");
      const dist = () => track.scrollWidth - innerWidth;
      const tween = gsap.to(track, { x: () => -dist(), ease: "none",
        scrollTrigger: { trigger: ".cabins__pin", start: "center center", end: () => "+=" + dist(), pin: true, scrub: .8, invalidateOnRefresh: true, anticipatePin: 1 } });
      gsap.to(".cabins__progress span", { scaleX: 1, ease: "none", scrollTrigger: { trigger: ".cabins__pin", start: "center center", end: () => "+=" + dist(), scrub: true } });
      $$(".cabin").forEach(c => {
        gsap.from($$(".cabin__body > *", c), { y: 30, opacity: 0, stagger: .05, duration: .8, ease: "power3.out",
          scrollTrigger: { trigger: c, containerAnimation: tween, start: "left 80%" } });
        gsap.fromTo($(".cabin__img img", c), { xPercent: -8, scale: 1.15 }, { xPercent: 8, ease: "none",
          scrollTrigger: { trigger: c, containerAnimation: tween, start: "left right", end: "right left", scrub: true } });
      });
    });
    mm.add("(max-width: 860px)", () => {
      $$(".cabin").forEach(c => {
        gsap.from(c, { y: 60, opacity: 0, duration: 1, ease: "power3.out", scrollTrigger: { trigger: c, start: "top 88%" } });
      });
    });

    // Curtea
    gsap.from(".yard__big", { xPercent: -8, opacity: 0, duration: 1.4, ease: "expo.out", scrollTrigger: { trigger: ".yard__big", start: "top 85%" } });
    gsap.from(".pills li", { scale: .6, opacity: 0, duration: .6, ease: "back.out(2)", stagger: .07, scrollTrigger: { trigger: ".pills", start: "top 90%" } });

    // Pisici
    gsap.from(".cats__paw", { scale: 0, rotate: -90, duration: 1.2, ease: "back.out(2)", scrollTrigger: { trigger: ".cats__media", start: "top 60%" } });
    gsap.to(".cats__media img", { yPercent: -5, ease: "none", scrollTrigger: { trigger: ".cats", scrub: true } });

    // Servicii, Instagram
    gsap.from(".svc", { y: 70, opacity: 0, duration: 1, ease: "power3.out", stagger: { each: .08, grid: "auto" }, scrollTrigger: { trigger: ".services__grid", start: "top 85%" } });
    gsap.from(".insta__item", { y: 60, opacity: 0, rotate: i => (i % 2 ? 3 : -3), duration: 1, ease: "power3.out", stagger: .08, scrollTrigger: { trigger: ".insta__grid", start: "top 90%" } });

    // Pași: linia se desenează, cercurile apar
    gsap.fromTo(".steps__line", { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", ease: "none", scrollTrigger: { trigger: ".steps__wrap", start: "top 80%", end: "bottom 60%", scrub: true } });
    $$(".step").forEach((s, i) => {
      gsap.timeline({ scrollTrigger: { trigger: s, start: "top 85%" } })
        .from($(".step__n", s), { scale: 0, rotate: -180, duration: .9, ease: "back.out(1.8)", delay: i * .08 })
        .from([$("h3", s), $("p", s)], { y: 24, opacity: 0, duration: .8, stagger: .08, ease: "power3.out" }, "-=.5");
    });

    // Band parallax
    gsap.fromTo(".band__img", { yPercent: -10 }, { yPercent: 10, ease: "none", scrollTrigger: { trigger: ".band", scrub: true } });

    // FAQ
    gsap.from(".qa", { x: 40, opacity: 0, duration: .9, ease: "power3.out", stagger: .07, scrollTrigger: { trigger: ".faq__list", start: "top 85%" } });

    addEventListener("load", () => ScrollTrigger.refresh());
  } else {
    counters.forEach(el => setCount(el, +el.dataset.count));
  }

  /* ---------- Butoane magnetice + cursor ---------- */
  if (finePointer && !reduce) {
    // Poziția se calculează față de locul butonului fără deplasare (altfel tremură) și se animă lin
    $$(".magnetic").forEach(b => {
      let box = null, mx = 0, my = 0;
      const move = hasGsap
        ? { x: gsap.quickTo(b, "x", { duration: .5, ease: "power3.out" }), y: gsap.quickTo(b, "y", { duration: .5, ease: "power3.out" }) }
        : { x: v => { mx = v; b.style.translate = `${mx}px ${my}px`; }, y: v => { my = v; b.style.translate = `${mx}px ${my}px`; } };
      b.addEventListener("mouseenter", () => {
        const r = b.getBoundingClientRect(), t = hasGsap ? [gsap.getProperty(b, "x"), gsap.getProperty(b, "y")] : [mx, my];
        box = { cx: r.left - t[0] + r.width / 2, cy: r.top - t[1] + r.height / 2 };
      });
      b.addEventListener("mousemove", e => {
        if (!box) return;
        move.x((e.clientX - box.cx) * .25);
        move.y((e.clientY - box.cy) * .35);
      });
      b.addEventListener("mouseleave", () => { box = null; move.x(0); move.y(0); });
    });

    const cur = $(".cursor");
    let cx = 0, cy = 0, tx = 0, ty = 0;
    addEventListener("mousemove", e => { tx = e.clientX; ty = e.clientY; });
    (function loop() {
      cx += (tx - cx) * .2; cy += (ty - cy) * .2;
      cur.style.translate = `${cx}px ${cy}px`;
      requestAnimationFrame(loop);
    })();
    $$(".cabin__img, .insta__item, .yard__img, .cats__media, .about__media").forEach(el => {
      el.addEventListener("mouseenter", () => cur.classList.add("is-on"));
      el.addEventListener("mouseleave", () => cur.classList.remove("is-on"));
    });

    // Urme de lăbuțe în hero
    const hero = $(".hero");
    let lx = 0, ly = 0, side = 1;
    hero.addEventListener("mousemove", e => {
      const d = Math.hypot(e.clientX - lx, e.clientY - ly);
      if (d < 90) return;
      const ang = Math.atan2(e.clientY - ly, e.clientX - lx) * 180 / Math.PI + 90;
      lx = e.clientX; ly = e.clientY; side *= -1;
      const p = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      p.setAttribute("class", "trail");
      p.innerHTML = '<use href="#i-paw"/>';
      const off = side * 12, rad = (ang) * Math.PI / 180;
      p.style.left = e.clientX - 11 + Math.cos(rad) * off + "px";
      p.style.top = e.clientY - 11 + Math.sin(rad) * off + "px";
      p.style.transform = `rotate(${ang}deg)`;
      document.body.appendChild(p);
      p.animate([{ opacity: .9, scale: .4 }, { opacity: .9, scale: 1, offset: .15 }, { opacity: 0, scale: 1 }], { duration: 1400, easing: "ease-out" }).onfinish = () => p.remove();
    });
  }

  /* ---------- Formular ---------- */
  const form = $("#form");
  const today = new Date().toISOString().slice(0, 10);
  const ci = form.checkin, co = form.checkout;
  ci.min = today; co.min = today;
  ci.addEventListener("change", () => { co.min = ci.value || today; if (co.value && co.value < ci.value) co.value = ""; });

  $$("[data-cabin]").forEach(a => a.addEventListener("click", () => { form.cabana.value = a.dataset.cabin; form.animal.value = "Câine"; }));
  $$("[data-pet]").forEach(a => a.addEventListener("click", () => { form.animal.value = a.dataset.pet; }));

  const err = $(".form__err", form);
  const bad = (el, on) => (el.closest(".field") || el.closest(".consent")).classList.toggle("is-bad", on);
  $$("input, select, textarea", form).forEach(el => el.addEventListener("input", () => bad(el, false)));

  form.addEventListener("submit", async e => {
    e.preventDefault();
    err.textContent = "";
    let ok = true;
    $$("[required]", form).forEach(el => {
      const v = el.type === "checkbox" ? el.checked : el.checkValidity();
      bad(el, !v); if (!v) ok = false;
    });
    if (!ok) {
      err.textContent = "Te rugăm să completezi câmpurile marcate.";
      $(".is-bad input", form)?.focus();
      return;
    }
    if (form.website.value) return; // bot

    const btn = $("button[type=submit]", form);
    btn.classList.add("is-loading");
    const name = form.nume_animal.value.trim();
    $(".ok-name", form).textContent = name || (form.animal.value === "Pisică" ? "pisica ta" : "blănosul tău");

    try {
      const res = await fetch(form.action, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } });
      const data = await res.json().catch(() => null);
      if (!res.ok || !data || !data.ok) throw new Error((data && data.error) || "send");
      form.classList.add("is-sent");
      form.reset();
    } catch (x) {
      // Previzualizare locală fără PHP: arătăm confirmarea ca demo
      if (/^(localhost|127\.0\.0\.1|)$/.test(location.hostname) || location.protocol === "file:") {
        form.classList.add("is-sent");
      } else {
        err.textContent = "Mesajul nu a putut fi trimis. Te rugăm să ne suni sau să încerci din nou.";
      }
    } finally {
      btn.classList.remove("is-loading");
    }
  });
})();
