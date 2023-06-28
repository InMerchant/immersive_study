<?php
$dbhost = 'localhost';
$dbuser = 'root';
$dbpass = '';
$dbname = 'review';

// 데이터베이스 연결
$conn = new mysqli($dbhost, $dbuser, $dbpass, $dbname);

// 연결 확인
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// 데이터 가져오기
$sql = "SELECT review, tags FROM review ORDER BY tags DESC LIMIT 10";
$result = $conn->query($sql);

// 데이터 배열 초기화
$data = array();
$data[] = ['Review', 'Tags'];

// 데이터 가져오기
if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $review = $row['review'];
        $tags = (int)$row['tags'];
        $data[] = [$review, $tags];
    }
}

// 연결 종료
$conn->close();

// PHP 배열을 JSON 형식으로 변환
$jsonData = json_encode($data);

// JSON 데이터 출력
echo $jsonData;
?>
