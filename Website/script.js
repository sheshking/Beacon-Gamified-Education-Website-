// ============================================
// BEACON — sign-up page behaviour
// ============================================

// difficulty button group (single-select)
document.querySelectorAll('[data-group]').forEach((group) => {
  const options = group.querySelectorAll('[data-value]');
  options.forEach((opt) => {
    opt.addEventListener('click', () => {
      options.forEach((o) => o.classList.remove('active'));
      opt.classList.add('active');
      const hiddenInput = document.getElementById(group.dataset.group);
      if (hiddenInput) {
        hiddenInput.value = opt.dataset.value;
        hiddenInput.dispatchEvent(new Event('change'));
      }
      const fieldEl = group.closest('.field');
      if (fieldEl) fieldEl.classList.remove('invalid');
    });
  });
});

function markInvalid(fieldEl) {
  fieldEl.classList.add('invalid');
}

function clearInvalid(fieldEl) {
  fieldEl.classList.remove('invalid');
}

function isValidEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

// ---------- photo upload ----------
let uploadedPhoto = null; // holds the resized dataURL, or null if none chosen

const photoInput = document.getElementById('photoInput');
const photoPreview = document.getElementById('photoPreview');
const photoRemove = document.getElementById('photoRemove');

function resizeImage(file, maxSize, callback) {
  const reader = new FileReader();
  reader.onload = (e) => {
    const img = new Image();
    img.onload = () => {
      const canvas = document.createElement('canvas');
      let { width, height } = img;
      if (width > height) {
        if (width > maxSize) { height *= maxSize / width; width = maxSize; }
      } else {
        if (height > maxSize) { width *= maxSize / height; height = maxSize; }
      }
      canvas.width = width;
      canvas.height = height;
      canvas.getContext('2d').drawImage(img, 0, 0, width, height);
      callback(canvas.toDataURL('image/jpeg', 0.85));
    };
    img.src = e.target.result;
  };
  reader.readAsDataURL(file);
}

if (photoInput) {
  photoInput.addEventListener('change', () => {
    const file = photoInput.files[0];
    if (!file) return;
    resizeImage(file, 200, (dataUrl) => {
      uploadedPhoto = dataUrl;
      photoPreview.innerHTML = `<img src="${dataUrl}" alt="Profile photo" />`;
      photoRemove.hidden = false;
    });
  });
}

if (photoRemove) {
  photoRemove.addEventListener('click', () => {
    uploadedPhoto = null;
    photoInput.value = '';
    photoPreview.innerHTML = '<span class="photo-placeholder">&#128100;</span>';
    photoRemove.hidden = true;
  });
}

const signupForm = document.getElementById('signupForm');
if (signupForm) {
  signupForm.addEventListener('submit', (e) => {
    e.preventDefault();
    let valid = true;

    const username = document.getElementById('username');
    const usernameField = username.closest('.field');
    if (username.value.trim().length < 3) {
      markInvalid(usernameField);
      valid = false;
    } else {
      clearInvalid(usernameField);
    }

    const email = document.getElementById('email');
    const emailField = email.closest('.field');
    if (!isValidEmail(email.value.trim())) {
      markInvalid(emailField);
      valid = false;
    } else {
      clearInvalid(emailField);
    }

    const grade = document.getElementById('grade');
    const gradeField = grade.closest('.field');
    if (!grade.value) {
      markInvalid(gradeField);
      valid = false;
    } else {
      clearInvalid(gradeField);
    }

    const experience = document.getElementById('experience');
    const experienceField = document.getElementById('difficultyGroup');
    if (!experience.value) {
      experienceField.classList.add('invalid');
      valid = false;
    } else {
      experienceField.classList.remove('invalid');
    }

    if (!valid) return;

    try {
      localStorage.setItem('beaconPlayer', JSON.stringify({
        username: username.value.trim(),
        grade: grade.value,
        experience: experience.value,
        photo: uploadedPhoto // null if the user didn't upload one
      }));
    } catch (e) {
      // localStorage unavailable, or the photo was too large to store —
      // carry on without persistence rather than blocking signup
    }

    const banner = document.getElementById('successBanner');
    banner.classList.add('show');
    banner.textContent =
      `PLAYER CREATED: ${username.value.trim()} — Class ${grade.value} · ${experience.value}`;
    signupForm.reset();
    document.querySelectorAll('.diff-btn.active').forEach((el) => el.classList.remove('active'));
    uploadedPhoto = null;
    photoPreview.innerHTML = '<span class="photo-placeholder">&#128100;</span>';
    photoRemove.hidden = true;

    setTimeout(() => {
      window.location.href = 'home.html';
    }, 1400);
  });
}
