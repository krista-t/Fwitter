function _all(q, e = document) {
  return e.querySelectorAll(q)
}

function _one(q, e = document) {
  return e.querySelector(q)
}
// ##############################
function validate(callback) {
  console.log(callback)
  event.preventDefault()
  //event on btn
  const form = event.target.parentElement
  const validate_error = "rgba(240, 130, 240, 0.1)"
  _all("[data-validate]", form).forEach(function (element) {
    //target p with error message ADDED
    element.style.borderColor = "grey"
    element.previousElementSibling.classList.add("hidden")
    element.classList.remove("validate_error")
    element.style.backgroundColor = "white"
  })
  _all("[data-validate]", form).forEach(function (element) {
    switch (element.getAttribute("data-validate")) {
      case "str":
        if (element.value.length < parseInt(element.getAttribute("data-min")) ||
          element.value.length > parseInt(element.getAttribute("data-max"))
        ) {
          element.classList.add("validate_error")
          element.style.backgroundColor = validate_error
          element.style.borderColor = "red"
          //target p with error message
          element.previousElementSibling.style.color = "red"
          element.previousElementSibling.classList.remove("hidden")
        }
        break;
      case "int":
        if (!/^\d+$/.test(element.value) ||
          parseInt(element.value) < parseInt(element.getAttribute("data-min")) ||
          parseInt(element.value) > parseInt(element.getAttribute("data-max"))
        ) {
          element.classList.add("validate_error")
          element.style.backgroundColor = validate_error
        }
        break;
      case "email":
        let re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        if (!re.test(element.value.toLowerCase())) {
          element.classList.add("validate_error")
          element.style.backgroundColor = validate_error
          element.previousElementSibling.style.color = "red"
          element.previousElementSibling.classList.remove("hidden")
        }
        break;
      case "re":
        let regex = new RegExp(element.getAttribute("data-re"));
        if (!regex.test(element.value)) {
          console.log("email error")
          element.classList.add("validate_error")
          element.style.backgroundColor = validate_error
        }
        break;
      case "match":
        if (element.value != _one(`[name='${element.getAttribute("data-match-name")}']`, form).value) {
          element.classList.add("validate_error")
          element.style.backgroundColor = validate_error
        }
        break;
    }
  })
  if (!_one(".validate_error", form)) {
    callback();
    return
  }
}