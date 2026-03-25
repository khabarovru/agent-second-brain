module.exports = async function () {
    const bar = document.querySelector(".status-bar");

    if (!bar) return;

    // Переключаем видимость через стиль
    if (bar.style.display === "none") {
        bar.style.display = "";
        localStorage.setItem("statusBarHidden", "false");
    } else {
        bar.style.display = "none";
        localStorage.setItem("statusBarHidden", "true");
    }
};

// Восстановление состояния при запуске Obsidian
document.addEventListener("DOMContentLoaded", () => {
    const bar = document.querySelector(".status-bar");
    if (!bar) return;

    if (localStorage.getItem("statusBarHidden") === "true") {
        bar.style.display = "none";
    }
});
