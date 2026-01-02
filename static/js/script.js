////////////////////////// Error handling /////////////////////////////////

document.addEventListener("DOMContentLoaded", () => {
  const heading = document.querySelector(".error-handling");

  if (heading && heading.classList.contains("show-error")) {
    setTimeout(() => {
      heading.classList.remove("show-error");
    }, 3000);
  }
});

////////////////////////// Mobile navigation /////////////////////////////////

const btnNavEl = document.querySelector(".btn-mobile-nav");
const navHeaderEl = document.querySelector(".dashboard-nav-m");

if (btnNavEl && navHeaderEl) {
  btnNavEl.addEventListener("click", function () {
    navHeaderEl.classList.toggle("nav-open");
  });
}
