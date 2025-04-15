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