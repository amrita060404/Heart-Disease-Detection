document.addEventListener('DOMContentLoaded', function() {
    // Navigation toggle for mobile
    const navContainer = document.querySelector('.nav-container');
    const mobileMenu = document.createElement('div');
    mobileMenu.className = 'mobile-menu';
    mobileMenu.innerHTML = `
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="#about">About Heart Disease</a></li>
            <li><a href="#how-it-works">How It Works</a></li>
            <li><a href="/assessment" class="nav-button">Take the Test</a></li>
        </ul>
    `;
    navContainer.insertAdjacentElement('afterend', mobileMenu)
    
    hamburger.addEventListener('click', function() {
        mobileMenu.classList.toggle('active');
    });

    // Close mobile menu when clicking a link
    mobileMenu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            mobileMenu.classList.remove('active');
        });
    });

    // Create and initialize infinite carousel
    const carousel = document.querySelector('.risk-cards');
    const cardData = [
        {
            level: 0,
            title: "No Heart Disease",
            desc: "No presence of heart disease detected"
        },
        {
            level: 1,
            title: "Mild Risk",
            desc: "Early signs or mild risk factors present"
        },
        {
            level: 2,
            title: "Moderate Risk",
            desc: "Noticeable risk factors requiring attention"
        },
        {
            level: 3,
            title: "Serious Risk",
            desc: "Significant risk factors present"
        },
        {
            level: 4,
            title: "Severe Risk",
            desc: "Immediate medical attention recommended"
        }
    ];

    // Create multiple copies of cards for infinite effect
    for (let i = 0; i < 3; i++) {
        cardData.forEach(card => {
            const cardElement = document.createElement('div');
            cardElement.className = 'risk-card';
            cardElement.innerHTML = `
                <div class="risk-level level-${card.level}">${card.level}</div>
                <h3>${card.title}</h3>
                <p>${card.desc}</p>
            `;
            carousel.appendChild(cardElement);
        });
    }

    const prevButton = document.querySelector('.carousel-button.prev');
    const nextButton = document.querySelector('.carousel-button.next');
    const cardWidth = document.querySelector('.risk-card').offsetWidth + 30;
    let currentPosition = 0;
    const cardCount = cardData.length * 3;
    const middleSet = cardData.length; // Middle set of cards

    // Start in the middle of the duplicated cards
    currentPosition = -(middleSet * cardWidth);
    carousel.style.transform = `translateX(${currentPosition}px)`;

    function updateCarousel() {
        // If we've scrolled past the first set, jump to the middle
        if (currentPosition >= 0) {
            currentPosition = -(middleSet * cardWidth);
            carousel.style.transition = 'none';
            carousel.style.transform = `translateX(${currentPosition}px)`;
            // Force reflow
            carousel.offsetHeight;
            carousel.style.transition = 'transform 0.5s ease';
        }
        // If we've scrolled past the last set, jump to the middle
        else if (currentPosition <= -((cardCount - middleSet) * cardWidth)) {
            currentPosition = -(middleSet * cardWidth);
            carousel.style.transition = 'none';
            carousel.style.transform = `translateX(${currentPosition}px)`;
            // Force reflow
            carousel.offsetHeight;
            carousel.style.transition = 'transform 0.5s ease';
        }
    }

    prevButton.addEventListener('click', () => {
        currentPosition += cardWidth;
        carousel.style.transform = `translateX(${currentPosition}px)`;
        updateCarousel();
    });

    nextButton.addEventListener('click', () => {
        currentPosition -= cardWidth;
        carousel.style.transform = `translateX(${currentPosition}px)`;
        updateCarousel();
    });

    // Scrolling effects for heart
    const heart = document.querySelector('.biological-heart');
    const heartPlatform = document.querySelector('.heart-platform');
    const heroSection = document.querySelector('.hero');
    const navbar = document.querySelector('.navbar');

    window.addEventListener('scroll', function() {
        const scrollPosition = window.scrollY;
        const heroHeight = heroSection.offsetHeight;

        if (scrollPosition > heroHeight * 0.5) {
            document.body.classList.add('scrolled');
            navbar.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
        } else {
            document.body.classList.remove('scrolled');
            navbar.style.boxShadow = 'none';
        }

        // Parallax effect for heart in hero section
        if (!document.body.classList.contains('scrolled')) {
            const parallaxValue = scrollPosition * 0.3;
            heart.style.transform = `translateY(${parallaxValue}px) rotate(${scrollPosition * 0.2}deg)`;
        }
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Make heart interactive
    heart.addEventListener('mouseenter', function() {
        this.style.animationPlayState = 'paused';
    });
    
    heart.addEventListener('mouseleave', function() {
        this.style.animationPlayState = 'running';
    });
    
    heart.addEventListener('click', function() {
        this.style.transform = 'scale(1.2)';
        setTimeout(() => {
            this.style.transform = 'scale(1)';
        }, 300);
    });
});