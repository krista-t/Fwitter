//make sure if cookie is present, UI displays and behaves correctly
window.addEventListener("load", checkCookieExists)

function checkCookieExists() {
  document.querySelectorAll("#icons button").forEach((icon) => {
    icon.disabled = true
  })

  if (document.cookie) {
    console.log("true, cookie here")
    const tweetForm = document.querySelector(".tweet-form input")
    document.querySelector("#login-btn").classList.add("hidden")
    document.querySelector(".img").classList.remove("hidden")
    if (tweetForm) {
      document.querySelector(".tweet-form input").disabled = false;
    }

    //if user logged allow interaction
    const loggedUser = document.querySelector("#logged-user span").textContent
    let loggedUserTweets = document.querySelectorAll(`div[id='${loggedUser}']`)
    //enable only this buttons
    loggedUserTweets.forEach((tweet) => {
      let tweetBtns = tweet.querySelectorAll("#icons button")
      tweetBtns.forEach(btn =>
        btn.disabled = false
      )
    })

    document.querySelectorAll("#fweets a").forEach((a) => {
      console.log(a)
      a.style = "pointer-events:all"
    })

    const user = document.querySelector("#logged-user span").textContent
    console.log(user)
    if (user == "@admin") {
      console.log("i am admin")
      let deleteBtns = document.querySelectorAll("#delete")
      deleteBtns.forEach(btn =>
        btn.disabled = false
      )
      //admin cannot tweet
      document.querySelector("#tweet-form").classList.add("hidden")
      document.querySelector("#suggested").classList.add("hidden")
      document.querySelector("#trends").classList.add("hidden")
      document.querySelector("#admin").classList.remove("hidden")

    }

    //use history api for spa
    //history.replaceState(stateObj, "/", "tweets", )
  } else {
    document.querySelector("#tweet-btn").disabled = true;
    document.querySelector(".tweet-form input").value =
      "PLEASE LOGIN TO TWEET"
    document.querySelector(".tweet-form input").disabled = true;
    document.querySelectorAll("#icons button").forEach((icon) => {
      icon.disabled = true
    })
    //cannot visit single profile page
    document.querySelectorAll("#fweets a").forEach((a) => {
      console.log(a)
      a.style = "pointer-events:none"
    })
  }
}

let user = document.querySelector("a")
user.addEventListener("click", showProfile)

function showProfile(profile) {
  console.log(profile)

  console.log("click")

}

function closeTweetModal() {
  document.querySelector("#edit-tweet").classList.add("hidden")
  // document.querySelector("#tweet-edit-form").innerHTML = ""
  document.querySelector("#edit-tweet input").value = ""
}
//fetch tweets
async function tweet() {
  const form = event.target.form
  const connection = await fetch("/tweet", {
    method: "POST",
    body: new FormData(form)
  })
  if (!connection.ok) {
    alert("Tweet with text, an image or both")
    return
  }
  // Success
  let tweet = await connection.json()
  console.log(tweet)
  const tweet_form = document.querySelector("#tweet-form")
  const tweet_id = tweet.tweet_id
  let section_tweet = `
          <section id = "${tweet_id}"  class= "p-4 border-t border-slate-200">
          <div class="flex">
            <img class="flex-none w-12 h-12 rounded-full" src="/img/${tweet.user_image}"alt="photo">
            <div id="@{{tweet['user_name']}}"  class="w-full pl-4">
            <div class = "flex">
            <a href="/${tweet.user_name}" target:="_blank">
            <p class="screen-name font-bold  cursor-pointer">
            @${tweet.user_name}
            </p>
          </a>

            <p id = "time" class = "ml-auto text-sm text-gray-500">${tweet.tweet_created_at}</p>
          </div>
              <p class="font-thin">
               ${tweet.user_full_name}
              </p>
              <div id = "tweet-text" class="pt-2">
             ${tweet.tweet_text}
              </div>
              <img id = "tweet-img" class="mt-2 w-full object-cover h-22" src="/img/${tweet.src}">
              <div id = "icons" class="flex gap-12 w-full mt-4 text-lg">
              <button id = "delete"  onclick="deleteTweet('${tweet_id}')"><i  class="fa-solid fa-trash mr-auto cursor-pointer"></i> </button>
              <button onclick="showTweetToEdit('${tweet_id}')">
                <i class="fa-solid fa-pen mr-auto cursor-pointer"></i>
              </button>
            <button><i class="fa-solid fa-heart cursor-pointer  ml-auto"></i></button>
            </div>`
  document.querySelector("#fweets").insertAdjacentHTML("afterbegin", section_tweet)
  if (tweet.src == "") {
    document.querySelector("#tweet-img").src = ""
  }
  tweet_form.reset()
}

//delete tweet
async function deleteTweet(tweet_id) {
  console.log(tweet_id)
  //Connect to the api and delete it from the db
  const connection = await fetch(`/delete_tweet/${tweet_id}`, {
    method: "DELETE"
  })
  console.log(document.querySelector(`section[id='${tweet_id}']`))
  document.querySelector(`[id='${tweet_id}']`).remove()
}

//show tweet to update//
function showTweetToEdit(tweet_id) {
  console.log("clicked")
  document.querySelector("#edit-tweet").classList.remove("hidden")
  let tweet = document.querySelector(`section[id='${tweet_id}']`)

  let tweet_text = tweet.querySelector("#tweet-text").textContent

  document.querySelector("#edit-tweet input").value = tweet_text
  console.log(document.querySelector("#edit-tweet input").value)
  let img = tweet.querySelector("#tweet-img")
  let edit_img = document.querySelector("#edit-image")
  console.log(edit_img)
  edit_img.style.display = "none"

  if (img !== null) {
    edit_img.src = img.src
    edit_img.style.display = "block"
  }

  document.querySelector("#edit-tweet button").setAttribute("id", tweet_id)
}


//update tweet
async function editTweet(tweet_id) {
  const form = event.target.form
  document.querySelector("#edit-tweet").classList.add("hidden")
  //Connect to the api and delete it from the db
  const connection = await fetch(`/edit_tweet/${tweet_id}`, {
    method: "PUT",
    body: new FormData(form)
  })
  if (!connection.ok) {
    alert("Could not tweet")
    return
  }
  //Success
  let editedTweet = await connection.json()
  console.log(editedTweet)
  let tweetSection = document.querySelector(`section[id='${tweet_id}']`)
  console.log(tweetSection)
  //if text is not changed leave it as is
  if (tweetSection.querySelector("#tweet-text").textContent != null) {
    tweetSection.querySelector("#tweet-text").textContent = editedTweet.tweet_text
  } else {
    tweetSection.querySelector("#tweet-text").textContent = tweetSection.querySelector("#tweet-text").textContent
  }
  console.log(editedTweet.tweet_updated_at)
  document.querySelector("#time").textContent = editedTweet.tweet_updated_at
}
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
  console.log("click")
  document.querySelector("#login").classList.remove("hidden")

}

//loggedin
async function logUser() {
  const form = event.target.form
  const connection = await fetch("/login", {
    method: "POST",
    body: new FormData(form)
  })
  let loggedUserValidation = await connection.json()
  console.log(loggedUserValidation)
  document.querySelector("#server-error-msg").innerHTML = loggedUserValidation["msg"]
  document.querySelector("#server-error-msg").style.color = "red"
  console.log(connection)
  if (!connection.ok) {
    console.log("Cannot log in")
  }

  if (loggedUserValidation.msg === "User does not exist!") {
    window.location = "/signup"
  } else {
    //only if backend validation passes
    if (loggedUserValidation.success) {
      document.querySelector(".img").classList.remove("hidden")
      const loggedUser = `@${loggedUserValidation.user}`
      let loggedUserTweets = document.querySelectorAll(`div[id='${loggedUser}']`)

      //enable only this buttons
      loggedUserTweets.forEach((tweet) => {
        let tweetBtns = tweet.querySelectorAll("#icons button")
        tweetBtns.forEach(btn =>
          btn.disabled = false
        )
      })
      document.querySelectorAll("#fweets a").forEach((a) => {
        console.log(a)
        a.style = "pointer-events:all"
      })
      document.querySelector("#logged-user span").textContent = loggedUser
      document.querySelector("#left-panel-img").src = "/img/" + loggedUserValidation.image + ""
      document.querySelector("#login").classList.add("hidden")
      document.querySelector("#login-btn").classList.add("hidden")
      document.querySelector("#tweet-btn").disabled = false;
      document.querySelector(".tweet-form input").value = null
      document.querySelector(".tweet-form input").disabled = false;

      if (loggedUserValidation.user == "admin") {
        let tweetBtns = document.querySelectorAll("#delete")
        tweetBtns.forEach(btn =>
          btn.disabled = false
        )
        //admin cannot post tweets
        document.querySelector("#tweet-form").classList.add("hidden")
        //document.querySelector("#suggested").classList.add("hidden")
        document.querySelector("#trends").classList.add("hidden")
        document.querySelector("#admin").classList.remove("hidden")
        document.querySelector("#left-panel-img").src = "/img/blank.png"
      }
    }
  }
}

//remove white spaces from edit tweet input
function removeWhiteSpaces(string) {
  //remove only spaces not tabs, newlines, etc
  let newString = string.replace(/  +/g, ' ')
  return newString
}