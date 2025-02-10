// Configuración del Canvas
const canvas = document.getElementById("backgroundCanvas");
const ctx = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const particles = [];
const mouse = {
    x: null,
    y: null,
    radius: 150, // Radio de interacción del mouse
};

// Evento de seguimiento del mouse
window.addEventListener("mousemove", (event) => {
    mouse.x = event.x;
    mouse.y = event.y;
});

// Evento para ajustar el canvas al cambiar el tamaño de la ventana
window.addEventListener("resize", () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    init(); // Recalcular las partículas
});

// Obtener color de la particula de CSS
function getParticulaColor() { 
    return getComputedStyle(document.documentElement).getPropertyValue('--particulas-color');
}

// Obtener color de la linea de la particula de CSS
function getParticulaLineaColor() {
    let color = getComputedStyle(document.documentElement).getPropertyValue('--particulas-linea-color').trim();
    let rgbValues = color.match(/\d+, \d+, \d+/); // Buscar los valores "r, g, b"
    return rgbValues ? rgbValues[0] : "199, 206, 219"; // Color por defecto
}

// Función para actualizar colores y redibujar partículas al cambiar el tema
function actualizarColoresParticulas() {
    const nuevoColorParticula = getParticleColor();
    const nuevoColorLinea = getParticulaLineaColor();

    // Actualizar el color de las partículas existentes
    particles.forEach(particle => {
        particle.color = nuevoColorParticula;
    });

    // Limpiar y redibujar el canvas con los nuevos colores
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawParticles(); // Redibujar partículas
    connectParticles(); // Redibujar conexiones
}

// Observar cambios en el tema y actualizar las partículas
const observer = new MutationObserver(() => {
    actualizarColoresParticulas();
});

// Iniciar el observador sobre el `body` para detectar cambios de clase
observer.observe(document.body, { attributes: true, attributeFilter: ['class'] });

// Clase para las partículas
class Particle {
    constructor(x, y, size, color, speedX, speedY) {
        this.x = x;
        this.y = y;
        this.size = size;
        this.speedX = speedX;
        this.speedY = speedY;
    }

    // Dibujar partícula
    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fillStyle = getParticulaColor();
        ctx.fill();
        ctx.closePath();
    }

    // Actualizar posición
    update() {
        this.x += this.speedX;
        this.y += this.speedY;

        // Rebote en los bordes
        if (this.x < 0 || this.x > canvas.width) this.speedX *= -1;
        if (this.y < 0 || this.y > canvas.height) this.speedY *= -1;

        // Interacción con el ratón
        const dx = this.x - mouse.x;
        const dy = this.y - mouse.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        if (distance < mouse.radius) {
            const angle = Math.atan2(dy, dx);
            const force = (mouse.radius - distance) / mouse.radius;
            const forceX = Math.cos(angle) * force * 10;
            const forceY = Math.sin(angle) * force * 10;
            this.x += forceX;
            this.y += forceY;
        }

        this.draw();
    }
}

// Crear partículas
function init() {
    particles.length = 0; // Vaciar el array
    const numberOfParticles = window.innerWidth < 768 ? 40 : 150;
    for (let i = 0; i < numberOfParticles; i++) {
        const size = Math.random() * 4 + 1; // Tamaño aleatorio
        const x = Math.random() * canvas.width;
        const y = Math.random() * canvas.height;
        const color = `rgba(255, 255, 255, ${Math.random()})`; // Transparencia aleatoria
        const speedX = (Math.random() - 0.5) * 2;
        const speedY = (Math.random() - 0.5) * 2;

        particles.push(new Particle(x, y, size, color, speedX, speedY));
    }
}



// Conectar partículas cercanas
function connectParticles() {
    const particulaColor = getParticulaLineaColor(); // Obtener solo "r, g, b"
    
    for (let i = 0; i < particles.length; i++) {
        for (let j = i; j < particles.length; j++) {
            const dx = particles[i].x - particles[j].x;
            const dy = particles[i].y - particles[j].y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < 120) {
                const opacity = (1 - distance / 120).toFixed(2);
                ctx.strokeStyle = `rgba(${particulaColor}, ${opacity})`;
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(particles[i].x, particles[i].y);
                ctx.lineTo(particles[j].x, particles[j].y);
                ctx.stroke();
            }
        }
    }
}


// Animación
function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach((particle) => particle.update());
    connectParticles();
    requestAnimationFrame(animate);
}

// Inicializar
init();
animate();