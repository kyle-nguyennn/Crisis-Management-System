/**
 * Created by NghiaNguyen on 4/1/2017.
 */
// $.get(
//     "https://api.data.gov.sg/v1/environment/psi",
//     {'api-key' : 'ZGT0v1m1vG3Jj5yhLRH0Zz9Awh6TviEd'},
//     function(data) {
//         $('#psi').text(data[0][0]);
//     },
//     json
// );

function setViewApi(data){
    console.log('hello');
    document.getElementById("psi").innerHTML = '<p>Currently dragging marker...</p>';
}