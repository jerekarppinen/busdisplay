<?php
include("globals.php");
$url = "http://api.reittiopas.fi/hsl/prod/?request=stop&code=1491123&user=" . $user . "&pass=" . $pass;
$response = json_decode(file_get_contents($url));
$departures = $response[0]->departures;
$times = array();
foreach($departures as $departure) {
	//$date = $departure->date;
	$time = (string) $departure->time;
	$date = (string) $departure->date;
	$busNumber =  substr($departure->code, 2, 3);
	$busNumber = trim($busNumber);
	$busNumber = "(" . $busNumber . ")";

	$hour = intval(substr($time, 0, 2));

	$year = substr($date, 0, 4);
	$month = substr($date, 4, 2);
	$day = substr($date, 6, 2);

	if($hour > 23) {
		$day = intval($day);
		$day++;
		$day = (string) $day;
		$day = "0" . $day;
	}

	$date = $year . $month . $day;

	if(strlen($time) == 4) {
			$time = substr_replace($time, ":", 2, 0);
		}
	else {
			$time = "0".$time;
			$time = substr_replace($time, ":", 2, 0);
		}

	$times[$departure->time] = array("time" => $time, "date" => $date, "bus" => $busNumber);

}
echo(json_encode($times));
?>