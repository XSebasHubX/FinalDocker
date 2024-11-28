// Initialize Swiper for the header slider
const swiper1 = new Swiper(".mySwiper-1", {
    loop: true,
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    autoplay: {
        delay: 5000,
        disableOnInteraction: false,
    },
});

// Initialize Swiper for the product tabs
const swiper2 = new Swiper(".mySwiper-2", {
    slidesPerView: 3,
    spaceBetween: 20,
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    breakpoints: {
        320: {
            slidesPerView: 1,
        },
        768: {
            slidesPerView: 2,
        },
        1024: {
            slidesPerView: 3,
        },
    },
});

// Tab switching functionality
const tabs = document.querySelectorAll('input[name="tabs"]');
tabs.forEach(tab => {
    tab.addEventListener('change', () => {
        const activeTab = document.querySelector('.tabInput:checked').value;
        const swipers = document.querySelectorAll('.mySwiper-2');
        swipers.forEach((swiper, index) => {
            swiper.style.display = index + 1 === parseInt(activeTab) ? "block" : "none";
        });
    });
});
