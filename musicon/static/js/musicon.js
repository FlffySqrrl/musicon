// Map location
var LAT = 49.25;
var LNG = -123.13;

// Global variables
var mapEvents = [];
var mapVenues = [];

$(document).ready(function() {

    $('[data-toggle="tooltip"]').tooltip();

    // -------------------------------------------------------------------------
    // MAP FUNCTIONS
    // -------------------------------------------------------------------------

    if ($("#map").is(":visible")) {

        // Adjust zoom levels here.
        var INITIAL_ZOOM = 12;
        var CLICKED_ZOOM = 14;

        // Initialize the map.
        var map;
        var mapMarkers = [];
        var infoWindow = new google.maps.InfoWindow({
            pixelOffset : new google.maps.Size(0, -25)
        });
        google.maps.event.addDomListener(window, "load", initialize(LAT, LNG));

        // Plots the map every time the page is loaded.
        function initialize(lat, lng) {
            var mapSettings = {
                zoom      : INITIAL_ZOOM,
                center    : new google.maps.LatLng(lat, lng),
                mapTypeId : google.maps.MapTypeId.ROADMAP
            };
            map = new google.maps.Map(document.getElementById("map"), mapSettings);

            getEvents();
            getVenues();
            createMarkers();
            mapEvents.length = 0;
            mapVenues.length = 0;
        }

        // Puts markers on the map.
        function createMarkers() {
            for (var i = 0; i < mapEvents.length; ++i) {
                var lat = mapVenues[i][1];
                var lng = mapVenues[i][2];
                var thisMarker = new google.maps.Marker({
                    map       : map,
                    title     : mapEvents[i][0],
                    position  : new google.maps.LatLng(lat, lng),
                    animation : google.maps.Animation.DROP
                });
                mapMarkers.push(thisMarker);
                setClickEvent(thisMarker);
            }
        }

        // Checks whether or not infoWindow is enabled.
        function isInfoWindowOpen(infoWindow) {
            var map = infoWindow.getMap();
            return (map !== null && typeof map !== "undefined");
        }

        // Enables infoWindow when a marker is clicked on.
        function initializeInfoWindow(eventName, eventLoc) {
            if (isInfoWindowOpen(infoWindow)) {
                infoWindow.close();
            }
            infoWindow.setContent("<b>" + eventName + "</b>");
            infoWindow.setPosition(eventLoc);
            infoWindow.open(map);
        }

        // Zooms the map in to where the marker is.
        // Displays event_name in event_form.
        // Displays lat and lng in venue_form.
        function setClickEvent(marker) {
            google.maps.event.addListener(marker, "click", function() {
                var markerTitle = marker.getTitle().replace("&#39;", "'");
                var markerPosition = marker.getPosition();

                map.setCenter(markerPosition);
                map.setZoom(CLICKED_ZOOM);
                initializeInfoWindow(markerTitle, marker.position);

                // document.getElementById("id_lat").value = markerPosition.lat();
                // document.getElementById("id_lng").value = markerPosition.lng();
                // document.getElementById("id_event_name").value = markerTitle;
            });
        }
    }
});
