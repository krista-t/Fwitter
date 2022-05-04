//check who is logged in
function checkProfile() {
  document.querySelector("#login-btn").classList.add("hidden")
  document.querySelector("#logout-btn").classList.add("hidden")
  let loggedUser = document.querySelector("#logged-user span").textContent
  loggedUser = loggedUser.substring(1)
  let profileUser = document.querySelector("#user-info p").id
  if (loggedUser != profileUser) {
    console.log("NOT")
    document.querySelector("#profile-form button").disabled = true
    document.querySelector("#profile-form input").disabled = true
  } else {
   return
  }
}
checkProfile()


//update profile img
async function uploadProfilePic(id) {
  const form = event.target.form
  //Connect to the api
  const connection = await fetch(`/${id}`, {
    method: "PUT",
    body: new FormData(form)
  })

  console.log(connection)
  if (!connection.ok) {
    alert("Wrong image format, only .jpg, .jpeg, and png allowed")
    return
  }
  //Success
  let profileImg = document.querySelector("#profile-photo")
  let updatedImg = await connection.json()
  profileImg.src = "/img/" + updatedImg.user_image + ""
  document.querySelector("#main-img").src = "/img/" + updatedImg.user_image + ""
  document.querySelector("#left-panel-img").src = "/img/" + updatedImg.user_image + ""
}