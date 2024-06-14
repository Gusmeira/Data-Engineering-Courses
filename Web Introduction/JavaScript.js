const link = document.getElementsByTagName("a")[0]
const btn = document.getElementById("btn")


const toggleLink = () => {
  if (link.style.display === "none") {
    link.style.display = "inline";
    btn.textContent = "Hide Link";
  } else {
    link.style.display = "none";
    btn.textContent = "Show Link";
  }
}

btn.addEventListener("click", toggleLink)