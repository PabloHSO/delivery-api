/* ============================
   PREMIUM ANIMATIONS ENGINE
   ============================ */

document.addEventListener("DOMContentLoaded", () => {

  /* ----------------------------
     SCROLL REVEAL
  ----------------------------- */
  const revealElements = document.querySelectorAll(
    ".hero, .top-banner img, .feature-card, .architecture, footer"
  );

  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("reveal-visible");
          revealObserver.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.15
    }
  );

  revealElements.forEach(el => {
    el.classList.add("reveal");
    revealObserver.observe(el);
  });


  /* ----------------------------
     STAGGER EFFECT (FEATURES)
  ----------------------------- */
  const featureCards = document.querySelectorAll(".feature-card");

  featureCards.forEach((card, index) => {
    card.style.transitionDelay = `${index * 90}ms`;
  });


  /* ----------------------------
     MICRO INTERACTION - BUTTONS
  ----------------------------- */
  const buttons = document.querySelectorAll(".cta-buttons a");

  buttons.forEach(btn => {
    btn.addEventListener("mouseenter", () => {
      btn.style.transform = "translateY(-4px) scale(1.02)";
    });

    btn.addEventListener("mouseleave", () => {
      btn.style.transform = "translateY(0) scale(1)";
    });
  });


  /* ----------------------------
     TECH ICON FLOAT EFFECT
  ----------------------------- */
  const techIcons = document.querySelectorAll(".tech-icons i");

  techIcons.forEach((icon, index) => {
    icon.style.animation = `float ${4 + index * 0.4}s ease-in-out infinite`;
  });

});
