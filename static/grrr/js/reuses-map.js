/**
 *   Nodes section map
 */

 // Ready, only IE 9 or bigger
 var ready = function(callback) {
     document.readyState === "interactive" ||
     document.readyState === "complete" ? callback() : document.addEventListener("DOMContentLoaded", callback);
 };

/**
*  Make an AJAX GET
*/

function get(url, callback, error_callback)
{
   var ajax = new XMLHttpRequest();
   var SUCCESS = 200;

   ajax.onreadystatechange = function() {
       if (ajax.readyState == XMLHttpRequest.DONE) {
           if (ajax.status == SUCCESS) {
               callback(ajax.response);
           } else if(error_callback){
               error_callback(ajax.response);
           }
       }
   };
   ajax.open("GET", url, true);
   ajax.send();
}

ready( function()
{
    // Map icon
    var icon = L.divIcon({
        html        : '<span class="icon-reuse"></span><span class="inner"></span>',
        iconSize    : [25, 40],
        iconAnchor  : [13, 40],
        popupAnchor : [0, -25],
    });

    // Map initial settings
    var map = L.map("map-header", {
        center: [40, 2],
        zoom: 6,
        minZoom: 5,
        scrollWheelZoom: false,
        fullscreenControl: true
    });

    // Add tile layer to map
    L.tileLayer('https://api.mapbox.com/styles/v1/ale/cj3rpgd2n00142slekpjya98f/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiYWxlIiwiYSI6ImpKQ2dnekEifQ.GjyY2X3Wa6pgoHTPOrUBdA', {
        'attribution': '<a href="https://www.mapbox.com/about/maps/" target="_blank">© Mapbox</a> <a href="http://www.openstreetmap.org/about/" target="_blank">© OpenStreetMap</a>'
    }).addTo(map);

    // Add data to map
    get("/api/reusos", function(response)
    {
        JSON.parse(response).forEach(function(i){
            var marker = L.marker([ i.lat, i.lon ], { icon: icon }).bindPopup( i.popup ).addTo(map);
        });
    }, function(error){
        console.log(error);
    });

});
