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
	$busNumber =  $departure->code;
	if(strlen($time) == 4) {
		$time = substr_replace($time, ":", 2, 0);
	}
	else {
		$time = "0".$time;
		$time = substr_replace($time, ":", 2, 0);
	}

	$times[$time] = $date . " (" . substr($busNumber, 2, 2) . ")";
}

echo(json_encode($times));

?>