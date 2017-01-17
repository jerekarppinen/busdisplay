<?php

if(isset($_GET['id'])) {
	$id = $_GET['id'];
}

$client = new SoapClient("http://omatlahdot.hkl.fi/interfaces/kamo?wsdl");

$times = array();

$i = 10;

// $id = "1491123";

$nextDepartures = $client->getNextDepartures($id);

foreach($nextDepartures as $departure) {

	$destination = $departure->dest;
	$line = $departure->line;
	$stopName = $departure->stopname;
	$time = $departure->time;

	$timeStrippedSeconds = substr($time, 0, -3);

	$time = $timeStrippedSeconds;

	$times[$i] = array("line" => $line, "time" => $time);

	$i++;

}

$wrapper = array();

$wrapper['stopname'] = $stopName;
$wrapper['destination'] = $destination;
$wrapper['departures'] = $times;

echo(json_encode($wrapper));

?>