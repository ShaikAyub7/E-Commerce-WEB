// function toggleMode() {
//     // Check if body has 'dark-mode' class
//     if (document.body.classList.contains('dark-mode')) {
//         // Remove 'dark-mode' class from body
//         document.body.classList.remove('dark-mode');
//         // Update button text to 'Dark Mode' and icon to 'moon'
//         document.getElementById('modeToggle').innerHTML = '<i class="fas fa-moon"></i> Dark Mode';
//     } else {
//         // Add 'dark-mode' class to body
//         document.body.classList.add('dark-mode');
//         // Update button text to 'Light Mode' and icon to 'sun'
//         document.getElementById('modeToggle').innerHTML = '<i class="fas fa-sun"></i> Light Mode';
//     }
// }

// const carousel = document.querySelector('#carouselExampleCaptions');
// const carouselInstance = new mdb.Carousel(carousel);
 // Initialize Bootstrap Carousel
const carousel = document.querySelector('#carouselExampleCaptions');
  const carouselInstance = new mdb.Carousel(carousel, {
    ride: true, // Autoplay the carousel
    interval: 5000, // Delay between slides in milliseconds
    pause: 'hover', // Pause the carousel on mouse hover
    wrap: true // Wrap around the carousel when reaching the last slide
  });