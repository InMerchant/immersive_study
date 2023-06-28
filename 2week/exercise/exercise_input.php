<?php
// 데이터베이스 연결 설정
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "health";

// 데이터베이스 연결 생성
$conn = new mysqli($servername, $username, $password, $dbname);

// 연결 확인
if ($conn->connect_error) {
    die("데이터베이스 연결 실패: " . $conn->connect_error);
}

// POST 데이터 가져오기
$exercise_date = $_POST['exercise_date'];
$exercise_name = $_POST['exercise_name'];

// SQL 쿼리 작성
$sql = "INSERT INTO exercise_records (exercise_date, exercise_name) VALUES ('$exercise_date', '$exercise_name')";

// 쿼리 실행
if ($conn->query($sql) === TRUE) {
    // 운동 기록 저장 성공 시, 캘린더 페이지로 리다이렉션
    header("Location: calendar.php");
    exit();
} else {
    echo "운동 기록 저장 실패: " . $conn->error;
}

// 데이터베이스 연결 종료
$conn->close();
?>
