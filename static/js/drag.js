/**
 * 拖拽功能模块
 * 支持鼠标拖拽和触摸设备
 */

let draggedElement = null;
let draggedData = null;

// 初始化可拖拽元素
function initDraggable(element) {
    // 鼠标事件
    element.addEventListener('dragstart', handleDragStart);
    element.addEventListener('dragend', handleDragEnd);
    
    // 触摸事件
    element.addEventListener('touchstart', handleTouchStart, { passive: false });
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

// 鼠标拖拽开始
function handleDragStart(e) {
    draggedElement = e.target.closest('.food-item');
    draggedData = {
        id: draggedElement.dataset.id,
        name: draggedElement.dataset.name
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
    
    try {
        const data = JSON.parse(e.dataTransfer.getData('text/plain'));
        if (data && data.id && data.name) {
            onDrop(data.id, data.name);
        }
    } catch (err) {
        console.error('Drop error:', err);
    }
}

// 触摸开始
function handleTouchStart(e) {
    const touch = e.touches[0];
    draggedElement = e.target.closest('.food-item');
    
    if (!draggedElement || draggedElement.classList.contains('opacity-50')) {
        draggedElement = null;
        return;
    }
    
    draggedData = {
        id: draggedElement.dataset.id,
        name: draggedElement.dataset.name
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
    const plateRect = plate.getBoundingClientRect();
    
    if (touch.clientX >= plateRect.left && touch.clientX <= plateRect.right &&
        touch.clientY >= plateRect.top && touch.clientY <= plateRect.bottom) {
        plate.classList.add('drag-over');
    } else {
        plate.classList.remove('drag-over');
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
    const plateRect = plate.getBoundingClientRect();
    
    plate.classList.remove('drag-over');
    
    if (touch.clientX >= plateRect.left && touch.clientX <= plateRect.right &&
        touch.clientY >= plateRect.top && touch.clientY <= plateRect.bottom) {
        // 在放置区内
        if (plate._onDrop && draggedData) {
            plate._onDrop(draggedData.id, draggedData.name);
        }
    }
    
    draggedElement = null;
    draggedData = null;
}

// 更新拖拽副本位置
function updateClonePosition(clone, touch) {
    clone.style.left = (touch.clientX - clone.offsetWidth / 2) + 'px';
    clone.style.top = (touch.clientY - clone.offsetHeight / 2) + 'px';
}
