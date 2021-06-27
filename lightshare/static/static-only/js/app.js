(function(document) {
  'use strict';
  
  document.addEventListener('polymer-ready', function() {
    console.log(document.querySelector("core-header-panel"));
    var coreHeaderPanel = document.querySelector("core-header-panel");
    coreHeaderPanel.addEventListener("scroll_to_search", function(event) {
      
        document.querySelector('#mainContainer').scroller.scrollTop = 1120;
console.log( document.querySelector('#mainContainer').scroller.scrollTop);
    });
    coreHeaderPanel.addEventListener("scroll", function(event) {
      //console.log(document);
        if (event.detail.target.scrollTop >= 30) {
         //console.log(event.detail.target.scrollTop);
            document.querySelector(".logo").classList.add('zoomed_logo');
         } else {
          //console.log("as");
            document.querySelector(".logo").classList.remove('zoomed_logo');
         }
    });
     document.querySelector("X-login").addEventListener('back_to_main_screen',function(event){
      //event.srcElement.hover();
      document.querySelector("core-header-panel").classList.remove('hidden');
      document.querySelector("X-login").classList.add('hidden');
      document.querySelector("paper-tabs").selected=-1;
    });
    var menus = document.querySelector('#menu');
    menus.addEventListener('core-select',function(event){
      if(event.detail.isSelected){
        if(event.target.selected==1){
          document.querySelector("core-header-panel").classList.add('hidden');
          document.querySelector("X-login").classList.remove('hidden');
        }
      }
    });
  });
  

// wrap document so it plays nice with other libraries
// http://www.polymer-project.org/platform/shadow-dom.html#wrappers
})(wrap(document));