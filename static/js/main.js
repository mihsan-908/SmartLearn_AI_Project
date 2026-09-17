document.addEventListener("DOMContentLoaded", () => {
    const reveals = document.querySelectorAll(".reveal");

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
            }
        });
    }, { threshold: 0.12 });

    reveals.forEach((el) => revealObserver.observe(el));

    const anchors = document.querySelectorAll('a[href^="#"]');
    anchors.forEach((anchor) => {
        anchor.addEventListener("click", (e) => {
            const targetId = anchor.getAttribute("href");
            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: "smooth", block: "start" });
            }
        });
    });
});

    window.addEventListener('load', () => {
        const loader = document.getElementById('globalLoader');
        if (loader) {
            loader.style.opacity = '0';
            loader.style.transition = 'opacity 0.45s ease';
            setTimeout(() => loader.style.display = 'none', 480);
        }
    });

    const hamburger = document.getElementById('navHamburger');
    const drawer = document.getElementById('navDrawer');

    if (hamburger && drawer) {
        hamburger.addEventListener('click', () => {
            const isOpen = drawer.classList.toggle('open');
            hamburger.classList.toggle('open', isOpen);
            hamburger.setAttribute('aria-expanded', isOpen);
            drawer.setAttribute('aria-hidden', !isOpen);
        });

        drawer.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                drawer.classList.remove('open');
                hamburger.classList.remove('open');
                hamburger.setAttribute('aria-expanded', false);
                drawer.setAttribute('aria-hidden', true);
            });
        });

        document.addEventListener('click', (e) => {
            if (!hamburger.contains(e.target) && !drawer.contains(e.target)) {
                drawer.classList.remove('open');
                hamburger.classList.remove('open');
                hamburger.setAttribute('aria-expanded', false);
            }
        });
    }

    document.querySelectorAll('.flash-close').forEach(btn => {
        btn.addEventListener('click', () => {
            const flash = btn.closest('.flash');
            flash.style.opacity = '0';
            flash.style.transform = 'translateX(16px)';
            flash.style.transition = 'all 0.30s ease';
            setTimeout(() => flash.remove(), 320);
        });
    });

    setTimeout(() => {
        document.querySelectorAll('.flash').forEach(flash => {
            flash.style.opacity = '0';
            flash.style.transform = 'translateX(16px)';
            flash.style.transition = 'all 0.30s ease';
            setTimeout(() => flash.remove(), 320);
        });
    }, 5000);
