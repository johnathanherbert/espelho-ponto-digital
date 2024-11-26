document.addEventListener("DOMContentLoaded", function () {
  // Validação do campo de ID
  const idInput = document.getElementById("id_colaborador");
  if (idInput) {
    idInput.addEventListener("input", function (e) {
      // Remove caracteres não numéricos
      this.value = this.value.replace(/[^0-9]/g, "");
    });
  }

  // Fechar modal de erro
  const closeButtons = document.querySelectorAll("[data-close-modal]");
  closeButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const modal = this.closest(".modal");
      if (modal) {
        modal.style.display = "none";
      }
    });
  });
});
