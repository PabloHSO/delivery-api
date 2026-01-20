from fastapi import APIRouter
from fastapi.responses import HTMLResponse

root_routes = APIRouter()

@root_routes.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <head>
            <title>🍔 Delivery System API</title>
            <!-- Google Fonts -->
            <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
            <!-- Font Awesome -->
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
            <!-- Particles.js CDN -->
            <script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>
            <style>
                /* ---------------- BODY ---------------- */
                body {
                    font-family: 'Roboto', sans-serif;
                    margin: 0;
                    padding: 0;
                    min-height: 100vh;
                    display: flex;
                    flex-direction: column;
                    background: linear-gradient(135deg, #ff6b6b, #f8f9fa);
                    background-size: 400% 400%;
                    animation: gradientMove 20s ease infinite;
                    color: #333;
                    position: relative;
                    overflow-x: hidden;
                }

                @keyframes gradientMove {
                    0% { background-position: 0% 50%; }
                    50% { background-position: 100% 50%; }
                    100% { background-position: 0% 50%; }
                }

                /* ---------------- PARTICLES ---------------- */
                #particles-js {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    z-index: -1;
                }

                /* ---------------- HEADER ---------------- */
                header {
                    text-align: center;
                    padding: 100px 20px 60px 20px;
                    color: #fff;
                }

                header h1 {
                    font-size: 4em;
                    margin-bottom: 20px;
                    text-shadow: 2px 2px 10px rgba(0,0,0,0.2);
                    animation: fadeInDown 1s ease forwards;
                }

                header p {
                    font-size: 1.5em;
                    margin-bottom: 40px;
                    text-shadow: 1px 1px 5px rgba(0,0,0,0.2);
                    animation: fadeInDown 1.2s ease forwards;
                }

                .docs-buttons a {
                    text-decoration: none;
                    color: #fff;
                    background-color: #007bff;
                    padding: 12px 25px;
                    border-radius: 8px;
                    margin: 0 10px;
                    font-weight: 500;
                    transition: all 0.3s ease;
                    box-shadow: 0 3px 6px rgba(0,0,0,0.2);
                    display: inline-block;
                    animation: fadeInUp 1.4s ease forwards;
                }

                .docs-buttons a:hover {
                    background-color: #0056b3;
                    transform: scale(1.05);
                    box-shadow: 0 6px 12px rgba(0,0,0,0.3);
                }

                .social-icons {
                    margin-top: 50px;
                    animation: fadeInUp 1.6s ease forwards;
                }

                .social-icons a {
                    display: inline-flex;
                    align-items: center;
                    background-color: #333;
                    color: #fff;
                    padding: 12px 22px;
                    border-radius: 12px;
                    margin: 0 8px;
                    font-size: 1.05em;
                    transition: all 0.3s ease;
                    box-shadow: 0 3px 6px rgba(0,0,0,0.15);
                }

                .social-icons a:hover {
                    background-color: #555;
                    transform: scale(1.05);
                }

                .social-icons i {
                    margin-right: 10px;
                    font-size: 1.3em;
                }

                /* ---------------- FEATURES ---------------- */
                .features {
                    flex: 1;
                    padding: 60px 20px;
                    max-width: 900px;
                    margin: 0 auto;
                    display: flex;
                    flex-direction: column;
                    gap: 25px;
                }

                .feature-item {
                    background-color: rgba(255,255,255,0.95);
                    padding: 25px 30px;
                    border-radius: 25px;
                    box-shadow: 0 10px 20px rgba(0,0,0,0.15);
                    font-size: 1.25em;
                    display: flex;
                    align-items: center;
                    gap: 15px;
                    opacity: 0;
                    transform: translateY(30px);
                    animation: fadeSlideIn 0.8s forwards;
                }

                .feature-item:nth-child(1) { animation-delay: 0.5s; }
                .feature-item:nth-child(2) { animation-delay: 0.8s; }
                .feature-item:nth-child(3) { animation-delay: 1.1s; }
                .feature-item:nth-child(4) { animation-delay: 1.4s; }
                .feature-item:nth-child(5) { animation-delay: 1.7s; }

                .feature-item i {
                    font-size: 1.6em;
                    color: #ff6b6b;
                }

                /* ---------------- FOOTER ---------------- */
                footer {
                    background-color: #343a40;
                    color: #fff;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 30px 40px;
                    flex-wrap: wrap;
                    animation: fadeInUp 2s ease forwards;
                }

                footer .footer-text {
                    font-size: 1em;
                }

                footer img {
                    width: 120px;
                    height: 120px;
                    border-radius: 50%;
                    border: 3px solid #ff6b6b;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
                }

                /* ---------------- ANIMATIONS ---------------- */
                @keyframes fadeInDown {
                    0% { opacity: 0; transform: translateY(-30px);}
                    100% { opacity: 1; transform: translateY(0);}
                }

                @keyframes fadeInUp {
                    0% { opacity: 0; transform: translateY(30px);}
                    100% { opacity: 1; transform: translateY(0);}
                }

                @keyframes fadeSlideIn {
                    0% { opacity: 0; transform: translateY(30px);}
                    100% { opacity: 1; transform: translateY(0);}
                }

                /* ---------------- RESPONSIVE ---------------- */
                @media(max-width: 700px) {
                    header h1 { font-size: 2.8em; }
                    header p { font-size: 1.2em; }
                    .docs-buttons a { display: block; margin: 10px 0; }
                    .social-icons { margin-top: 30px; }
                    .features { padding: 40px 15px; }
                    footer { flex-direction: column; text-align: center; }
                    footer img { margin-top: 15px; }
                }
            </style>
        </head>
        <body>
            <!-- Particles Background -->
            <div id="particles-js"></div>

            <header>
                <h1>🍔 Delivery System API</h1>
                <p>Bem-vindo(a) à API de delivery!</p>
                <div class="docs-buttons">
                    <a href="/docs">📄 Swagger UI</a>
                    <a href="/redoc">📘 Redoc</a>
                </div>
                <div class="social-icons">
                    <a href="https://www.linkedin.com/in/pablohsilveira" target="_blank">
                        <i class="fab fa-linkedin"></i> LinkedIn
                    </a>
                    <a href="https://github.com/seu-usuario/delivery-api" target="_blank">
                        <i class="fab fa-github"></i> GitHub
                    </a>
                </div>
            </header>

            <section class="features">
                <div class="feature-item"><i class="fas fa-user-check"></i> Cadastro e autenticação de usuários (admin e comum)</div>
                <div class="feature-item"><i class="fas fa-receipt"></i> Criação, atualização e cancelamento de pedidos</div>
                <div class="feature-item"><i class="fas fa-plus-square"></i> Adição e remoção de itens do pedido</div>
                <div class="feature-item"><i class="fas fa-lock"></i> Endpoints protegidos por JWT e documentação via Swagger/OpenAPI</div>
                <div class="feature-item"><i class="fas fa-vial"></i> Testes unitários com Pytest e cobertura completa</div>
            </section>

            <footer>
                <div class="footer-text">
                    Desenvolvido por Pablo Henrique Silveira &copy; 2026
                </div>
                <img src="/static/images/eu6.jpg" alt="Minha foto">
            </footer>

            <!-- ---------------- PARTICLES.JS CONFIG ---------------- -->
            <script>
                particlesJS("particles-js", {
                    "particles": {
                        "number": { "value": 80, "density": { "enable": true, "value_area": 800 } },
                        "color": { "value": "#ffffff" },
                        "shape": { "type": "circle" },
                        "opacity": { "value": 0.5, "random": true },
                        "size": { "value": 3, "random": true },
                        "line_linked": { "enable": true, "distance": 150, "color": "#ffffff", "opacity": 0.2, "width": 1 },
                        "move": { "enable": true, "speed": 2, "direction": "none", "random": true, "straight": false, "out_mode": "out" }
                    },
                    "interactivity": {
                        "detect_on": "canvas",
                        "events": {
                            "onhover": { "enable": true, "mode": "repulse" },
                            "onclick": { "enable": true, "mode": "push" }
                        },
                        "modes": {
                            "repulse": { "distance": 100 },
                            "push": { "particles_nb": 4 }
                        }
                    },
                    "retina_detect": true
                });
            </script>
        </body>
    </html>
    """
