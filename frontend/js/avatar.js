// Seleccionar el avatar
const avatar = document.getElementById("avatar");

// Obtener la URL desde el atributo data-url del avatar
const redirectUrl = avatar.dataset.url;

// Crear una instancia de animación de GSAP (puedes pausar o reanudar según sea necesario)
const hoverAnimation = gsap.timeline({ paused: true });
hoverAnimation
    .to(avatar, {
        scale: 10, // Agrandar el avatar
        opacity: 0, // Desvanecer el avatar
        duration: 2.0, // Tiempo para completar la animación
        ease: "power2.inOut", // Suavidad
    })
    .call(() => {
        // Redirigir solo si el cursor sigue sobre el avatar
        if (isHovering) {
            window.location.href = redirectUrl;
        }
    });

// Efecto de flotación continua
gsap.to(avatar, {
    y: -10, // Mover hacia arriba
    repeat: -1, // Repetir infinitamente
    yoyo: true, // Volver a la posición original
    duration: 2, // Tiempo de la animación
    ease: "power1.inOut", // Suavidad
});

// Variable para controlar el estado del cursor sobre el avatar
let isHovering = false;

// Manejar el evento `mouseenter`
avatar.addEventListener("mouseenter", () => {
    isHovering = true; // El cursor está sobre el avatar
    hoverAnimation.restart(); // Reiniciar la animación de hover
});

// Manejar el evento `mouseleave`
avatar.addEventListener("mouseleave", () => {
    isHovering = false; // El cursor ha salido del avatar
    hoverAnimation.pause(); // Pausar la animación actual
    gsap.to(avatar, {
        scale: 1, // Restaurar tamaño original
        opacity: 1, // Restaurar visibilidad
        duration: 1, // Tiempo de restauración
        ease: "power2.inOut", // Suavidad
    });
});
