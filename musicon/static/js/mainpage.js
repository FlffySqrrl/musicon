$(function() {

    // Arrays we use to add data from our database.
    Events = [];
    Venues = [];
    Artists = [];
    markers = [];

    // Set initial map.
    var map;
    var infoWindow = new google.maps.InfoWindow({
                    pixelOffset: new google.maps.Size(10,-25)
                 });

    google.maps.event.addDomListener(window, 'load', initialize(49.25, -123.133333));

    // Plot the map every time the page is loaded.
    function initialize(lat, lng) {
        var latlng = new google.maps.LatLng(lat, lng);
        var mapSettings = {
            center: latlng,
            zoom: 10,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        }
        map = new google.maps.Map(document.getElementById("googleMap"),mapSettings);

        getEvents(Events);
        getVenues(Venues);
        getArtists(Artists);

        createMarkers();

        Events.length = 0;
        Venues.length = 0;
        Artists.length = 0;
    }

    // Create markers on the map.
    function createMarkers() {
        for (var i = 0; i < Events.length; i++) {
            var lat  = Venues[i][1];
            var lng = Venues[i][2];
            var latlng = new google.maps.LatLng(lat, lng);
            var marker;

            marker = new google.maps.Marker( {
                        position: latlng,
                        map: map,
                        title: Events[i][0],
                        animation: google.maps.Animation.DROP
            });
            markers.push(marker);
            clickEvent(marker);
            }
    }

    // Check whether info pop-up is open or not.
    function isInfoWindowOpen(infoWindow){
        var map = infoWindow.getMap();
        return (map !== null && typeof map !== "undefined");
    }

    // Enables info window when a point on the map is clicked on.
    function initializeInfoWindow(name, eventPosition) {
        if (isInfoWindowOpen(infoWindow)){
            infoWindow.close();
        }
        infoWindow = new google.maps.InfoWindow({
                        pixelOffset: new google.maps.Size(10,-25)
                     });
        infoWindow.setContent(name);
        infoWindow.setPosition(eventPosition)
        infoWindow.open(map);
    }

    // When a point is clicked, the map is zoomed in and the lat and lon
    // of the venue and the name of the event is shown on the input boxes
    // to help adding fav_event and fav_venue.
    function clickEvent(marker) {
    google.maps.event.addListener(marker, 'click', function() {
        var markerPosition = marker.getPosition();
        map.setCenter(markerPosition);
        map.setZoom(13);
        var contentString = marker.getTitle();

        initializeInfoWindow(contentString, marker.position);

        document.getElementById("id_lat").value = markerPosition.lat();
        document.getElementById("id_lon").value = markerPosition.lng();
        document.getElementById("id_eName").value = contentString;
        });
    }
});
