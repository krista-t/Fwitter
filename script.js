window.addEventListener("load", checkCookieExists)

function checkCookieExists(){
  if(document.cookie){
    console.log("true, cookie here")
    document.querySelector("#login-btn").classList.add("hidden")
  }
}

//fetch tweets
async function tweet() {
    const form = event.target.form
     const connection = await fetch("/tweet", {
       method: "POST",
       body: new FormData(form)
     })
     console.log(connection)
     if (!connection.ok) {
       alert("Could not tweet")
       return
     }
     // Success
     let tweet = await connection.json()
      console.log(tweet)

     //INSERT  <img class="mt-2 w-full object-cover h-20" src=${tweet.image}> INTO GAP DOWN
     let section_tweet = `
          <div class="p-4 border-t border-slate-200">
          <div class="flex">
            <img class="flex-none w-12 h-12 rounded-full" src="" alt="photo">
            <div class="w-full pl-4">
              <p class="font-bold">
               @ INSERT USERNAME
              </p>
              <p class="font-thin">
               INSERT user
              </p>
              <div class="pt-2">
              ${tweet.text}
              </div>
              <img class="mt-2 w-full object-cover h-22" src="/img/${tweet.src}">
              <div class="flex gap-12 w-full mt-4 text-lg">
                  <i class="fa-solid fa-message ml-auto"></i>
                  <i class="fa-solid fa-heart"></i>
                  <i class="fa-solid fa-retweet"></i>
                  <i class="fa-solid fa-share-nodes"></i>
              </div>
            </div>
          </div>
        </div>`
     document.querySelector(".fweets").insertAdjacentHTML("afterbegin", section_tweet)
     console.log(document.querySelector("#tweet-formm").value)

   }

   //////////
   //fetch users
   async function createUser() {
      const form = event.target.form;
      const connection = await fetch("/signup", {
        method: "POST",
        body: new FormData(form)

      })
      let userData = await connection.json()
      document.querySelector("#server-error-msg").innerHTML = userData["msg"]
      document.querySelector("#server-error-msg").style.color = "red"
      console.log(userData)
      if (!connection.ok) {
        console.log("Cannot sign up")

      }else{
        //check is all validations are successfull and redirect to homepage
        if (userData.success) {
          console.log("success")
          window.location = "/"
        }
      }
     }

     function showLogInForm(){
       document.querySelector("#login").classList.remove("hidden")
     }

       //fetch loggedin
       async function logUser(){
         const form = event.target.form
          const connection = await fetch("/login", {
            method: "POST",
            body: new FormData(form)
          })
          let loggedUserValidation = await connection.json()
          document.querySelector("#server-error-msg").innerHTML = loggedUserValidation["msg"]
          document.querySelector("#server-error-msg").style.color = "red"
          console.log(loggedUserValidation)
          console.log(connection)
          if (!connection.ok) {
            console.log("Cannot sign up")
            }

             if (loggedUserValidation.msg === "User does not exist!") {
               window.location = "/signup"
             }
           else{
             //check is all validations are successfull, hide login popup, and show logout btn
             if (loggedUserValidation.success) {
               console.log("success")
               document.querySelector("#login").classList.add("hidden")
               document.querySelector("#login-btn").classList.add("hidden")
             }
           }
         }