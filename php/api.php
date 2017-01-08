<?php

$client = new SoapClient("http://omatlahdot.hkl.fi/interfaces/kamo?wsdl");

$times = array();

foreach($client->getNextDepartures('1491123') as $departure) {

	$destination = $departure->dest;
	$line = $departure->line;
	$stopName = $departure->stopname;
	$time = $departure->time;

	$timeStrippedSeconds = substr($time, 0, -3);

	$time = $timeStrippedSeconds;

	$timeWithoutChars = str_replace(":", "", $time);
	$timeAsInteger = intval($timeWithoutChars);

	$times[$timeAsInteger] = array("line" => $line, "time" => $time);

}

$wrapper = array();

$wrapper['stopname'] = $stopName;
$wrapper['destination'] = $destination;
$wrapper['departures'] = $times;

echo(json_encode($wrapper));



?>