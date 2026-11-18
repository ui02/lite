document.addEventListener("DOMContentLoaded", () => {
  const dialog = document.getElementById("image-lightbox");
  const lightboxImage = document.getElementById("lightbox-image");
  const closeButton = document.getElementById("lightbox-close");
  const prevButton = document.getElementById("lightbox-prev");
  const nextButton = document.getElementById("lightbox-next");
  const counter = document.getElementById("lightbox-counter");

  if (!dialog || !lightboxImage) return;

  let galleryImages = [];
  let currentIndex = 0;

  function showImage(index) {
    currentIndex = (index + galleryImages.length) % galleryImages.length;

    const link = galleryImages[currentIndex];
    const image = link.querySelector("img");

    lightboxImage.src = link.href;
    lightboxImage.alt = image ? image.alt : "";

    if (counter) {
      counter.textContent = `${currentIndex + 1} / ${galleryImages.length}`;
    }
  }

  function openLightbox(link) {
    const gallery = link.closest(".image-gallery");
    if (!gallery) return;

    galleryImages = Array.from(
      gallery.querySelectorAll("a[href]"),
    ).filter((item) => item.querySelector("img"));

    currentIndex = galleryImages.indexOf(link);
    if (currentIndex < 0 || galleryImages.length === 0) return;

    showImage(currentIndex);
    dialog.showModal();
  }

  document.addEventListener("click", (event) => {
    const link = event.target.closest(".image-gallery a");

    if (!link || !dialog) return;

    event.preventDefault();
    openLightbox(link);
  });

  prevButton?.addEventListener("click", () => {
    showImage(currentIndex - 1);
  });

  nextButton?.addEventListener("click", () => {
    showImage(currentIndex + 1);
  });

  closeButton?.addEventListener("click", () => {
    dialog.close();
  });

  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) {
      dialog.close();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (!dialog.open) return;

    if (event.key === "ArrowLeft") {
      showImage(currentIndex - 1);
    } else if (event.key === "ArrowRight") {
      showImage(currentIndex + 1);
    }
  });

  dialog.addEventListener("close", () => {
    lightboxImage.src = "";
  });
});
