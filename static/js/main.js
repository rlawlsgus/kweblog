// static/js/main.js

// 알림 개수 확인 및 표시
function checkNotifications() {
  if (document.querySelector(".notification-link")) {
    fetch("/api/unread_notifications")
      .then((response) => response.json())
      .then((data) => {
        const badge = document.getElementById("notification-badge");
        if (data.count > 0) {
          badge.textContent = data.count;
          badge.style.display = "inline-block";
        } else {
          badge.style.display = "none";
        }
      });
  }
}

// 주기적으로 알림 확인
document.addEventListener("DOMContentLoaded", () => {
  checkNotifications();
  setInterval(checkNotifications, 60000); // 1분마다 확인

  // 플래시 메시지 자동 사라짐
  const flashMessages = document.querySelectorAll(".flash-message");
  if (flashMessages.length > 0) {
    setTimeout(() => {
      flashMessages.forEach((msg) => {
        msg.style.opacity = "0";
        msg.style.transition = "opacity 0.5s";
        setTimeout(() => {
          msg.remove();
        }, 500);
      });
    }, 3000);
  }
});
