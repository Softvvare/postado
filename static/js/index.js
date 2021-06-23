// onload scroll continue where you left off:
document.querySelectorAll(".interactions a").forEach((elem) => {
  elem.addEventListener("click", (e) => {
    localStorage.setItem("windowLocation", document.location);
    localStorage.setItem("windowScrollPosition", window.scrollY);
  });
});

// scroll to last position:
window.onload = () => {
  window.scrollTo({
    left: 0,
    top: localStorage.getItem("windowScrollPosition"),
    behavior: "smooth",
  });
};

// set scroll position to 0 if navbar is used:
document.querySelectorAll(".nav-item").forEach((elem) => {
  elem.addEventListener("click", (e) => {
    localStorage.setItem("windowScrollPosition", 0);
  });
});

// back to the page where you left off:
try {
  document.getElementById("back-left-off").addEventListener("click", (e) => {
    window.location.href = localStorage.getItem("windowLocation");
  });
} catch (err) {}

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
      try {
        document.getElementById("popup").remove();
      } catch (err) {}
    },
    false
  );
});

// zooming pictures:
var postImages = document.querySelectorAll(".post-image");
postImages.forEach((elem) => {
  elem.addEventListener("click", (e) => {
    document.getElementById("dimmer").classList.toggle("dim");

    if (document.getElementById("dimmer").classList.contains("dim")) {
      document.body.style.overflow = "hidden";
      try {
        document.querySelector(".profile-posts").style.backdropFilter = "none";
      } catch (err) {}
    } else {
      document.body.style.overflow = "auto";
      try {
        document.querySelector(".profile-posts").style.backdropFilter =
          "blur(20px)";
      } catch (err) {}
    }

    elem.classList.toggle("zoomed-image");
  });
});

// home redirect:
document.querySelector("#logo").addEventListener("click", (e) => {
  location.href = document.querySelector("#logo").dataset.url;
});

// from feed to profile:
document.querySelectorAll(".post-person-image").forEach((elem) => {
  elem.addEventListener("click", (e) => {
    window.location.href = elem.dataset.url;
  });
});

// open liked users popup:
document.querySelectorAll(".like-count").forEach((elem) => {
  var popUpWindow =
    elem.parentElement.parentElement.parentElement.lastElementChild;
  elem.addEventListener("click", (e) => {
    popUpWindow.classList.toggle("liked-popup-active");
  });
  popUpWindow.children[0].addEventListener("click", (e) => {
    if (popUpWindow.classList.contains("liked-popup-active")) {
      popUpWindow.classList.remove("liked-popup-active");
    }
  });
});

// alert coold down:
var alrt = document.querySelector(".dj-message");
setTimeout(() => {
  try {
    alrt.style.opacity = "0";
    alrt.style.visibility = "hidden";
  } catch (err) {}
}, 3000);

try {
  // going to following profile:
  var fprofiles = document.querySelectorAll("#ff-user");
  fprofiles.forEach((elem) => {
    elem.addEventListener("click", (e) => {
      window.location.href = elem.dataset.purl;
    });
  });

  // profile popup close:
  var popupCloseBtn = document.querySelectorAll(".popup-close");
  popupCloseBtn.forEach((elem) => {
    elem.addEventListener("click", (e) => {
      document.querySelectorAll(".popup-f").forEach((element) => {
        element.classList.add("popup-unactive");
      });
    });
  });

  // followings popup open:
  var followingsPopup = document.querySelector("#open-followings");
  followingsPopup.addEventListener("click", (e) => {
    if (
      !document
        .querySelector("#follower-popup")
        .classList.contains("popup-unactive")
    ) {
      document.querySelector("#follower-popup").classList.add("popup-unactive");
    }
    document
      .querySelector("#following-popup")
      .classList.remove("popup-unactive");
  });

  // follower popup open:
  var followingsPopup = document.querySelector("#open-followers");
  followingsPopup.addEventListener("click", (e) => {
    if (
      !document
        .querySelector("#following-popup")
        .classList.contains("popup-unactive")
    ) {
      document
        .querySelector("#following-popup")
        .classList.add("popup-unactive");
    }
    document
      .querySelector("#follower-popup")
      .classList.remove("popup-unactive");
  });
} catch (err) {}

// post detailed view:
try {
  document.querySelectorAll(".post-ctx").forEach((elem) => {
    elem.addEventListener("click", (e) => {
      window.location.href = elem.dataset.url;
    });
  });
} catch (err) {}

// go into room:
try {
  document.querySelectorAll(".room").forEach((elem) => {
    elem.addEventListener("click", (e) => {
      console.log(elem.dataset.url);
      window.location.href = elem.dataset.url;
    });
  });
} catch (err) {}
