const carousels = document.querySelectorAll('.carousel');

carousels.forEach((carousel) => {
  const carouselInner = carousel.querySelector('.carousel-inner');
  const carouselRow = carouselInner.querySelector('.carousel-row');
  const carouselItems = carouselRow.querySelectorAll('.carousel-item');
  const prevBtn = carousel.querySelector('.prev');
  const nextBtn = carousel.querySelector('.next');

  let currentItem = 0;
  const carouselWidth = carousel.offsetWidth;
  const itemWidth = carouselWidth / 3;
  const maxItems = Math.floor(carouselRow.offsetWidth / itemWidth);

  function showItem(index) {
    carouselInner.style.transform = `translateX(-${index * itemWidth}px)`;
  }

  prevBtn.addEventListener('click', (event) => {
    event.preventDefault();
    if (currentItem > 0) {
      currentItem--;
      showItem(currentItem);
    }
  });

  nextBtn.addEventListener('click', (event) => {
    event.preventDefault();
    if (currentItem < carouselItems.length - maxItems) {
      currentItem++;
      showItem(currentItem);
    }
  });

  showItem(currentItem);
});