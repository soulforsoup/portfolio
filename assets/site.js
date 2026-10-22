/* Progressive enhancement: every page and original image works without JS. */
(function () {
  'use strict';
  document.documentElement.classList.add('has-js');

  var menuButton = document.querySelector('.menu-toggle');
  var navigation = document.querySelector('.nav-links');
  function closeMenu() {
    if (!menuButton || !navigation) return;
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.firstElementChild.textContent = 'Menu';
    navigation.classList.remove('is-open');
  }
  if (menuButton && navigation) {
    menuButton.addEventListener('click', function () {
      var open = menuButton.getAttribute('aria-expanded') !== 'true';
      menuButton.setAttribute('aria-expanded', String(open));
      menuButton.firstElementChild.textContent = open ? 'Close' : 'Menu';
      navigation.classList.toggle('is-open', open);
    });
    navigation.addEventListener('click', function (event) {
      if (event.target.closest('a')) closeMenu();
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
        closeMenu();
        menuButton.focus();
      }
    });
    window.matchMedia('(min-width: 601px)').addEventListener('change', closeMenu);
  }

  var filterGroups = document.querySelectorAll('[data-filters]');
  filterGroups.forEach(function (group) {
    var grid = document.getElementById(group.dataset.filters);
    if (!grid) return;
    var filters = Array.from(group.querySelectorAll('[data-filter]'));
    var items = Array.from(grid.querySelectorAll('[data-category]'));
    var count = document.getElementById(group.dataset.count);
    group.hidden = false;
    filters.forEach(function (button) {
      button.addEventListener('click', function () {
        var value = button.dataset.filter;
        var visible = 0;
        filters.forEach(function (other) {
          other.setAttribute('aria-pressed', String(other === button));
        });
        items.forEach(function (item) {
          item.hidden = value !== 'all' && item.dataset.category !== value;
          if (!item.hidden) visible += 1;
        });
        grid.classList.toggle('is-filtered', value !== 'all');
        if (count) count.textContent = String(visible).padStart(2, '0') + ' ' + group.dataset.noun;
      });
    });
  });

  var supportsDialog = typeof HTMLDialogElement !== 'undefined' &&
    typeof HTMLDialogElement.prototype.showModal === 'function';
  var previouslyFocused = null;
  function openDialog(dialog) {
    previouslyFocused = document.activeElement;
    dialog.showModal();
    document.body.classList.add('modal-open');
  }
  function restorePage(dialog) {
    document.body.classList.remove('modal-open');
    if (previouslyFocused && document.contains(previouslyFocused)) previouslyFocused.focus();
    if (dialog.id === 'video-viewer') {
      var frame = dialog.querySelector('iframe');
      if (frame) frame.remove();
    }
  }
  if (supportsDialog) {
    document.querySelectorAll('dialog').forEach(function (dialog) {
      dialog.querySelectorAll('[data-close]').forEach(function (button) {
        button.addEventListener('click', function () { dialog.close(); });
      });
      dialog.addEventListener('close', function () { restorePage(dialog); });
    });
  }

  var photoDialog = document.getElementById('photo-viewer');
  if (photoDialog && supportsDialog) {
    var photoLinks = Array.from(document.querySelectorAll('[data-photo]'));
    var activePhotos = [];
    var photoIndex = 0;
    var displayImage = photoDialog.querySelector('.viewer-image');
    var photoTitle = document.getElementById('photo-title');
    var photoCount = document.getElementById('photo-position');
    var originalLink = document.getElementById('photo-original');
    function renderPhoto() {
      var anchor = activePhotos[photoIndex];
      var img = anchor.querySelector('img');
      displayImage.src = anchor.href;
      displayImage.alt = img.alt;
      photoTitle.textContent = img.alt;
      photoCount.textContent = String(photoIndex + 1).padStart(2, '0') + ' / ' + String(activePhotos.length).padStart(2, '0');
      originalLink.href = anchor.href;
    }
    function stepPhoto(delta) {
      photoIndex = (photoIndex + delta + activePhotos.length) % activePhotos.length;
      renderPhoto();
    }
    photoLinks.forEach(function (anchor) {
      anchor.addEventListener('click', function (event) {
        if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        activePhotos = photoLinks.filter(function (link) { return !link.closest('[data-category]').hidden; });
        photoIndex = activePhotos.indexOf(anchor);
        renderPhoto();
        openDialog(photoDialog);
      });
    });
    photoDialog.querySelector('[data-prev]').addEventListener('click', function () { stepPhoto(-1); });
    photoDialog.querySelector('[data-next]').addEventListener('click', function () { stepPhoto(1); });
    photoDialog.addEventListener('keydown', function (event) {
      if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
        event.preventDefault();
        stepPhoto(event.key === 'ArrowRight' ? 1 : -1);
      }
    });
    var startX = 0;
    var startY = 0;
    displayImage.addEventListener('touchstart', function (event) {
      if (event.touches.length !== 1) return;
      startX = event.touches[0].clientX;
      startY = event.touches[0].clientY;
    }, { passive: true });
    displayImage.addEventListener('touchend', function (event) {
      if (event.changedTouches.length !== 1 || event.touches.length > 0) return;
      var deltaX = event.changedTouches[0].clientX - startX;
      var deltaY = event.changedTouches[0].clientY - startY;
      if (Math.abs(deltaX) > 65 && Math.abs(deltaX) > Math.abs(deltaY) * 1.5) stepPhoto(deltaX < 0 ? 1 : -1);
    }, { passive: true });
  }

  var videoDialog = document.getElementById('video-viewer');
  if (videoDialog && supportsDialog) {
    document.querySelectorAll('[data-video]').forEach(function (anchor) {
      anchor.addEventListener('click', function (event) {
        if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
        var id = anchor.dataset.video;
        if (!/^[a-zA-Z0-9_-]{11}$/.test(id)) return;
        event.preventDefault();
        var title = anchor.dataset.title;
        document.getElementById('video-title').textContent = title;
        document.getElementById('video-external').href = 'https://www.youtube.com/watch?v=' + id;
        document.getElementById('video-description').textContent = anchor.dataset.description || '';
        var frame = document.createElement('iframe');
        frame.className = 'video-embed';
        frame.title = title;
        frame.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0';
        frame.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; fullscreen';
        frame.referrerPolicy = 'strict-origin-when-cross-origin';
        frame.allowFullscreen = true;
        videoDialog.querySelector('.video-stage').prepend(frame);
        openDialog(videoDialog);
      });
    });
  }

  /* An unavailable thumbnail leaves a locally rendered title cover in place. */
  document.querySelectorAll('.project-cover img').forEach(function (img) {
    img.addEventListener('error', function () { img.hidden = true; });
    if (img.complete && img.naturalWidth === 0) img.hidden = true;
  });
}());
