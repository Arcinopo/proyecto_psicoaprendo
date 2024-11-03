document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.alfanumerico-btn');
    const audioCache = {};

    buttons.forEach(button => {
        const char = button.getAttribute('data-char').toLowerCase();
        const audioPath = `/static/sounds/${char}.mp3`;
        console.log(`Cargando audio para: ${audioPath}`); // Mensaje de depuración

        audioCache[char] = new Audio(audioPath);

        button.addEventListener('click', function() {
            console.log(`Intentando reproducir sonido para: ${char}`);
            this.classList.add('playing');

            const audio = audioCache[char];
            if (audio) {
                audio.currentTime = 0; // Reinicia el audio
                audio.play()
                    .then(() => {
                        setTimeout(() => this.classList.remove('playing'), 500);
                    })
                    .catch(error => {
                        console.error(`No se pudo reproducir el audio para "${char}":`, error);
                        alert(`Audio para "${char}" no disponible.`);
                        this.classList.remove('playing');
                    });
            } else {
                console.error(`Archivo de audio para "${char}" no encontrado.`);
            }
        });
    });
});
