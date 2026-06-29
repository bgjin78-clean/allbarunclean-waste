document.addEventListener("DOMContentLoaded", function () {
    createGallery("beforeGallery", "before", 8, "폐기물처리 작업 전 현장");
    createGallery("processGallery", "process", 8, "폐기물처리 작업 중 현장");
    createGallery("afterGallery", "after", 8, "폐기물처리 작업 후 현장");

    createLightbox();
    setupContactForm();
});

function createGallery(containerId, prefix, count, altText) {
    const container = document.getElementById(containerId);
    if (!container) return;

    for (let i = 1; i <= count; i++) {
        const number = String(i).padStart(2, "0");
        const img = document.createElement("img");

        img.src = `./images/main/${prefix}-${number}.jpg`;
        img.alt = `${altText} ${i}`;
        img.loading = "lazy";
        img.className = "gallery-img";

        img.onerror = function () {
            if (img.src.endsWith(".jpg")) {
                img.src = `./images/main/${prefix}-${number}.jpeg`;
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

    lightbox.querySelector(".lightbox-close").addEventListener("click", closeLightbox);

    lightbox.addEventListener("click", function (e) {
        if (e.target === lightbox) closeLightbox();
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

function setupContactForm() {
    emailjs.init("JKsVOKPtnWHIr2BCV");

    const contactForm = document.getElementById("contactForm");
    const formMessage = document.getElementById("formMessage");

    if (!contactForm || !formMessage) return;

    contactForm.addEventListener("submit", async function (e) {
        e.preventDefault();

        const submitBtn = contactForm.querySelector('button[type="submit"]');
        const privacyCheck = contactForm.querySelector('input[type="checkbox"]');

        formMessage.classList.remove("show");

        if (!privacyCheck.checked) {
            formMessage.textContent = "개인정보 수집 및 이용에 동의해 주세요.";
            formMessage.style.color = "#f59e0b";
            formMessage.classList.add("show");
            return;
        }

        submitBtn.disabled = true;
        submitBtn.textContent = "접수 중입니다...";

        const formData = {
            name: contactForm.querySelector('input[placeholder="이름"]').value,
            phone: contactForm.querySelector('input[placeholder="연락처"]').value,
            region: contactForm.querySelector('input[placeholder*="작업 지역"]').value,
            service: contactForm.querySelector("select").value,
            message: contactForm.querySelector("textarea").value
        };

        try {
            await emailjs.send(
                "allbarunclean-waste",
                "template_b4ox5js",
                formData
            );

            formMessage.textContent = "상담접수가 완료되었습니다. 확인 후 연락드리겠습니다.";
            formMessage.style.color = "#10b981";
            formMessage.classList.add("show");

            contactForm.reset();

        } catch (error) {
            console.error("EmailJS Error:", error);

            formMessage.textContent = "전송 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.";
            formMessage.style.color = "#ef4444";
            formMessage.classList.add("show");
        }

        submitBtn.disabled = false;
        submitBtn.textContent = "상담 접수하기";
    });
}