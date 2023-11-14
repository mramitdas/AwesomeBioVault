const body = document.querySelector("body");
const modal = document.querySelector(".modal");
const modalButton = document.querySelector(".nav-modal-trigger");
const closeButton = document.querySelector(".close-button");

const openModal = () => {
  modal.classList.add("is-open");
  body.style.overflow = "hidden";
};

const closeModal = () => {
  modal.classList.remove("is-open");
  body.style.overflow = "initial";
};

modalButton.addEventListener("click", openModal);
closeButton.addEventListener("click", closeModal);
