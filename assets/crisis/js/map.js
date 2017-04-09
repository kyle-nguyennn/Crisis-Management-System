/**
 * Created by NghiaNguyen on 3/31/2017.
 */
var map;
var myMarker;
function initMap() {
    var singapore = {lat: 1.3553794, lng: 103.8677444};
    map = new google.maps.Map(document.getElementById('map'), {
        center: singapore, //singapore
        zoom: 11
    });

    myMarker = new google.maps.Marker({
        position: singapore,
        map: map,
        draggable: true,
        animation: google.maps.Animation.DROP,
    });
    myMarker.addListener('click', toggleBounce);

    google.maps.event.addListener(myMarker, 'dragstart', function (evt) {
        console.log("Start dragging...")
    });
    google.maps.event.addListener(myMarker, 'dragend', function (evt) {
        $('#latitude').val(evt.latLng.lat().toFixed(7));
        $('#longitude').val(evt.latLng.lng().toFixed(7));
    });

}

function toggleBounce() {
    if (myMarker.getAnimation() != null) {
        myMarker.setAnimation(null);
    } else {
        myMarker.setAnimation(google.maps.Animation.BOUNCE);
    }
}
