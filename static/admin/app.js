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

    if (selectedImage) {

        alert(
            "タイトル\n" +
            title +
            "\n\n本文\n" +
            content +
            "\n\n画像\n" +
            selectedImage.name
        );

    } else {

        alert(
            "タイトル\n" +
            title +
            "\n\n本文\n" +
            content +
            "\n\n画像なし"
        );

    }

});