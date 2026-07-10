const image = document.getElementById("image");
const preview = document.getElementById("preview");
const button = document.getElementById("postButton");

image.addEventListener("change", () => {

    const file = image.files[0];

    if (file) {
        preview.src = URL.createObjectURL(file);
        preview.style.display = "block";
    } else {
        preview.src = "";
        preview.style.display = "none";
    }

});

button.addEventListener("click", () => {

    const title = document.getElementById("title").value;

    const content = document.getElementById("content").value;

    const selectedImage = image.files[0];

    const post = {
        title: title,
        content: content,
        images: Array.from(image.files)
    };

    if (post.Image) {

        alert(
            "タイトル\n" +
            post.title +
            "\n\n本文\n" +
            post.content +
            "\n\n画像\n" +
            post.images.length
        );

    } else {

        alert(
            "タイトル\n" +
            post.title +
            "\n\n本文\n" +
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