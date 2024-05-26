
// histoy load to get history
window.addEventListener("load", function load(){

    console.log('a')
  
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
          for(let i = 0; i < promptLog.length; i++) {
            let obj = promptLog[i]
            console.log(obj.input_information)
          }
        } catch(e) {
          console.log(e.message)
        }
      })
    })
  
  })