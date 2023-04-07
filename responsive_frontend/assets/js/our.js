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

function detachElements() {
  searchInput.parentNode.removeChild(searchInput);
  navList.parentNode.removeChild(navList);
};