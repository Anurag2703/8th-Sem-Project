// Comment submit
async function submitComment() {
    const storyId = document.getElementById("storyId").value;
    const comment = document.getElementById("commentText").value;

    const formData = new FormData();
    formData.append("story_id", storyId);
    formData.append("comment", comment);

    const response = await fetch("http://127.0.0.1:8000/add-comment/", {
        method: "POST",
        body: formData
    });

    const result = await response.json();
    document.getElementById("responseMsg").textContent = result.message || result.error;
}


