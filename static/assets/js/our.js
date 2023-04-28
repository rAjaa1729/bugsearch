var resizing = false;
window.addEventListener('resize', function(){
  if(resizing) return;
  resizing = true;
  (!window.requestAnimationFrame) ? setTimeout(moveNavigation, 300) : window.requestAnimationFrame(moveNavigation);
});
window.dispatchEvent(new Event('resize'));//trigger the moveNavigation function

function moveNavigation(){
  var mq = checkMQ();
  if ( mq == 'mobile' && !Util.hasClass(navList.parentNode, 'js-cd-side-nav') ) {
    detachElements();
    sidebar.appendChild(navList);
    sidebar.insertBefore(searchInput, sidebar.firstChild);
  } else if ( mq == 'desktop' && !Util.hasClass(navList.parentNode, 'js-cd-main-header') ) {
    detachElements();
    mainHeader.appendChild(navList);
    mainHeader.insertBefore(searchInput, mainHeader.firstChild.nextSibling);
  }
  resizing = false;
};



// function detachElements() {
//   searchInput.parentNode.removeChild(searchInput);
//   navList.parentNode.removeChild(navList);
// };
// const likeBtn1 = document.getElementById("like-btn1");
// const dislikeBtn1 = document.getElementById("dislike-btn1");
// const counter1 = document.getElementById("counter1");

// let count1 = 0;

// likeBtn1.addEventListener("click", () => {
//   count1++;
//   counter1.innerText = count1;
// });

// dislikeBtn1.addEventListener("click", () => {
//   count1--;
//   counter1.innerText = count1;
// });

// const likeBtn2 = document.getElementById("like-btn2");
// const dislikeBtn2 = document.getElementById("dislike-btn2");
// const counter2 = document.getElementById("counter2");

// let count2 = 0;

// likeBtn2.addEventListener("click", () => {
//   count2++;
//   counter2.innerText = count2;
// });

// dislikeBtn2.addEventListener("click", () => {
//   count2--;
//   counter2.innerText = count2;
// });

// const likeBtn3 = document.getElementById("like-btn3");
// const dislikeBtn3 = document.getElementById("dislike-btn3");
// const counter3 = document.getElementById("counter3");

// let count3 = 0;

// likeBtn3.addEventListener("click", () => {
//   count3++;
//   counter3.innerText = count3;
// });

// dislikeBtn3.addEventListener("click", () => {
//   count3--;
//   counter3.innerText = count3;
// });

// const likeBtn4 = document.getElementById("like-btn4");
// const dislikeBtn4 = document.getElementById("dislike-btn4");
// const counter4 = document.getElementById("counter4");

// let count4 = 0;

// likeBtn4.addEventListener("click", () => {
//   count4++;
//   counter4.innerText = count4;
// });
// 4
// dislikeBtn4.addEventListener("click", () => {
//   count4--;
//   counter4.innerText = count4;
// });
