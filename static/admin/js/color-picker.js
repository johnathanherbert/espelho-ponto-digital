document.addEventListener("DOMContentLoaded", function () {
  const colorInputs = document.querySelectorAll('input[type="color"]');

  colorInputs.forEach((input) => {
    const hexInput = input.parentElement.querySelector(".color-picker-hex");

    // Atualiza o input hex quando o color picker muda
    input.addEventListener("input", (e) => {
      hexInput.value = e.target.value.toUpperCase();
    });

    // Atualiza o color picker quando o input hex muda
    hexInput.addEventListener("input", (e) => {
      const value = e.target.value;
      if (/^#[0-9A-F]{6}$/i.test(value)) {
        input.value = value;
      }
    });

    // Formata o valor inicial
    if (input.value) {
      hexInput.value = input.value.toUpperCase();
    }
  });
});
