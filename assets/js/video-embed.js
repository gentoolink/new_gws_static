// Click-to-play video embeds.
//
// Each embed ships as a <button class="video-facade" data-video-id="..."> holding
// a locally hosted still. The YouTube iframe is only built once someone actually
// presses play, so a page carrying an embed doesn't cost every visitor ~1MB of
// player JS -- or a YouTube cookie -- just to scroll past it. The nocookie host
// keeps it that way for people who do press play.
//
// Used by index.html (#problem) and blog-semantic-markup-ai-ready.html.

document.querySelectorAll('.video-facade').forEach(function (btn) {
  btn.addEventListener('click', function () {
    var frame = document.createElement('iframe');
    frame.src = 'https://www.youtube-nocookie.com/embed/' + btn.dataset.videoId + '?autoplay=1&rel=0';
    frame.title = btn.getAttribute('aria-label').replace(/^Play video: /, '');
    frame.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; web-share';
    frame.referrerPolicy = 'strict-origin-when-cross-origin';
    frame.allowFullscreen = true;
    btn.replaceWith(frame);
    frame.focus();
  });
});
