var iframe = document.getElementById("plot");
    
iframe.onload = function(){
    iframe.style.height = iframe.contentWindow.document.body.scrollHeight + 'px';
    iframe.style.width = iframe.contentWindow.document.body.scrollWidth + 'px';
}