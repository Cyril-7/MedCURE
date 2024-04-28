// get the slider element
const slider = document.getElementById("slider");

// create the slider handle element
const handle = document.createElement("div");
handle.classList.add("slider-handle");

// add the handle to the slider
slider.appendChild(handle);

// set up the event listeners
let isDragging = false;
let startX = 0;
let handleX = 0;

handle.addEventListener("mousedown", (event) => {
  isDragging = true;
  startX = event.clientX;
  handleX = handle.offsetLeft;
});

document.addEventListener("mousemove", (event) => {
  if (isDragging) {
    const deltaX = event.clientX - startX;
    const newHandleX = handleX + deltaX;
    const minHandleX = 0;
    const maxHandleX = slider.offsetWidth - handle.offsetWidth;
    if (newHandleX >= minHandleX && newHandleX <= maxHandleX) {
      handle.style.left = newHandleX + "px";
    }
  }
});

document.addEventListener("mouseup", () => {
  isDragging = false;
});


window.addEventListener("load", function(){
  var checkbox  = document.getElementById('{{form.check.id}}');
  var x = document.getElementById('{{form.password.id}}');
  checkbox.addEventListener('change', function() {
      if(this.checked) {
          x.type = 'text'; 
      } else {
          x.type = 'password'; 
      }
  });
});