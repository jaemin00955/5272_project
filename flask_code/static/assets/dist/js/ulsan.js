var mapContainer = document.getElementById('map'), // 지도를 표시할 div
    mapOption = {
        center: new kakao.maps.LatLng(35.31520807223912, 129.26284224108414), // 지도의 중심좌표
        level: 1 // 지도의 확대 레벨
    };

var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다

// 마커를 표시할 위치와 내용을 가지고 있는 객체 배열입니다
var positions = [
    {
        content: '<div id="warn_2214" ><span class="left"></span><span class="center">2214</span><span class="right"></span></div>',
        latlng: new kakao.maps.LatLng(35.315337201900824, 129.2627027662117)
    },
    {
        content: '<div id="warn_2223" class="safe" ><span class="left"></span><span class="center">2223</span><span class="right"></span></div>',
        latlng: new kakao.maps.LatLng(35.31517086534916, 129.262775185857)
    },
    {
        content: '<div id="warn_2222" class="safe"><span class="left"></span><span class="center">2222</span><span class="right"></span></div>',
        latlng: new kakao.maps.LatLng(35.31497826470411, 129.26333576755584)
    },
    {
        content: '<div id="warn_2221" class="safe"><span class="left"></span><span class="center">2221</span><span class="right"></span></div>',
        latlng: new kakao.maps.LatLng(35.31489071880471, 129.26316947059254)
    }
];

for (var i = 0; i < positions.length; i ++) {
    // 마커를 생성합니다
 //   var marker = new kakao.maps.Marker({
  //      map: map, // 마커를 표시할 지도
  //      position: positions[i].latlng// 마커의 위치

   // });

    // 마커에 표시할 인포윈도우를 생성합니다
    var customOverlay = new kakao.maps.CustomOverlay({
        content: positions[i].content,
        position: positions[i].latlng// 인포윈도우에 표시할 내용

    });
    customOverlay.setMap(map);
}

var linePath = [
    new kakao.maps.LatLng(35.315337201900824, 129.2627027662117), //2214
    new kakao.maps.LatLng(35.31517086534916, 129.262775185857), //2222
    new kakao.maps.LatLng(35.31497826470411, 129.26333576755584), //2213
    new kakao.maps.LatLng(35.31489071880471, 129.26316947059254), //2221
    new kakao.maps.LatLng(35.31517086534916, 129.262775185857), //2222
    new kakao.maps.LatLng(35.315337201900824, 129.2627027662117),
    new kakao.maps.LatLng(35.31497826470411, 129.26333576755584),
    new kakao.maps.LatLng(35.31489071880471, 129.26316947059254),
    new kakao.maps.LatLng(35.315337201900824, 129.2627027662117)

];

// 지도에 표시할 선을 생성합니다
var polyline = new kakao.maps.Polyline({
    path: linePath, // 선을 구성하는 좌표배열 입니다
    strokeWeight: 3, // 선의 두께 입니다
    strokeColor: '#0fbd0f', // 선의 색깔입니다
    strokeOpacity: 0.4, // 선의 불투명도 입니다 1에서 0 사이의 값이며 0에 가까울수록 투명합니다
    strokeStyle: 'solid' // 선의 스타일입니다
});

// 지도에 선을 표시합니다
polyline.setMap(map);