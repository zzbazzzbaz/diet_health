/**
 * 问答模块交互脚本
 */

// 选项点击动画
function animateOption(element, isCorrect) {
    element.style.transform = 'scale(0.98)';
    setTimeout(() => {
        element.style.transform = 'scale(1)';
    }, 100);
}

// 显示解析动画
function showExplanation(element) {
    element.style.opacity = '0';
    element.style.transform = 'translateY(10px)';
    element.classList.remove('hidden');
    
    requestAnimationFrame(() => {
        element.style.transition = 'all 0.3s ease';
        element.style.opacity = '1';
        element.style.transform = 'translateY(0)';
    });
}
