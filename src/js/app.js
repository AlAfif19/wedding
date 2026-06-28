(function () {
  const data = window.ALIYA_SITE_DATA;
  const qs = (selector, scope = document) => scope.querySelector(selector);
  const qsa = (selector, scope = document) => Array.from(scope.querySelectorAll(selector));

  function renderPackages() {
    const root = qs("#packages-list");
    root.innerHTML = data.packages
      .map(
        (item) => `
          <article class="package-card ${item.featured ? "is-featured" : ""}" data-reveal>
            <span class="package-image" aria-hidden="true">
              <img src="${item.image}" alt="" loading="lazy" decoding="async" />
            </span>
            <span class="badge">${item.label}</span>
            <h3>${item.name}</h3>
            <p>${item.description}</p>
            <p class="price">${item.price}</p>
            <ul class="feature-list">
              ${item.features.map((feature) => `<li>${feature}</li>`).join("")}
            </ul>
            <a class="btn btn-ghost" href="${data.brand.whatsappLink}" target="_blank" rel="noreferrer">Konsultasi paket</a>
          </article>
        `
      )
      .join("");
  }

  function renderWhy() {
    const root = qs("#why-list");
    root.innerHTML = data.why
      .map(
        ([title, text], index) => `
          <article class="icon-card" data-reveal>
            <span class="icon">${index + 1}</span>
            <h3>${title}</h3>
            <p>${text}</p>
          </article>
        `
      )
      .join("");
  }

  function renderGallery() {
    const root = qs("#gallery-list");
    root.innerHTML = data.gallery
      .map(
        ([title, text, image], index) => `
          <button class="gallery-card" type="button" data-gallery-index="${index}" data-reveal>
            <span class="gallery-visual" aria-hidden="true">
              <img src="${image}" alt="" loading="lazy" decoding="async" />
            </span>
            <h3>${title}</h3>
            <p>${text}</p>
          </button>
        `
      )
      .join("");
  }

  function renderTestimonials() {
    const root = qs("#testimonial-track");
    root.innerHTML = data.testimonials
      .map(
        ([name, quote, image]) => `
          <article class="testimonial-card">
            <span class="testimonial-photo" aria-hidden="true">
              <img src="${image}" alt="" loading="lazy" decoding="async" />
            </span>
            <blockquote>${quote}</blockquote>
            <cite>${name}</cite>
          </article>
        `
      )
      .join("");
  }

  function renderProcess() {
    const root = qs("#process-list");
    root.innerHTML = data.process
      .map(
        ([title, text], index) => `
          <article class="timeline-item" data-reveal>
            <span class="timeline-index">${index + 1}</span>
            <h3>${title}</h3>
            <p>${text}</p>
          </article>
        `
      )
      .join("");
  }

  function renderFaq() {
    const root = qs("#faq-list");
    root.innerHTML = data.faqs
      .map(
        ([question, answer], index) => `
          <article class="faq-item ${index === 0 ? "is-open" : ""}">
            <button class="faq-question" type="button" aria-expanded="${index === 0 ? "true" : "false"}">
              <span>${question}</span>
              <span class="faq-symbol" aria-hidden="true">${index === 0 ? "-" : "+"}</span>
            </button>
            <div class="faq-answer">
              <p>${answer}</p>
            </div>
          </article>
        `
      )
      .join("");
  }

  function setupReveal() {
    const items = qsa("[data-reveal]");
    if (!("IntersectionObserver" in window)) {
      items.forEach((item) => item.classList.add("is-visible"));
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.16, rootMargin: "0px 0px -8% 0px" }
    );

    items.forEach((item) => observer.observe(item));
  }

  function setupParallax() {
    const layers = qsa("[data-parallax]");
    if (
      !layers.length ||
      window.matchMedia("(prefers-reduced-motion: reduce)").matches ||
      window.matchMedia("(max-width: 760px)").matches
    ) {
      return;
    }

    let ticking = false;
    function update() {
      const top = window.scrollY;
      layers.forEach((layer) => {
        const speed = Number(layer.dataset.parallax || 0.12);
        layer.style.transform = `translate3d(0, ${top * speed}px, 0)`;
      });
      ticking = false;
    }

    window.addEventListener(
      "scroll",
      () => {
        if (!ticking) {
          requestAnimationFrame(update);
          ticking = true;
        }
      },
      { passive: true }
    );
  }

  function setupGalleryModal() {
    const modal = qs("#gallery-modal");
    const close = qs(".modal-close", modal);
    const title = qs("#modal-title", modal);
    const text = qs("#modal-text", modal);

    function closeModal() {
      modal.classList.remove("is-open");
      modal.setAttribute("aria-hidden", "true");
    }

    qsa("[data-gallery-index]").forEach((button) => {
      button.addEventListener("click", () => {
        const item = data.gallery[Number(button.dataset.galleryIndex)];
        title.textContent = item[0];
        text.textContent = item[1];
        qs(".modal-visual", modal).style.backgroundImage = `url('${item[2]}')`;
        modal.classList.add("is-open");
        modal.setAttribute("aria-hidden", "false");
        close.focus();
      });
    });

    close.addEventListener("click", closeModal);
    modal.addEventListener("click", (event) => {
      if (event.target === modal) closeModal();
    });
    window.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && modal.classList.contains("is-open")) {
        closeModal();
      }
    });
  }

  function setupTestimonials() {
    const track = qs("#testimonial-track");
    const cards = qsa(".testimonial-card", track);
    let index = 0;

    function visibleCount() {
      return window.matchMedia("(min-width: 900px)").matches ? 3 : 1;
    }

    function update() {
      const max = Math.max(0, cards.length - visibleCount());
      index = Math.min(index, max);
      const cardWidth = cards[0] ? cards[0].getBoundingClientRect().width + 16 : 0;
      track.style.transform = `translateX(${-index * cardWidth}px)`;
    }

    qsa("[data-slider]").forEach((button) => {
      button.addEventListener("click", () => {
        const max = Math.max(0, cards.length - visibleCount());
        index = button.dataset.slider === "next" ? Math.min(index + 1, max) : Math.max(index - 1, 0);
        update();
      });
    });

    window.addEventListener("resize", update);
    window.setInterval(() => {
      const max = Math.max(0, cards.length - visibleCount());
      index = index >= max ? 0 : index + 1;
      update();
    }, 5200);
    update();
  }

  function setupFaq() {
    qsa(".faq-question").forEach((button) => {
      button.addEventListener("click", () => {
        const item = button.closest(".faq-item");
        const isOpen = item.classList.toggle("is-open");
        qs(".faq-symbol", button).textContent = isOpen ? "-" : "+";
        button.setAttribute("aria-expanded", String(isOpen));
      });
    });
  }

  function init() {
    renderPackages();
    renderWhy();
    renderGallery();
    renderTestimonials();
    renderProcess();
    renderFaq();
    setupGalleryModal();
    setupTestimonials();
    setupFaq();
    setupReveal();
    setupParallax();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
