$(function() {
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname);
    
    chatsock.onmessage = function(message) {
        var data = JSON.parse(message.data);
        var $chat = $("#chat-messages");

        var $msg = $("#message-template").children().clone();
        $msg.find(".author").html(data.user);
        $msg.find(".date").html(data.timestamp);
        $msg.find(".text").html("<p>"+data.message+"</p>");

        $chat.append($msg);
        $chat.scrollTop($chat[0].scrollHeight);
    };

    $("#chatform").on("submit", function(event) {
        event.preventDefault();
        var message = {
            message: $('#message').val(),
        };
        chatsock.send(JSON.stringify(message));
        $("#message").val('').focus();

        return false;
    });
});