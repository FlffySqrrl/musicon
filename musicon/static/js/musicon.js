var cities = {
    "vancouver" : {
        "lat" : 49.25,
        "lng" : -123.13,
    },
};

// Map location
var LAT = cities["vancouver"]["lat"];
var LNG = cities["vancouver"]["lng"];

// Global variables
var mapEvents = [];
var mapVenues = [];

$(document).ready(function() {

    // Enable tooltips.
    $("[data-toggle='tooltip']").tooltip();

    // -------------------------------------------------------------------------
    // SEARCH FORM
    // -------------------------------------------------------------------------

    // Convert the dropdown menu into a select element.
    $("#by-menu-dropdown li a").click(function() {
        $("#by-menu-label").html($(this).html());
        $("#by-menu-select option").prop("selected", false)
                                   .filter("[value=" + $(this).attr("value") + "]")
                                   .prop("selected", true);
    });

    // Animate the search field.
    $("#search-field").focus(function() {
        $(this).attr("default-width", $(this).css("width"));
        $(this).animate({ width : 150 }, "fast");
    }).blur(function() {
        var defaultWidth = $(this).attr("default-width");
        $(this).animate({ width : defaultWidth }, "fast");
    });

    // Submit the search form on enter.
    $("#search-field").keydown(function(e) {
        if (e.keyCode == 13) {
            e.preventDefault();
            $("#search-form").submit();
        }
    });

    // -------------------------------------------------------------------------
    // MAP
    // -------------------------------------------------------------------------

    // Check to prevent error message.
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
        google.maps.event.addDomListener(window, "load", initMap(LAT, LNG));

        /**
         * Plots the map every time the page is loaded.
         */
        function initMap(lat, lng) {
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

        /**
         * Puts markers on the map.
         */
        function createMarkers() {
            for (var i = 0; i < mapEvents.length; ++i) {
                var lat = mapVenues[i][1];
                var lng = mapVenues[i][2];

                var content = "<div>" + mapEvents[i]["date"];
                if (mapEvents[i]["time"]) {
                    content += " " + mapEvents[i]["time"];
                }
                if (mapEvents[i]["venue"]) {
                    content += " at " + mapEvents[i]["venue"];
                }
                content += "</div>";
                if (mapEvents[i]["type"] === "Festival") {
                    content += "<div><strong class='songkick-pink'>";
                } else {
                    content += "<div><strong>";
                }
                content += mapEvents[i]["lineup"][0] + "</strong></div>";
                for (var j = 1; j < mapEvents[i]["lineup"].length; ++j) {
                    content += "<div>" + mapEvents[i]["lineup"][j] + "</div>";
                }

                var thisMarker = new google.maps.Marker({
                    map       : map,
                    content   : content,
                    position  : new google.maps.LatLng(lat, lng),
                    animation : google.maps.Animation.DROP
                });
                mapMarkers.push(thisMarker);
                setClickEvent(thisMarker);
            }
        }

        /**
         * Zooms the map in to where the marker is.
         * Displays event_name in event_form.
         * Displays lat and lng in venue_form.
         */
        function setClickEvent(marker) {
            google.maps.event.addListener(marker, "click", function() {
                var markerContent = marker.content.replace("&#39;", "'");
                var markerPosition = marker.getPosition();

                map.setCenter(markerPosition);
                map.setZoom(CLICKED_ZOOM);
                initInfoWindow(markerContent, markerPosition);

                // document.getElementById("id_lat").value = markerPosition.lat();
                // document.getElementById("id_lng").value = markerPosition.lng();
                // document.getElementById("id_event_name").value = markerTitle;
            });
        }

        /**
         * Checks whether or not infoWindow is enabled.
         */
        function isInfoWindowOpen(infoWindow) {
            var map = infoWindow.getMap();
            return (map !== null && typeof map !== "undefined");
        }

        /**
         * Enables infoWindow when a marker is clicked on.
         */
        function initInfoWindow(markerContent, markerPosition) {
            if (isInfoWindowOpen(infoWindow)) {
                infoWindow.close();
            }
            infoWindow.setContent(markerContent);
            infoWindow.setPosition(markerPosition);
            infoWindow.open(map);
        }
    }
});
