// Little Pink Llama — site interactions (no dependencies)
(function () {
  // Mobile nav toggle
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.querySelector('.nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      nav.classList.toggle('open');
    });
  }

  // Hero slideshow
  var slides = document.querySelectorAll('.hero .slide');
  if (slides.length > 1) {
    var dotsWrap = document.querySelector('.hero-dots');
    var current = 0;
    var timer;
    function show(i) {
      slides[current].classList.remove('active');
      dotsWrap.children[current].classList.remove('active');
      current = (i + slides.length) % slides.length;
      slides[current].classList.add('active');
      dotsWrap.children[current].classList.add('active');
    }
    slides.forEach(function (_, i) {
      var b = document.createElement('button');
      b.setAttribute('aria-label', 'Slide ' + (i + 1));
      if (i === 0) b.classList.add('active');
      b.addEventListener('click', function () {
        show(i);
        restart();
      });
      dotsWrap.appendChild(b);
    });
    function restart() {
      clearInterval(timer);
      timer = setInterval(function () { show(current + 1); }, 5000);
    }
    restart();
  }

  // Product gallery thumbnails
  var mainImg = document.querySelector('.gallery-main img');
  var thumbs = document.querySelectorAll('.gallery-thumbs img');
  thumbs.forEach(function (t) {
    t.addEventListener('click', function () {
      mainImg.src = t.dataset.full || t.src;
      thumbs.forEach(function (x) { x.classList.remove('active'); });
      t.classList.add('active');
    });
  });

  // Contact form → WhatsApp (no backend)
  var form = document.querySelector('.contact-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = (form.querySelector('[name=name]') || {}).value || '';
      var email = (form.querySelector('[name=email]') || {}).value || '';
      var phone = (form.querySelector('[name=phone]') || {}).value || '';
      var comment = (form.querySelector('[name=comment]') || {}).value || '';
      var msg = 'Hi Little Pink Llama!\nName: ' + name + '\nEmail: ' + email +
        (phone ? '\nPhone: ' + phone : '') + '\nMessage: ' + comment;
      window.open('https://wa.me/919460074404?text=' + encodeURIComponent(msg), '_blank', 'noopener');
    });
  }

  // Newsletter form → WhatsApp
  var news = document.querySelector('.newsletter form');
  if (news) {
    news.addEventListener('submit', function (e) {
      e.preventDefault();
      var em = news.querySelector('input[type=email]').value;
      var msg = 'Hi! Please add me to the Little Pink Llama updates list. Email: ' + em;
      window.open('https://wa.me/919460074404?text=' + encodeURIComponent(msg), '_blank', 'noopener');
    });
  }
})();
