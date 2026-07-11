const WORKER_URL = "https://iolite-cms.ylpyz1989.workers.dev/";

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


button.addEventListener("click", async () => {


    const content = document.getElementById("content").value;

    const post = {
        content: content,
        images: Array.from(image.files)
    };


    const response = await fetch(
        WORKER_URL,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                content: post.content
            })
        }
    );


    const result = await response.json();


    if (result.success) {
        alert("投稿しました！");
    } else {
        alert("投稿に失敗しました");
    }

});