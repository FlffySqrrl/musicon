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
var mapEvents  = [];
var mapVenues  = [];
var mapMarkers = [];

$(document).ready(function() {

    // Enable tooltips.
    $("[data-toggle='tooltip']").tooltip();

    $("tr").click(function() {
        var eventId = $(this).attr("id");
        var marker = mapMarkers.reduce(function(a, b) {
            return (a["eventId"] === eventId && a) || (b["eventId"] === eventId && b);
        });
        new google.maps.event.trigger(marker, "click");
    });

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
        var infoWindow = new google.maps.InfoWindow({
            pixelOffset : new google.maps.Size(0, -25),
        });
        google.maps.event.addDomListener(window, "load", initMap(LAT, LNG));

        /**
         * Plots the map every time the page is loaded.
         */
        function initMap(lat, lng) {
            var mapSettings = {
                zoom      : INITIAL_ZOOM,
                center    : new google.maps.LatLng(lat, lng),
                mapTypeId : google.maps.MapTypeId.ROADMAP,
            };
            map = new google.maps.Map(document.getElementById("map"), mapSettings);

            mapEvents  = [];
            mapVenues  = [];
            mapMarkers = [];

            getEvents();
            getVenues();
            createMarkers();
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
                    animation : google.maps.Animation.DROP,
                    eventId   : mapEvents[i]["id"],
                });
                mapMarkers.push(thisMarker);
                setClickEvent(thisMarker);
            }
        }

        /**
         * Sets what happens when a marker is clicked on.
         */
        function setClickEvent(marker) {
            google.maps.event.addListener(marker, "click", function() {
                var markerContent = marker.content.replace("&#39;", "'");
                var markerPosition = marker.getPosition();

                // Zoom the map in to the marker.
                map.setCenter(markerPosition);
                map.setZoom(CLICKED_ZOOM);
                initInfoWindow(markerContent, markerPosition);

                // Scroll to and highlight corresponding row on the table.
                var eventRow = "#" + marker["eventId"];
                $("tbody").scrollTo(eventRow, { duration : 500 });
                $(eventRow).effect("highlight", { color : "#ff467a" }, 2000);

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
         * Enables infoWindow when a marker is clicked on and closes any
         * currently open ones.
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
