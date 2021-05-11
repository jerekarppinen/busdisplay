<?php
declare(strict_types=1);
date_default_timezone_set("Europe/Helsinki");

$json = exec('sh graphql-kivisto.sh');

$array = json_decode($json, true);

$station = $array['data']['station']['name'];
$zone = $array['data']['station']['zoneId'];

$stopTimes = $array['data']['station']['stoptimesWithoutPatterns'];

$times = [];

foreach($stopTimes as $stopTime) {
	$realtimeArrival = $stopTime['realtimeArrival'];
	$scheduledArrival = $stopTime['scheduledArrival'];

	$arrival = $scheduledArrival;

	$headsign = $stopTime['headsign'];
	$train = $stopTime['trip']['route']['shortName'];

	if ($stopTime['realtime'] === true) {
		$arrival = $realtimeArrival;
	}

	$times[] = ['line' => $train, 'time' => date("H:i", $serviceDay + $arrival), 'destination' => $headsign];
}


$wrapper = [];
$wrapper['stopname'] = $station;
$wrapper['departures'] = $times;

echo json_encode($wrapper);
