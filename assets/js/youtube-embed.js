document.addEventListener("DOMContentLoaded", () => {
  const links = document.querySelectorAll(
    ".diary-post-content a[href]"
  );

  links.forEach(link => {
    const paragraph = link.closest("p");

    // URLだけの段落を対象にする
    if (!paragraph || paragraph.textContent.trim() !== link.textContent.trim()) {
      return;
    }

    let url;

    try {
      url = new URL(link.href);
    } catch {
      return;
    }

    let videoId = "";

    if (url.hostname === "www.youtube.com" ||
        url.hostname === "youtube.com" ||
        url.hostname === "www.youtube-nocookie.com" ||
        url.hostname === "youtube-nocookie.com") {
      if (url.pathname === "/watch") {
        videoId = url.searchParams.get("v") || "";
      } else if (url.pathname.startsWith("/embed/")) {
        videoId = url.pathname.split("/")[2] || "";
      }
    } else if (url.hostname === "youtu.be") {
      videoId = url.pathname.slice(1);
    }

    if (!/^[a-zA-Z0-9_-]{11}$/.test(videoId)) {
      return;
    }

    const wrapper = document.createElement("div");
    wrapper.className = "youtube-container";

    const iframe = document.createElement("iframe");
    iframe.src = `https://www.youtube-nocookie.com/embed/${videoId}`;
    iframe.title = "YouTube video player";
    iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
    iframe.referrerPolicy = "strict-origin-when-cross-origin";
    iframe.allowFullscreen = true;
    iframe.loading = "lazy";

    wrapper.appendChild(iframe);
    paragraph.replaceWith(wrapper);
  });
});
