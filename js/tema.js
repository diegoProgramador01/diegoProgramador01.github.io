document.addEventListener("DOMContentLoaded", function () {
    const themeIcon = document.getElementById("theme-icon");
    const html = document.documentElement;

    // Función para actualizar el icono según el tema
    function updateIcon() {
        if (html.classList.contains("dark-theme")) {
            themeIcon.classList.replace("fa-sun", "fa-moon");
        } else {
            themeIcon.classList.replace("fa-moon", "fa-sun"); 
        }
    }

    // Verificar si hay un tema guardado en localStorage
    if (localStorage.getItem("theme") === "dark") {
        html.classList.add("dark-theme");
    }

    // Actualizar el icono según el estado inicial
    updateIcon();

    // Evento para cambiar el tema
    themeIcon.addEventListener("click", function () {
        html.classList.toggle("dark-theme");

        // Guardar el estado en localStorage
        if (html.classList.contains("dark-theme")) {
            localStorage.setItem("theme", "dark");
        } else {
            localStorage.setItem("theme", "light");
        }

        // Actualizar el icono después del cambio
        updateIcon();
    });
});
