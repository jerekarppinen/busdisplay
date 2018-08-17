<?php
declare(strict_types=1);
date_default_timezone_set('Europe/Helsinki');

$json = exec('sh graphql-yliskylantie.sh');

$array = json_decode($json, true);

$times = [];
$i = 10;

foreach($array as $item) {
	$stop = $item['stop'];
	$stoptimesWithoutPatterns = $item['stop']['stoptimesWithoutPatterns'];
	foreach($stoptimesWithoutPatterns as $st) {
		$realtimeArrival = $st['realtimeArrival'];
		$scheduledArrival = $st['scheduledArrival'];
		$arrival = $scheduledArrival;
		if ($st['realtime'] === true) {
			$arrival = $realtimeArrival;
		}

		$headsign = $st['headsign'];
		$serviceDay = $st['serviceDay'];

		$times[] = ['line' => '89', 'time' => date("H:i", $serviceDay + $arrival)];
	}
}

$wrapper = [];
$wrapper['stopname'] = 'Yliskylänkaari';
$wrapper['departures'] = $times;
$wrapper['destination'] = 'Herttoniemi';

echo json_encode($wrapper);
