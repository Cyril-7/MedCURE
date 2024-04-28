var blocks = document.querySelectorAll('.block');
var currentBlockIndex = 0;
var maxIndex = blocks.length - 1;
var visibleBlocks = 3;

function showBlocks(startIndex, numBlocks) {
    for (var i = startIndex; i < startIndex + numBlocks; i++) {
        if (blocks[i]) {
            blocks[i].classList.add('visible');
        }
    }
    if (startIndex + visibleBlocks > 8) {
        document.querySelector('.right-arrow').classList.add('hide-right-arrow');
    } else {
        document.querySelector('.right-arrow').classList.remove('hide-right-arrow');
    }
    if (startIndex === 0) {
        document.querySelector('.left-arrow').classList.remove('show-left-arrow');
    } else {
        document.querySelector('.left-arrow').classList.add('show-left-arrow');
    }
}

function hideBlocks() {
    for (var i = 0; i <= maxIndex; i++) {
        blocks[i].classList.remove('visible');
    }
}

showBlocks(currentBlockIndex, visibleBlocks);

document.querySelector('.left-arrow').addEventListener('click', function() {
    if (currentBlockIndex > 0) {
        currentBlockIndex -= 1;
        hideBlocks();
        showBlocks(currentBlockIndex, visibleBlocks);
        if (currentBlockIndex === 0) {
            document.querySelector('.left-arrow').classList.remove('show-left-arrow');
        }
        if (currentBlockIndex + visibleBlocks < blocks.length) {
            document.querySelector('.right-arrow').classList.add('show-right-arrow');
        }
    }
});

document.querySelector('.right-arrow').addEventListener('click', function() {
    if (currentBlockIndex + visibleBlocks <= maxIndex) {
        currentBlockIndex += 1;
        hideBlocks();
        showBlocks(currentBlockIndex, visibleBlocks);
        if (currentBlockIndex > 0) {
            document.querySelector('.left-arrow').classList.add('show-left-arrow');
        }
        if (currentBlockIndex + visibleBlocks > maxIndex) {
            document.querySelector('.right-arrow').classList.remove('show-right-arrow');
        }
    }
});