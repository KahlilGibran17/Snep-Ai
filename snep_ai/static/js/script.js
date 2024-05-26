const body = document.querySelector("body");
const sidebar = body.querySelector(".sidebar");
const toggle = body.querySelector(".toggle");
const newscan = body.querySelector(".newscan-btn");

toggle.addEventListener("click", () => {
  sidebar.classList.toggle("close");
});


