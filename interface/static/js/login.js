document.addEventListener("DOMContentLoaded", () => {
  const formLogin = document.getElementById("formLogin");
  const usuarioInput = document.getElementById("usuario");
  const passwordInput = document.getElementById("password");
  const statusBox = document.getElementById("status");
  const togglePassword = document.getElementById("togglePassword");

  if (!formLogin) {
    console.error("No se encontró el formulario con id='formLogin'");
    return;
  }

  // Mostrar / ocultar contraseña
  if (togglePassword && passwordInput) {
    togglePassword.addEventListener("click", () => {
      const esPassword = passwordInput.type === "password";

      passwordInput.type = esPassword ? "text" : "password";
      togglePassword.textContent = esPassword ? "🙈" : "👁";
    });
  }

  formLogin.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = usuarioInput.value.trim();
    const password = passwordInput.value.trim();

    if (!email || !password) {
      mostrarEstado("Ingrese correo y contraseña.", "error");
      return;
    }

    mostrarEstado("Validando credenciales...", "info");

    try {
      const response = await fetch("/api/v1/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          email: email,
          password: password
        })
      });

      const data = await response.json();

      if (!response.ok || !data.ok) {
        mostrarEstado(
          data.message || "Correo o contraseña incorrectos.",
          "error"
        );
        return;
      }

      mostrarEstado("Inicio de sesión correcto. Redirigiendo...", "success");

      setTimeout(() => {
        window.location.href = "/home";
      }, 700);

    } catch (error) {
      console.error("Error en login:", error);
      mostrarEstado("Error de conexión con el servidor.", "error");
    }
  });

  function mostrarEstado(mensaje, tipo) {
    statusBox.textContent = mensaje;

    statusBox.classList.remove(
      "success",
      "error",
      "info"
    );

    statusBox.classList.add(tipo);
  }
});