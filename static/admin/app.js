<script>

const button = document.getElementById("postButton");

button.addEventListener("click", () => {

    const title = document.getElementById("title").value;

    const content = document.getElementById("content").value;

    alert(
        "タイトル\n" +
        title +
        "\n\n本文\n" +
        content
    );

});

</script>
