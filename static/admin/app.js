const image = document.getElementById("image");
const preview = document.getElementById("preview");
const button = document.getElementById("postButton");

image.addEventListener("change", () => {

    preview.innerHTML = "";

    for (const file of image.files) {

        const img = document.createElement("img");

        img.src = URL.createObjectURL(file);

        img.style.maxWidth = "200px";
        img.style.margin = "10px";
        img.style.borderRadius = "8px";

        preview.appendChild(img);

    }

});

button.addEventListener("click", () => {

    const content = document.getElementById("content").value;

    const post = {
        content: content,
        images: Array.from(image.files)
    };

    if (post.images.length > 0) {

        alert(
            "本文\n" +
            post.content +
            "\n\n画像\n" +
            post.images.length
        );

    } else {

        alert(
            "本文\n" +
            post.content +
            "\n\n画像なし"
        );

    }

    const markdown = createMarkdown(post);

    console.log(markdown);

});

function createMarkdown(post) {

    return `---
title: "${post.title}"
date: ${new Date().toISOString()}
---

${post.content}`;
}