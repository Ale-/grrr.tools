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

var l = 'all';
var f = 'all';

var toggleMarkers = function(){
  $('.leaflet-marker-icon').hide();
  var selected = '.leaflet-marker-icon';
  if(l != 'all')
      selected += '.' + l;
  if(f != 'all')
      selected += '.' + f;
  $(selected).show();
}

$('.frontmap-legend__filter--legend').click( function(){
    l = $(this).attr('data-key');
    $('.frontmap-legend__filter--legend').each( function(i, it){
        $(it).removeClass('active');
    })
    $(this).addClass('active');
    toggleMarkers();
});

$('.frontmap-legend__filter--filter').click( function(){
    f = $(this).attr('data-key');
    $('.frontmap-legend__filter--filter').each( function(i, it){
        $(it).removeClass('active');
    })
    $(this).addClass('active');
    toggleMarkers();
});



ready( function()
{
  //Markers
  var offer_marker = function(material){
      return L.divIcon({
          html: '<span class="icon-offer"></span><i class="inner"></i>',
          iconSize: [25, 40],
          iconAnchor: [13, 40],
          popupAnchor: [0, -25],
          className: "of " + material.toLowerCase(),
      });
  }
  var need_marker = function(material){
      return L.divIcon({
          html: '<span class="icon-demand"></span><i class="inner"></i>',
          iconSize: [25, 40],
          iconAnchor: [13, 40],
          popupAnchor: [0, -25],
          className: "de " + material.toLowerCase(),
      });
  }

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
    get("/api/batches", function(response)
    {
        JSON.parse(response).forEach(function(i){
            var icon = i.cat == 'of' ? offer_marker(i.mat) : need_marker(i.mat);
            var message = "<img src='" + i.img + "' />" +
                          "<p class='batch-category'>" + i.spa + (i.cat == 'of' ? ' ofrece' : ' necesita') + "</p>" +
                          "<h5 class='batch-name'><a href='" + i.lnk + "'>" + i.nam + "</a></h5>" +
                          "<p>" + i.des + "</p>";
            var marker = L.marker([ i.lat, i.lon ], { icon: icon }).bindPopup( message ).addTo(map);
        });
    }, function(error){
        console.log(error);
    });

});
