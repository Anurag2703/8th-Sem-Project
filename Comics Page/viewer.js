// Get the PDF path from URL
const params = new URLSearchParams(window.location.search);
const pdfUrl = params.get('pdf');

// Set PDF in iframe using Google Docs viewer (no toolbar)
if (pdfUrl) {
    document.getElementById('pdfViewer').src =
        `https://docs.google.com/gview?url=${location.origin}${pdfUrl}&embedded=true`;
}

// Disable key shortcuts (Ctrl+S, Ctrl+P, etc.)
document.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && ['s', 'p', 'u'].includes(e.key.toLowerCase())) {
        e.preventDefault();
    }
});


// Erase all comments
document.getElementById("eraseCommentsBtn").addEventListener("click", async () => {
    const params = new URLSearchParams(window.location.search);
    const pdfPath = params.get("pdf");
    const pdfName = pdfPath.split('/').pop(); // e.g., "1.pdf"

    const response = await fetch("http://localhost:8000/erase_comment", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ pdf_name: pdfName })
    });

    const result = await response.json();
    alert(result.message);
    window.location.reload();
});
