// NAVBAR
const navbarLinks = document.querySelectorAll('.navbar-link');

navbarLinks.forEach(link => {
    link.addEventListener('mouseenter', () => {
        navbarLinks.forEach(otherLink => {
            if (otherLink !== link) {
                otherLink.classList.add('blur');
            }
        });
    });

    link.addEventListener('mouseleave', () => {
        navbarLinks.forEach(otherLink => {
            otherLink.classList.remove('blur');
        });
    });
});



function scrollToBottom() {
    var messageBody = document.getElementById("messageFormeight");
    messageBody.scrollTop = messageBody.scrollHeight;
}

$(document).ready(function () {
    $("#messageArea").on("submit", function (event) {
        const date = new Date();
        const str_time =
        date.getHours() + ":" + String(date.getMinutes()).padStart(2, "0");
        var rawText = $("#text").val();

        var userHtml = `
            <div class="d-flex justify-content-end mb-4">
            <div class="msg_cotainer_send">${rawText}
                <span class="msg_time_send">${str_time}</span>
            </div>
            <div class="img_cont_msg">
                <img src="https://i.ibb.co/d5b84Xw/Untitled-design.png" class="rounded-circle user_img_msg">
            </div>
            </div>
        `;

        $("#text").val("");
        $("#messageFormeight").append(userHtml);
        scrollToBottom();

        $.ajax({
        data: { msg: rawText },
        type: "POST",
        url: "/get",
        })
        .done(function (data) {
            var botHtml = `
            <div class="d-flex justify-content-start mb-4">
                <div class="img_cont_msg">
                <img src="https://i.ibb.co/fSNP7Rz/icons8-chatgpt-512.png" class="rounded-circle user_img_msg">
                </div>
                <div class="msg_cotainer">${data}
                <span class="msg_time">${str_time}</span>
                </div>
            </div>
            `;
            $("#messageFormeight").append(botHtml);
            scrollToBottom();
        })
        .fail(function (xhr, status, error) {
            console.error("AJAX Error:", status, error);
            console.error("Server response:", xhr.responseText);
        });

        event.preventDefault();
    });
});
