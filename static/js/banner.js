// Swiper banner
new Swiper('.swiper-container', {
    loop: true,
    slidesPerView: 1,
    autoplay: {
        delay: 6000,
        disableOnInteraction: false
    },
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
    effect: 'slide',
});

// Mostrar modal de login
document.addEventListener('DOMContentLoaded', function() {
    var btn = document.getElementById('btn-ingresar');
    var modal = document.getElementById('login-modal');
    var closeBtn = document.getElementById('close-login-modal');
    if(btn && modal && closeBtn) {
        btn.onclick = function() { modal.style.display = 'block'; }
        closeBtn.onclick = function() { modal.style.display = 'none'; }
        window.onclick = function(event) {
            if(event.target == modal) { modal.style.display = 'none'; }
        }
    }
});
