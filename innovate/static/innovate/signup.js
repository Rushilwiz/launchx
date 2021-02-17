var modal = document.getElementById("payment-modal")
var openBtn = document.getElementById("payment-modal-open")
var closeBtn = document.getElementById("payment-modal-close")

openBtn.onclick = () => {
  modal.style.display = "block"
}

closeBtn.onclick = () => {
  modal.style.display = "none"
}

window.onclick = (e) => {
  if (e.target == modal) {
    modal.style.display = "none"
  }
}