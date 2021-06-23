try {
  document.querySelector("#share").addEventListener("click", (e) => {
    console.log(window.location.origin + e.target.parentElement.dataset.copy);
    var textArea = document.createElement("textarea");
    textArea.value =
      window.location.origin + e.target.parentElement.dataset.copy;
    document.body.appendChild(textArea);
    textArea.select();
    try {
      var successful = document.execCommand("copy");
      var msg = successful ? "successful" : "unsuccessful";
      alert("Copied to clipboard!");
    } catch (err) {
      console.log("Oops, unable to copy");
    }
    document.body.removeChild(textArea);
  });
} catch (err) {}
