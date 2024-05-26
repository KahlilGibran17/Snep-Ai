const chooseFile = document.getElementById("image");
const imgPreview = document.getElementById("img-view");
const iconCont = document.getElementById("icon-container");

const validationHistoryList = document.getElementById("news-item-list");
const historyList = document.getElementById("news-item-list");

const submitBtn = document.getElementById("submit");
const result = document.getElementById("result");

const titleInput = document.getElementById("input-title");
const titleInput_p = document.getElementById("title");
const contentInput = document.getElementById("input-content");
const dateInput = document.getElementById("input-date");

var picture;

document.addEventListener("DOMContentLoaded", function() {

  if (chooseFile != null) {

    chooseFile.addEventListener("change", function () {
      getImgData();
    });
  
    function getImgData() {
      const files = chooseFile.files[0];
      if (files) {
        const fileReader = new FileReader();
        fileReader.readAsDataURL(files);
        fileReader.addEventListener("load", function () {
          iconCont.style.display = "none";
          imgPreview.style.display = "block";
          imgPreview.innerHTML = '<img src="' + this.result + '" id="input-image"/>';

          picture  = fileReader.result.replace("data:", "")
          .replace(/^.+,/, "");

        });
      }
    }

  }

  if (submitBtn != null){

    submitBtn.addEventListener("click", function prompt(){
      result.innerHTML = "Processing..."

      let type = document.getElementById("type").value
      console.log(type)
      
      if (titleInput_p == null){

        // assign input into json
        const formData = {
          "title": titleInput.value,
          "content": contentInput.value,
          "date": dateInput.value,
          "informationType": type
        }
        // call api
        const response = fetch("/informationValidation", {
          method: "POST",
          body: JSON.stringify(formData),
          headers: {
            "Content-Type" : "application/json"
          }
        }).then(response => {
          // get api response
          const data = response.json()
          console.log(data);
          const promise = Promise.resolve(data);
          promise.then((value) => {
            // processing response
            result.innerHTML = value.response
            submitBtn.disabled = true
            if (!value.isSuccess){
              messageElement.classList.add("error");
              throw new Error(
                value.response
              );
            }
          })
        })

      }else{

        if(picture != undefined){

          // assign input into json
          const formData = {
            "title": titleInput_p.value,
            "content": picture,
            "date": dateInput.value,
            "informationType": type
          }
          // call api
          const response = fetch("/informationValidation_Picture", {
            method: "POST",
            body: JSON.stringify(formData),
            headers: {
              "Content-Type" : "application/json"
            }
          }).then(response => {
            // get api response
            const data = response.json()
            console.log(data);
            const promise = Promise.resolve(data);
            promise.then((value) => {
              // processing response
              result.innerHTML = value.response
              submitBtn.disabled = true
              if (!value.isSuccess){
                messageElement.classList.add("error");
                throw new Error(
                  value.response
                );
              }
            })
          })

        }else{
    
          result.innerHTML = "Please insert picture"

        }

      }
  
    })

  }

  function createHistoryElement(title = "title", content = "content", decision = true, accuracy = 0){

    console.log(message);

    const newsLi = document.createElement("li");

    let newsContent = '<div class="news-item"><a href=""><div class="d-flex justify-content-between"><h6 class="news title">' + title + '</h6><div class="d-flex gap-2 head-stat"><span class="status' + decision + '">' + decision + '</span><span class="prob">' + accuracy + '</span></div></div><span class="new snippet">' + content + '</span></a></div>';

    newsLi.innerHTML = newsContent;

    return newsLi;
  }

  function processResponse(promptLog){
    // Regular expression pattern to match the title and content
    const regex =  /Title: (.*?), Content: (.*?), Decision: (.*?), Accuracy: (.*)/;;
    // format
    let inputString = "Title: titleContent, Content: content, Decision: true, Accuracy: 0";

    const match = response.match(regex);

    if (match) {
      // Extract the matched groups
      const title = match[1].trim();
      const content = match[2].trim();
      const decision = match[3].trim() === 'true'; // Convert string 'true' to boolean true
      const accuracy = parseFloat(match[4].trim()); // Convert string to number
  
      // Output the result
      console.log("Title:", title);
      console.log("Content:", content);
      console.log("Decision:", decision);
      console.log("Accuracy:", accuracy);
    } else {
      console.log("No match found.");
    }

    createHistoryElement()
    createHistoryElement(title, content, decision, accuracy)

    for(let i = 0; i < promptLog.length; i++) {
      let response = promptLog[i]
      console.log(response)

      const match = response.match(regex);

      if (match) {
          // Extract the title and content from the matched groups
          const title = match[1].trim();
          const content = match[2].trim();

          // Output the result
          historyList.appendChild(createHistoryElement(title))
      } else {
          console.log("No match found.");
      }
    }

  }

  // histoy load to get history
  window.addEventListener("load", function load(){

    const response = fetch("/getPromptLog", {
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
          let promptLog = value.promptLog
          processResponse(promptLog)
        } catch(e) {
          console.log(e.message)
        }
      })
    })
  })

});