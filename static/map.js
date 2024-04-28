function initMap() {
  // Create a new map centered on the user's location
  var map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 0, lng: 0 },
    zoom: 8,
  });

  // Try to get the user's location
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function (position) {
      // If the user's location is successfully retrieved, center the map on it
      var pos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude,
      };
      map.setCenter(pos);

      // Add a marker for the user's location
      var userMarker = new google.maps.Marker({
        position: pos,
        map: map,
        title: "Your location",
      });

      // Find nearby hospitals using the Google Places API
      var request = {
        location: pos,
        radius: "5000",
        type: ["hospital"],
      };
      var service = new google.maps.places.PlacesService(map);
      service.nearbySearch(request, function (results, status) {
        if (status == google.maps.places.PlacesServiceStatus.OK) {
          // Limit the number of hospitals to 10
          var numHospitals = Math.min(results.length, 10);

          // Add markers for each of the nearby hospitals
          for (var i = 0; i < numHospitals; i++) {
            var hospitalMarker = new google.maps.Marker({
              position: results[i].geometry.location,
              map: map,
              title: results[i].name,
            });
          }
        }
      });
    });
  }
}
