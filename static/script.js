window.onload = function () {

    const canvas = document.getElementById("bg");
    const ctx = canvas.getContext("2d");

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    let blobs = [];

    class Blob {
        constructor() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.radius = Math.random() * 120 + 80;
            this.speedX = (Math.random() - 0.5) * 0.3;
            this.speedY = (Math.random() - 0.5) * 0.3;
        }

        update() {
            this.x += this.speedX;
            this.y += this.speedY;

            if (this.x < -this.radius) this.x = canvas.width + this.radius;
            if (this.x > canvas.width + this.radius) this.x = -this.radius;

            if (this.y < -this.radius) this.y = canvas.height + this.radius;
            if (this.y > canvas.height + this.radius) this.y = -this.radius;
        }

        draw() {
            const gradient = ctx.createRadialGradient(
                this.x, this.y, this.radius * 0.1,
                this.x, this.y, this.radius
            );

            gradient.addColorStop(0, "rgba(0, 150, 255, 0.15)");
            gradient.addColorStop(1, "rgba(0, 150, 255, 0)");

            ctx.fillStyle = gradient;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    function init() {
        blobs = [];
        for (let i = 0; i < 6; i++) {
            blobs.push(new Blob());
        }
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        blobs.forEach(blob => {
            blob.update();
            blob.draw();
        });
        requestAnimationFrame(animate);
    }

    init();
    animate();
function openModal() {
    document.getElementById("infoModal").style.display = "block";
}

function closeModal() {
    document.getElementById("infoModal").style.display = "none";
}

window.onclick = function(event) {
    const modal = document.getElementById("infoModal");
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
    // Smooth Counter Animation
    document.querySelectorAll(".counter").forEach(counter => {
        const target = +counter.dataset.target;
        let count = 0;
        const increment = target / 80;

        function updateCounter() {
            if (count < target) {
                count += increment;
                counter.innerText = Math.floor(count);
                requestAnimationFrame(updateCounter);
            } else {
                counter.innerText = target;
            }
        }
        updateCounter();
    });

};
