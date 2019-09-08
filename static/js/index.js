//set unique path in url
function setUniquePath(a){
    var path = document.getElementById('urlBar');
    path.value = window.location + a;
}

var options = {//options for navigator
    enableHighAccuracy: true,
    timeout: 5000,
    maximumAge: 0
};
function success(position,uniquePath) {//execute on success
    console.log("refreshed");
    
    $.post("/updateLocat",{//a post call w/o refreshing page
        
        lat: position.coords.latitude,
        long: position.coords.longitude,
        path: uniquePath
    });
}
function sendCoords(uniquePath){//sending coords
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position){//watchPosition repeats
            success(position,uniquePath);
        },function(){},options);
    } else { 
        x.innerHTML = "Geolocation is not supported by this browser.";
    }
}

function copyToBoard(){//copy button
  var copyText = document.getElementById("urlBar");
  copyText.select();
  copyText.setSelectionRange(0, 99999);
  document.execCommand("copy");
}