 //update tweet
 async function uploadProfilePic(id) {
    const form = event.target.form
    console.log("form")
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
    let updatedImg = await connection.json()
    document.querySelector("#profile-photo").src = "/img/" + updatedImg.user_image + ""
    document.querySelector("#main-img").src = "/img/" + updatedImg.user_image + ""
    document.querySelector("#left-panel-img").src = "/img/" + updatedImg.user_image + ""
  }