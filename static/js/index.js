// delete ensure functions:
function deleteEnsure(e) {
  e.parentElement.children[6].style.opacity = 1;
  e.parentElement.children[6].style.visibility = "visible";
}

function closeEnsure(e) {
  e.parentElement.style.opacity = 0;
  e.parentElement.style.visibility = "hidden";
}

// info for user:
var navIcons = document.querySelectorAll("#nav-img");
navIcons.forEach((elem) => {
  elem.parentElement.addEventListener(
    "mouseover",
    (e) => {
      var body = document.getElementsByTagName("BODY")[0];
      var left = e.clientX + "px";
      var top = (Number(e.clientY) + 20).toString() + "px";
      var popup = document.createElement("DIV");
      popup.setAttribute("id", "popup");
      popup.style.top = top;
      popup.style.left = left;
      var popupText = document.createElement("P");
      popupText.innerText = elem.parentElement.dataset.help;
      popup.appendChild(popupText);
      body.appendChild(popup);
    },
    false
  );

  elem.parentElement.addEventListener(
    "mouseout",
    (e) => {
      document.getElementById("popup").remove();
    },
    false
  );
});

// zooming pictures:
var postImages = document.querySelectorAll(".post-image");
postImages.forEach((elem) => {
  elem.addEventListener("click", (e) => {
    elem.classList.toggle("zoomed-image");
    document.getElementById("dimmer").classList.toggle("dim");
  });
});

// home redirect:
document.querySelector("#logo").addEventListener("click", (e) => {
  location.href = document.querySelector("#logo").dataset.url;
});

// alert coold down:
var alrt = document.querySelector(".dj-message");
setTimeout(() => {
  try {
    alrt.style.opacity = "0";
    alrt.style.visibility = "hidden";
  } catch (err) {}
}, 3000);
