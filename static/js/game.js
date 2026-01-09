/**
 * 游戏模块交互脚本
 */

// 卡片选择动画
function animateCardSelect(element) {
    element.style.transform = 'scale(0.95)';
    setTimeout(() => {
        element.style.transform = 'scale(1)';
    }, 150);
}
