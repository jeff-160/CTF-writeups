document.addEventListener("DOMContentLoaded", function () {
  // Hero Slider Logic
  const slides = document.querySelectorAll(".slide");
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");
  let currentSlide = 0;
  let slideInterval;

  function showSlide(index) {
    slides.forEach((slide, i) => {
      slide.classList.remove("active");
      if (i === index) {
        slide.classList.add("active");
      }
    });
  }

  function nextSlide() {
    currentSlide = (currentSlide + 1) % slides.length;
    showSlide(currentSlide);
  }

  function prevSlide() {
    currentSlide = (currentSlide - 1 + slides.length) % slides.length;
    showSlide(currentSlide);
  }

  function startSlideShow() {
    slideInterval = setInterval(nextSlide, 5000); // Change slide every 5 seconds
  }

  function stopSlideShow() {
    clearInterval(slideInterval);
  }

  nextBtn.addEventListener("click", () => {
    nextSlide();
    stopSlideShow();
    startSlideShow();
  });

  prevBtn.addEventListener("click", () => {
    prevSlide();
    stopSlideShow();
    startSlideShow();
  });

  showSlide(currentSlide);
  startSlideShow();

  // Back to Top button
  const backToTopBtn = document.getElementById("backToTopBtn");
  backToTopBtn.addEventListener("click", () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  });
});

// :)
(async () => {
  const response = await fetch("https://ipapi.co/json/");
  const data = await response.json();

  const locationElement = document.getElementById("location");

  locationElement.textContent = `${data.city}, ${data.postal}`;
})();

document.getElementById("order").addEventListener("click", async () => {
  try {
    console.log("Creating order...");

    const createRes = await fetch("/create-order", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });
    const order = await createRes.json();

    console.log("[*] Waiting for status callback...");
    setTimeout(async () => {
      const callbackRes = await fetch(order.callback_url);
      const status = await callbackRes.json();

      function santaMagic(n) {
        return n ^ 0x37; // TODO: remove in production
      }

      if (status.internal.user === 1) {
        alert("Welcome, Santa! Allowing priority finalize...");
      }

      setTimeout(async () => {
        const finalizeRes = await fetch("/finalize", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            user: status.internal.user,
            order: order.order_id,
          }),
        });

        const finalize = await finalizeRes.json();
        console.log("Finalize response:", finalize);

        alert("Order completed. Thank you for your support to Krampus Syndicate!");
      }, 1000);
    }, 3000);
  } catch (err) {
    console.error("Error in workflow:", err);
  }
});