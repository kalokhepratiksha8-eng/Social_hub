// Like button toggle
document.addEventListener('click', function(e) {
  const btn = e.target.closest('.like-btn');
  if (!btn) return;
  e.preventDefault();

  const postId = btn.dataset.postId;
  const csrf = btn.dataset.csrf;

  fetch(`/post/${postId}/like/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrf,
      'Content-Type': 'application/json',
    }
  })
  .then(res => res.json())
  .then(data => {
    const svg = btn.querySelector('svg');
    if (data.liked) {
      btn.classList.add('liked');
      if (svg) { svg.setAttribute('fill', '#e24b4a'); svg.setAttribute('stroke', '#e24b4a'); }
    } else {
      btn.classList.remove('liked');
      if (svg) { svg.setAttribute('fill', 'none'); svg.setAttribute('stroke', 'currentColor'); }
    }
    const likesEl = document.getElementById(`likes-${postId}`);
    if (likesEl) likesEl.textContent = data.likes_count;
  })
  .catch(err => console.error('Like error:', err));
});

// Follow button toggle
document.addEventListener('click', function(e) {
  const btn = e.target.closest('.follow-btn');
  if (!btn) return;

  const username = btn.dataset.username;
  const csrf = btn.dataset.csrf;

  fetch(`/profile/${username}/follow/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrf,
      'Content-Type': 'application/json',
    }
  })
  .then(res => res.json())
  .then(data => {
    if (data.following) {
      btn.textContent = 'Following';
      btn.classList.add('following');
    } else {
      btn.textContent = 'Follow';
      btn.classList.remove('following');
    }
    const countEl = document.getElementById('followers-count');
    if (countEl) countEl.textContent = data.followers_count;
  })
  .catch(err => console.error('Follow error:', err));
});

// Auto-dismiss messages
document.addEventListener('DOMContentLoaded', function() {
  const messages = document.querySelectorAll('.message');
  messages.forEach(msg => {
    setTimeout(() => {
      msg.style.transition = 'opacity .4s';
      msg.style.opacity = '0';
      setTimeout(() => msg.remove(), 400);
    }, 3000);
  });
});

// Double-tap to like on post image
document.querySelectorAll('.post-image-wrap').forEach(wrap => {
  let lastTap = 0;
  wrap.addEventListener('click', function() {
    const now = Date.now();
    if (now - lastTap < 300) {
      const postCard = wrap.closest('.post-card');
      if (postCard) {
        const likeBtn = postCard.querySelector('.like-btn');
        if (likeBtn && !likeBtn.classList.contains('liked')) {
          likeBtn.click();
        }
      }
    }
    lastTap = now;
  });
});
