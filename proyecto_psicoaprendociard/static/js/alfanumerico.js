document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.alfanumerico-btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const char = this.getAttribute('data-char');
            const audio = new Audio(`/static/sounds/${char}.mp3`);
            audio.play();
        });
    });
});
