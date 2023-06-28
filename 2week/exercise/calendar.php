<!DOCTYPE html>
<html>
<head>
    <title>운동 기록 캘린더</title>
    <meta charset="UTF-8">
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
            max-width: 800px;
            margin: 0 auto;
        }

        table td {
            border: 1px solid black;
            padding: 5px;
            cursor: pointer;
            text-align: center;
            vertical-align: middle;
        }

        table td.today {
            background-color: lightblue;
        }

        table td.has-record {
            background-color: lightgreen;
        }

        .exercise-details {
            display: none;
        }
    </style>
</head>
<body>
    <h1>운동 기록 캘린더</h1>

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

    // 현재 연도와 월 가져오기
    $currentYear = isset($_GET['year']) ? $_GET['year'] : date("Y");
    $currentMonth = isset($_GET['month']) ? $_GET['month'] : date("m");

    // 현재 월의 첫 날과 마지막 날 계산
    $firstDayOfMonth = date("Y-m-01", strtotime($currentYear . "-" . $currentMonth));
    $lastDayOfMonth = date("Y-m-t", strtotime($currentYear . "-" . $currentMonth));

    // 이전 월과 다음 월 계산
    $previousMonth = date("m", strtotime("-1 month", strtotime($firstDayOfMonth)));
    $nextMonth = date("m", strtotime("+1 month", strtotime($lastDayOfMonth)));

    // 이전 월과 다음 월로 이동하는 링크 생성
    $previousLink = "calendar.php?year=" . ($previousMonth == "12" ? ($currentYear - 1) : $currentYear) . "&month=" . $previousMonth;
    $nextLink = "calendar.php?year=" . ($nextMonth == "01" ? ($currentYear + 1) : $currentYear) . "&month=" . $nextMonth;

    // 현재 월 이름 표시
    echo "<h2>" . date("F Y", strtotime($firstDayOfMonth)) . "</h2>";

    // 이전 월과 다음 월로 이동하는 링크 표시
    echo "<a href=\"$previousLink\">이전 달</a> | <a href=\"$nextLink\">다음 달</a>";
    echo "<br><br>";

    // 캘린더 테이블 생성
    echo "<table>";
    echo "<tr>";
    echo "<th>일</th>";
    echo "<th>월</th>";
    echo "<th>화</th>";
    echo "<th>수</th>";
    echo "<th>목</th>";
    echo "<th>금</th>";
    echo "<th>토</th>";
    echo "</tr>";

    // 첫 주의 첫 번째 요일 계산
    $firstDayOfWeek = date("w", strtotime($firstDayOfMonth));

    // 첫 주의 빈 칸 생성
    echo "<tr>";
    for ($i = 0; $i < $firstDayOfWeek; $i++) {
        echo "<td></td>";
    }

    // 해당 월의 날짜 표시
    $currentDay = 1;
    $totalDaysOfMonth = date("t", strtotime($firstDayOfMonth));
    while ($currentDay <= $totalDaysOfMonth) {
        // 현재 날짜에 해당하는 운동 기록 가져오기
        $sql = "SELECT exercise_name FROM exercise_records WHERE exercise_date = '$currentYear-$currentMonth-$currentDay'";
        $result = $conn->query($sql);

        $isToday = date("Y-m-d") === "$currentYear-$currentMonth-$currentDay";
        $hasExerciseRecord = $result && $result->num_rows > 0;

        echo "<td" . ($isToday ? " class=\"today\"" : "") . ($hasExerciseRecord ? " class=\"has-record\"" : "") . ">";
        echo "<strong>$currentDay</strong>";

        if ($hasExerciseRecord) {
            echo "<div class=\"exercise-details\">";
            while ($row = $result->fetch_assoc()) {
                echo $row["exercise_name"] . "<br>";
            }
            echo "</div>";
        }

        echo "</td>";

        // 다음 날로 이동
        $currentDay++;
        $firstDayOfWeek++;
        if ($firstDayOfWeek == 7) {
            // 한 주가 끝나면 다음 줄로 이동
            echo "</tr><tr>";
            $firstDayOfWeek = 0;
        }
    }

    // 마지막 주의 나머지 빈 칸 생성
    while ($firstDayOfWeek < 7) {
        echo "<td></td>";
        $firstDayOfWeek++;
    }

    echo "</tr>";
    echo "</table>";

    // 데이터베이스 연결 종료
    $conn->close();
    ?>

    <script>
        // 운동 기록이 있는 날짜 클릭 시, 운동 기록을 보여주는 기능
        const exerciseCells = document.querySelectorAll('td.has-record');

        exerciseCells.forEach(cell => {
            cell.addEventListener('click', () => {
                const exerciseDetails = cell.querySelector('.exercise-details');
                exerciseDetails.style.display = exerciseDetails.style.display === 'none' ? 'block' : 'none';
            });
        });
    </script>
    <br><br>
    <button onclick="navigateToExercise()">운동 기록 입력 페이지로 이동</button>
    <script>
        function navigateToExercise() {
            // 운동 기록 입력 페이지로 이동
            window.location.href = "exercise.html";
        }
    </script>
</body>
</html>
