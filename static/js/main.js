// 全局配置
const CONFIG = {
    timeoutSeconds: 60,
    warningSeconds: 10
};

// 无操作超时处理
let idleTimer = null;
let warningTimer = null;

function resetIdleTimer() {
    clearTimeout(idleTimer);
    clearTimeout(warningTimer);
    hideTimeoutWarning();
    
    // 设置警告定时器
    warningTimer = setTimeout(() => {
        showTimeoutWarning();
    }, (CONFIG.timeoutSeconds - CONFIG.warningSeconds) * 1000);
    
    // 设置超时定时器
    idleTimer = setTimeout(() => {
        window.location.href = '/';
    }, CONFIG.timeoutSeconds * 1000);
}

function showTimeoutWarning() {
    const modal = document.getElementById('timeout-modal');
    if (modal) {
        modal.classList.remove('hidden');
        startCountdown();
    }
}

function hideTimeoutWarning() {
    const modal = document.getElementById('timeout-modal');
    if (modal) {
        modal.classList.add('hidden');
    }
}

function startCountdown() {
    let seconds = CONFIG.warningSeconds;
    const countdownEl = document.getElementById('countdown');
    
    const interval = setInterval(() => {
        seconds--;
        if (countdownEl) {
            countdownEl.textContent = seconds;
        }
        if (seconds <= 0) {
            clearInterval(interval);
        }
    }, 1000);
}

// 监听用户操作
function initIdleDetection() {
    const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click'];
    events.forEach(event => {
        document.addEventListener(event, resetIdleTimer, true);
    });
    resetIdleTimer();
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    // 首页不启用超时检测
    if (window.location.pathname !== '/') {
        initIdleDetection();
    }
});

// CSRF Token 获取
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');
