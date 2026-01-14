/**
 * 拖拽功能模块
 * 支持鼠标拖拽和触摸设备
 */

let draggedElement = null;
let draggedData = null;
let dragSource = null; // 'food-list' 或 'plate'

// 长按删除相关变量
let longPressTimer = null;
let longPressTarget = null;
const LONG_PRESS_DURATION = 1000; // 长按1秒
let onPlateRemove = null; // 餐盘删除回调

// 初始化可拖拽元素
function initDraggable(element, source = 'food-list') {
    // 鼠标事件
    element.addEventListener('dragstart', (e) => handleDragStart(e, source));
    element.addEventListener('dragend', handleDragEnd);
    
    // 触摸事件
    element.addEventListener('touchstart', (e) => handleTouchStart(e, source), { passive: false });
    element.addEventListener('touchmove', handleTouchMove, { passive: false });
    element.addEventListener('touchend', handleTouchEnd);
}

// 初始化放置区域
function initPlateDropZone(plate, onDrop) {
    plate.addEventListener('dragover', handleDragOver);
    plate.addEventListener('dragleave', handleDragLeave);
    plate.addEventListener('drop', function(e) {
        handleDrop(e, onDrop);
    });
    
    // 存储回调
    plate._onDrop = onDrop;
}

// 初始化食物列表为放置区（用于从餐盘拖回）
function initFoodListDropZone(foodListContainer, onRemove) {
    foodListContainer.addEventListener('dragover', handleDragOver);
    foodListContainer.addEventListener('dragleave', handleDragLeave);
    foodListContainer.addEventListener('drop', function(e) {
        e.preventDefault();
        e.currentTarget.classList.remove('drag-over');
        
        if (dragSource === 'plate' && draggedData) {
            onRemove(draggedData.id);
        }
    });
    
    foodListContainer._onRemove = onRemove;
}

// 鼠标拖拽开始
function handleDragStart(e, source) {
    draggedElement = e.target.closest('.food-item, .selected-food');
    dragSource = source;
    draggedData = {
        id: draggedElement.dataset.id,
        name: draggedElement.dataset.name,
        image: draggedElement.dataset.image || ''
    };
    draggedElement.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', JSON.stringify(draggedData));
}

// 鼠标拖拽结束
function handleDragEnd(e) {
    if (draggedElement) {
        draggedElement.classList.remove('dragging');
    }
    draggedElement = null;
    draggedData = null;
    dragSource = null;
}

// 拖拽经过放置区
function handleDragOver(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    e.currentTarget.classList.add('drag-over');
}

// 拖拽离开放置区
function handleDragLeave(e) {
    e.currentTarget.classList.remove('drag-over');
}

// 放置
function handleDrop(e, onDrop) {
    e.preventDefault();
    e.currentTarget.classList.remove('drag-over');
    
    // 只处理从食物列表拖到餐盘的情况
    if (dragSource === 'plate') return;
    
    try {
        const data = JSON.parse(e.dataTransfer.getData('text/plain'));
        if (data && data.id && data.name) {
            onDrop(data.id, data.name, data.image);
        }
    } catch (err) {
        console.error('Drop error:', err);
    }
}

// 触摸开始
function handleTouchStart(e, source) {
    const touch = e.touches[0];
    draggedElement = e.target.closest('.food-item, .selected-food');
    
    if (!draggedElement || (source === 'food-list' && draggedElement.classList.contains('opacity-40'))) {
        draggedElement = null;
        return;
    }
    
    dragSource = source;
    draggedData = {
        id: draggedElement.dataset.id,
        name: draggedElement.dataset.name,
        image: draggedElement.dataset.image || ''
    };
    
    draggedElement.classList.add('dragging');
    
    // 创建拖拽副本
    const clone = draggedElement.cloneNode(true);
    clone.id = 'drag-clone';
    clone.style.position = 'fixed';
    clone.style.zIndex = '9999';
    clone.style.pointerEvents = 'none';
    clone.style.width = draggedElement.offsetWidth + 'px';
    clone.style.opacity = '0.8';
    clone.style.transform = 'scale(1.1)';
    document.body.appendChild(clone);
    
    updateClonePosition(clone, touch);
}

// 触摸移动
function handleTouchMove(e) {
    if (!draggedElement) return;
    
    e.preventDefault();
    const touch = e.touches[0];
    const clone = document.getElementById('drag-clone');
    
    if (clone) {
        updateClonePosition(clone, touch);
    }
    
    // 检测是否在放置区上方
    const plate = document.getElementById('plate');
    const foodList = document.getElementById('food-list');
    const plateRect = plate.getBoundingClientRect();
    const foodListRect = foodList.getBoundingClientRect();
    
    if (touch.clientX >= plateRect.left && touch.clientX <= plateRect.right &&
        touch.clientY >= plateRect.top && touch.clientY <= plateRect.bottom) {
        plate.classList.add('drag-over');
        foodList.classList.remove('drag-over');
    } else if (touch.clientX >= foodListRect.left && touch.clientX <= foodListRect.right &&
               touch.clientY >= foodListRect.top && touch.clientY <= foodListRect.bottom) {
        foodList.classList.add('drag-over');
        plate.classList.remove('drag-over');
    } else {
        plate.classList.remove('drag-over');
        foodList.classList.remove('drag-over');
    }
}

// 触摸结束
function handleTouchEnd(e) {
    if (!draggedElement) return;
    
    const clone = document.getElementById('drag-clone');
    if (clone) {
        clone.remove();
    }
    
    draggedElement.classList.remove('dragging');
    
    // 检测放置位置
    const touch = e.changedTouches[0];
    const plate = document.getElementById('plate');
    const foodList = document.getElementById('food-list');
    const plateRect = plate.getBoundingClientRect();
    const foodListRect = foodList.getBoundingClientRect();
    
    plate.classList.remove('drag-over');
    foodList.classList.remove('drag-over');
    
    if (touch.clientX >= plateRect.left && touch.clientX <= plateRect.right &&
        touch.clientY >= plateRect.top && touch.clientY <= plateRect.bottom) {
        // 拖到餐盘
        if (dragSource === 'food-list' && plate._onDrop && draggedData) {
            plate._onDrop(draggedData.id, draggedData.name, draggedData.image);
        }
    } else if (touch.clientX >= foodListRect.left && touch.clientX <= foodListRect.right &&
               touch.clientY >= foodListRect.top && touch.clientY <= foodListRect.bottom) {
        // 拖回食物列表
        if (dragSource === 'plate' && foodList._onRemove && draggedData) {
            foodList._onRemove(draggedData.id);
        }
    }
    
    draggedElement = null;
    draggedData = null;
    dragSource = null;
}

// 更新拖拽副本位置
function updateClonePosition(clone, touch) {
    clone.style.left = (touch.clientX - clone.offsetWidth / 2) + 'px';
    clone.style.top = (touch.clientY - clone.offsetHeight / 2) + 'px';
}
