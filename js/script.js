let stateObj = {
  landingPage: "/"

}
//make sure if cookie is present, UI displays correctly
window.addEventListener("load", checkCookieExists)
function checkCookieExists() {
  if (document.cookie) {
    console.log("true, cookie here")
    document.querySelector("#login-btn").classList.add("hidden")
     //use history api for spa
     //history.replaceState(stateObj, "/", "tweets", )
     //console.log(stateObj)
  }
}
function closeTweetModal(){
  document.querySelector("#edit-tweet").classList.add("hidden")
  document.querySelector("#tweet-edit-form").innerHTML = ""
}
//fetch tweets
async function tweet() {
  const form = event.target.form
  const connection = await fetch("/tweet", {
    method: "POST",
    body: new FormData(form)
  })
  if (!connection.ok) {
    alert("Could not tweet")
    return
  }
  // Success
  let tweet = await connection.json()
  const tweet_form = document.querySelector("#tweet-form")
  const tweet_id = tweet.tweet_id
  let section_tweet = `
          <div id = "${tweet_id}"  class= "p-4 border-t border-slate-200">
          <div class="flex">
            <img class="flex-none w-12 h-12 rounded-full" src="" alt="photo">
            <div class="w-full pl-4">
              <p class="font-bold">
               @ INSERT USERNAME
              </p>
              <p class="font-thin">
               INSERT user_full_name
              </p>
              <div class="pt-2">
             ${tweet.tweet_text}
              </div>
              <img id = "tweet-img" class="mt-2 w-full object-cover h-22" src="/img/${tweet.src}">
              <div class = "flex gap-12 w-full mt-4 text-lg">
              <i onclick="deleteTweet('${tweet_id}')" class="fa-solid fa-trash mr-auto cursor-pointer"></i>
              <i onclick = "toggleEditTweetModal()" class="fa-solid fa-pen mr-auto cursor-pointer"></i>
              <i class="fa-solid fa-heart cursor-pointer  ml-auto"></i>
             </div>`
  document.querySelector("#fweets").insertAdjacentHTML("afterbegin", section_tweet)
  if (tweet.src == "") {
    document.querySelector("#tweet-img").src = ""
  }
  tweet_form.reset()
}

//delete tweet
async function deleteTweet(tweet_id){
  console.log(tweet_id)
  //Connect to the api and delete it from the db
 const connection = await fetch(`/delete_tweet/${tweet_id}`, {
   method: "DELETE"
 })
 console.log(document.querySelector(`[id='${tweet_id}']`))
 document.querySelector(`[id='${tweet_id}']`).remove()
}



//show tweet to update
async function showTweetToEdit(tweet_id){
  console.log(tweet_id)
  document.querySelector("#edit-tweet").classList.remove("hidden")
  //Connect to the api and delete it from the db
 const connection = await fetch(`/edit_tweet/${tweet_id}`, {
   method: "GET"
 })
   console.log(connection)
   if (!connection.ok) {
    alert("Could not show tweet")
    return
  }
let tweet_to_edit= `
<label for="txt-tweet" class="w-full font-thin text-sm text-gray-400 pt-2 pl-4">Tweet with image or text up
to 100 characters, or both</label>
<!-- reference validation here for text input only -->
<input name="tweet_text" id="txt-tweet"
class="w-full h-12 p-4 text-gray-800 rounded outline-none placeholder:text-gray-800" type="text"
placeholder="What is on your mind?" data-validate="str" data-max="100">
<label>
<input id="upload" class="absolute bottom-2 left-2 text-sm " type="file" name="image">
<i class="fa-solid fa-image absolute bottom-2 left-4 text-3xl cursor-pointer text-gray-700"></i>
</label>
<button id="tweet-btn" onclick=" " type="submit"
class="absolute bottom-2 right-2 px-8 py-2 bg-blue-400 text-white rounded-full">
Update Tweet
</button>`
document.querySelector("#tweet-edit-form").insertAdjacentHTML("afterbegin", tweet_to_edit)

}




//update tweet
async function editTweet(tweet_id){
  console.log(tweet_id)

  //Connect to the api and delete it from the db
 const connection = await fetch(`/edit_tweet/${tweet_id}`, {
   method: "PUT"
 })
   console.log(connection)
   if (!connection.ok) {
    alert("Could not tweet")
    return
  }
 console.log(document.querySelector(`[id='${tweet_id}']`))
 //document.querySelector(`[id='${tweet_id}']`).update()
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

  } else {
    //check is all validations are successfull and redirect to homepage
    if (userData.success) {
      console.log("success")
      window.location = "/"
    }
  }
}

function showLogInForm() {
  document.querySelector("#login").classList.remove("hidden")
  history.pushState(stateObj, "login", "login")
  //console.log(stateObj)
}

//fetch loggedin
async function logUser() {
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
  } else {
    //check is all validations are successfull, hide login popup, and show logout btn
    if (loggedUserValidation.success) {
      console.log("success")
      document.querySelector("#login").classList.add("hidden")
      document.querySelector("#login-btn").classList.add("hidden")
      history.pushState(stateObj, "/", "tweets")

    }
  }
}