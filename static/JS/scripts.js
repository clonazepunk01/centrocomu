let currentIndex = 0;

function moveSlide(direction) {
    const slides = document.querySelector('.slides');
    const totalSlides = document.querySelectorAll('.slide').length;

    currentIndex += direction;

    if (currentIndex < 0) {
        currentIndex = totalSlides - 1;
    } else if (currentIndex >= totalSlides) {
        currentIndex = 0;
    }

    const offset = -currentIndex * 100;
    slides.style.transform = `translateX(${offset}%)`;
}

setInterval(() => {
    moveSlide(1);
}, 3000);


document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'es'
    });

    calendar.render();
});



// Inicializar el mapa con una ubicación específica
function initMap() {
// Coordenadas de la ubicación (por ejemplo, Ciudad de México)
var location = { lat: -38.7385465724806,  lng: -72.94529748770817};  // Cambia las coordenadas aquí

// Crear el mapa y centrarlo en la ubicación
var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 15,  // Nivel de zoom ajustado
    center: location
});

// Crear un marcador en la ubicación específica
var marker = new google.maps.Marker({
    position: location,
    map: map,
    title: 'Ciudad de México'  // Cambia el título si es necesario
});
}