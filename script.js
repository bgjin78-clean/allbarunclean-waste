document.addEventListener("DOMContentLoaded", function () {
    createGallery("beforeGallery", "before", 8, "폐기물처리 작업 전 현장");
    createGallery("processGallery", "process", 8, "폐기물처리 작업 중 현장");
    createGallery("afterGallery", "after", 8, "폐기물처리 작업 후 현장");

    createLightbox();
});

function createGallery(containerId, prefix, count, altText) {
    const container = document.getElementById(containerId);
    if (!container) return;

    for (let i = 1; i <= count; i++) {
        const number = String(i).padStart(2, "0");
        const img = document.createElement("img");

        img.src = `./images/${prefix}-${number}.jpg`;
        img.alt = `${altText} ${i}`;
        img.loading = "lazy";
        img.className = "gallery-img";

        img.onerror = function () {
            if (img.src.endsWith(".jpg")) {
                img.src = `./images/${prefix}-${number}.jpeg`;
            }
        };

        img.addEventListener("click", function () {
            openLightbox(img.src, img.alt);
        });

        container.appendChild(img);
    }
}

function createLightbox() {
    const lightbox = document.createElement("div");
    lightbox.className = "lightbox";
    lightbox.innerHTML = `
        <button class="lightbox-close" aria-label="닫기">×</button>
        <img src="" alt="">
    `;

    document.body.appendChild(lightbox);

    const closeBtn = lightbox.querySelector(".lightbox-close");
    closeBtn.addEventListener("click", closeLightbox);

    lightbox.addEventListener("click", function (e) {
        if (e.target === lightbox) closeLightbox();
    });

    document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") closeLightbox();
    });
}

function openLightbox(src, alt) {
    const lightbox = document.querySelector(".lightbox");
    const lightboxImg = lightbox.querySelector("img");

    lightboxImg.src = src;
    lightboxImg.alt = alt;

    lightbox.classList.add("active");
    document.body.style.overflow = "hidden";
}

function closeLightbox() {
    const lightbox = document.querySelector(".lightbox");
    if (!lightbox) return;

    lightbox.classList.remove("active");
    document.body.style.overflow = "";
}
emailjs.init("JKsVOKPtnWHIr2BCV");

const contactForm = document.getElementById("contactForm");
const formMessage = document.getElementById("formMessage");

if (contactForm) {

    contactForm.addEventListener("submit", async function(e) {

        e.preventDefault();

        const submitBtn = contactForm.querySelector("button");
        const privacyCheck = contactForm.querySelector('input[type="checkbox"]');

        if (!privacyCheck.checked) {
            formMessage.textContent = "개인정보 수집 및 이용에 동의해 주세요.";
            formMessage.style.color = "#f59e0b";
            formMessage.classList.add("show");
            return;
        }
        
        submitBtn.disabled = true;
        submitBtn.textContent = "전송 중입니다";

        try {

            const formData = {
                name: contactForm.querySelector('input[type="text"]').value,
                phone: contactForm.querySelector('input[type="tel"]').value,
                region: contactForm.querySelectorAll('input[type="text"]')[1].value,
                service: contactForm.querySelector('select').value,
                message: contactForm.querySelector('textarea').value
            };

            await emailjs.send(
                "allbarunclean-waste",
                "template_b4ox5js",
                formData
            );

            formMessage.textContent =
                "상담접수가 완료되었습니다. 확인 후 연락드리겠습니다.";
            formMessage.style.color = "#10b981";
            formMessage.classList.add("show");

            contactForm.reset();

        } catch(error) {

            console.error(error);

            formMessage.textContent =
                "전송 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.";
            formMessage.style.color = "#ef4444";
            formMessage.classList.add("show");

        }

        submitBtn.disabled = false;
        submitBtn.textContent = "상담 접수하기";

    });

}