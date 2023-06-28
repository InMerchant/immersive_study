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

// csv 파일 경로
$csvFile = "C:/Users/303-02/불만제로/review.csv";

//기존 데이터 삭제
$sqlDelete = "DELETE FROM review";
$conn->query($sqlDelete);

// csv 파일 읽기
$handle = fopen($csvFile, 'r');
if ($handle !== false) {
    //첫 번째 줄은 헤더로 처리
    fgetcsv($handle);

    //데이터 읽기
    while (($data = fgetcsv($handle)) !== false) {
        // 데이터 분리
        $rowData = str_replace(array('(', ')'), '', $data[0]);
        $rowData = explode(',', $rowData);
        $review = $conn->real_escape_string($rowData[0]); // 단어 (작은따옴표 이스케이프 처리)
        $tags = (int) $rowData[1]; // 빈도 수

        //데이터 저장
        $sql = "INSERT INTO review (review, tags) VALUES ('{$review}', '{$tags}')";
        $conn->query($sql);
    }

    fclose($handle);
    echo "CSV 파일이 성공적으로 데이터베이스에 저장되었습니다.";
} 
else {
    echo "CSV 파일을 열 수 없습니다.";
}

// 연결 종료
$conn->close();
?>