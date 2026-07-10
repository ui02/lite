const image = document.getElementById("image");

const button = document.getElementById("postButton");

image.addEventListener("change", () => {

    // 画像が選ばれた時の処理

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