var mapContainer = document.getElementById('map'), // 지도를 표시할 div
    mapOption = {
        center: new kakao.maps.LatLng(37.56068711851083, 126.9935363820278), // 지도의 중심좌표
        level: 1 // 지도의 확대 레벨
    };

var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다

// 마커를 표시할 위치와 내용을 가지고 있는 객체 배열입니다
var positions = [
    {
        content: '<div id="warn_syntest1" class="safe"><span class="left"></span><span class="center">syntest1</span><span class="right"></span></div>',
        latlng: new kakao.maps.LatLng(37.56068711851083, 126.9935363820278)
    }
    ]

for (var i = 0; i < positions.length; i ++) { /*
    // 마커를 생성합니다
    var marker = new kakao.maps.Marker({
        map: map, // 마커를 표시할 지도
        position: positions[i].latlng// 마커의 위치

    });

    // 마커에 표시할 인포윈도우를 생성합니다 */
    var customOverlay = new kakao.maps.CustomOverlay({
        content: positions[i].content, // 인포윈도우에 표시할 내용
        position: positions[i].latlng
    });
    customOverlay.setMap(map);
}

