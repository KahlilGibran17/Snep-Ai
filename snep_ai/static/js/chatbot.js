const chatbox = document.querySelector(".chatbox");
const chatInput = document.getElementById("input-text-user");
const sendChatBtn = document.getElementById("send-btn");

// chat event listener
document.addEventListener("DOMContentLoaded", function () {
  let inputValue = null;
  const inputInitHeight = chatInput.scrollHeight;

  const createChatLi = (message, className) => {
    const chatLi = document.createElement("li");

    chatLi.classList.add("chat", className);

    let chatContent =
      className === "outgoing"
        ? `<p></p>`
        : `<i class="bx bx-bot icon"></i><p></p>`;

    chatLi.innerHTML = chatContent;
    chatLi.querySelector("p").textContent = message;
    return chatLi;
  };

  const generateResponse = (chatElement) => {
    const messageElement = chatElement.querySelector("p");
    messageElement.textContent = "Thinking...";

    try {
      // fetching api response
      const formData = { "prompt" : inputValue};
      const response = fetch("/chat", {
        method: "POST",
        body: JSON.stringify(formData),
        headers: {
          "Content-Type" : "application/json"
        }
      }).then(response => {
        // get api response
        const data = response.json()
        const promise = Promise.resolve(data);
        promise.then((value) => {
          // processing response
          messageElement.textContent = value.response;
          if (!value.isSuccess){
            messageElement.classList.add("error");
            throw new Error(
              value.response
            );
          }
        })
      })

    } catch (error) {
      messageElement.classList.add("error");
      messageElement.textContent = error.message;
    }

  };

  const handleChat = () => {
    inputValue = chatInput.value.trim();
    if (!inputValue) return;
    chatInput.value = "";

    chatbox.appendChild(createChatLi(inputValue, "outgoing"));
    chatbox.scrollTo(0, chatbox.scrollHeight);

    setTimeout(() => {
      const incomingChatLi = createChatLi("Thinking...", "incoming");
      chatbox.appendChild(incomingChatLi);
      chatbox.scrollTo(0, chatbox.scrollHeight);
      generateResponse(incomingChatLi);
    }, 600);
  };

  chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
      e.preventDefault();
      handleChat();
    }
  });

  sendChatBtn.addEventListener("click", handleChat);

  // fetch data on load
  const getChatLog = () => {
    const response = fetch("/getChatLog", {
      method: "GET",
    }).then(response => {
      // get api response
      const data = response.json()
      const promise = Promise.resolve(data);
      promise.then((value) => {
        // processing response
        try{
          if (!value.isSuccess){
            throw new Error (
              "error fetching chat log"
            )
          }
          let chatLog = value.chatLog
          for(let i = 0; i < chatLog.length; i++) {
            let obj = chatLog[i]
            user = createChatLi(obj.message, "outgoing")
            bot = createChatLi(obj.response, "incoming")
            chatbox.appendChild(user)
            chatbox.appendChild(bot)
          }
          chatbox.scrollTo(0, chatbox.scrollHeight);
        } catch(e) {
          console.log(e.message)
        }
      })
    })
  }

  getChatLog()

});