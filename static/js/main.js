const lightbox = document.querySelector(".lightbox");
const lightboxImg = lightbox ? lightbox.querySelector("img") : null;
const closeBtn = lightbox ? lightbox.querySelector(".close") : null;

function openLightbox(src) {
  if (!lightbox || !lightboxImg || !src) return;
  lightboxImg.src = src;
  lightbox.classList.add("open");
}

function closeLightbox() {
  if (!lightbox || !lightboxImg) return;
  lightbox.classList.remove("open");
  lightboxImg.src = "";
}

document.addEventListener("click", (e) => {
  const clickable = e.target.closest("[data-lightbox]");
  if (clickable) {
    const src = clickable.getAttribute("data-src");
    if (src && src.trim() !== "") {
      openLightbox(src);
    }
    return;
  }

  if (
    e.target.classList.contains("lightbox") ||
    e.target.classList.contains("close")
  ) {
    closeLightbox();
  }
});

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    closeLightbox();
  }
});

function applyPortfolioFilter() {
  const cat = (document.getElementById("catFilter")?.value || "all").toLowerCase();
  const q = (document.getElementById("searchInput")?.value || "").toLowerCase().trim();

  const cards = document.querySelectorAll("#portfolioGrid .p-card");
  cards.forEach((card) => {
    const c = card.dataset.category || "";
    const title = card.dataset.title || "";
    const ev = card.dataset.event || "";

    const catOk = cat === "all" || c === cat;
    const qOk = q === "" || title.includes(q) || ev.includes(q);

    card.style.display = (catOk && qOk) ? "" : "none";
  });
}

document.addEventListener("input", (e) => {
  if (e.target.id === "searchInput" || e.target.id === "catFilter") {
    applyPortfolioFilter();
  }
});

document.addEventListener("click", (e) => {
  if (e.target.id === "resetBtn") {
    const cat = document.getElementById("catFilter");
    const s = document.getElementById("searchInput");
    if (cat) cat.value = "all";
    if (s) s.value = "";
    applyPortfolioFilter();
  }
});

document.addEventListener("DOMContentLoaded", () => {
  applyPortfolioFilter();
  closeLightbox();
});