document.addEventListener("DOMContentLoaded", function () {
    // Check if ePub.js is loaded correctly
    if (typeof ePub === "undefined") {
        console.error("ePub.js is not loaded correctly.");
        return;
    }

    const container = document.getElementById("epub-container");

    // Replace with actual EPUB path
    const epubPath = "/mylib/static/pdfs/demo.epub";
    const book = ePub(epubPath);
    console.log(ePub); // Should print the ePub object if loaded


    const rendition = book.renderTo(container, {
        width: "100%",
        height: "100%"
    });
    console.log(rendition);
    rendition.display();

    // When the EPUB is ready, log success
    book.on("ready", function () {
        console.log("EPUB loaded successfully");
    });

    // Handle error during opening of EPUB
    book.on("openFailed", function (error) {
        console.error("Failed to open EPUB:", error);
    });

    // Handle errors in EPUB.js
    book.on("error", function (error) {
        console.error("EPUB.js encountered an error:", error);
    });

    document.getElementById("prev").addEventListener("click", () => {
        rendition.prev();
    });

    document.getElementById("next").addEventListener("click", () => {
        rendition.next()
    });
});
