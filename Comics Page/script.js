// Comment submit
async function submitComment(button) {
    const form = button.parentElement;
    const storyId = form.querySelector(".story-id").value;
    const comment = form.querySelector(".comment-text").value;

    const formData = new FormData();
    formData.append("story_id", storyId);
    formData.append("comment", comment);

    try {
        const response = await fetch("http://127.0.0.1:8000/add-comment/", {
            method: "POST",
            body: formData
        });

        const result = await response.json();
        form.querySelector(".response-msg").textContent = result.message || result.error;
    } catch (error) {
        form.querySelector(".response-msg").textContent = "Error sending comment.";
    }
}



