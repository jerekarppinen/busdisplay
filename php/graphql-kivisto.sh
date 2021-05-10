{
  station(id: "HSL:4000211") {
    gtfsId
    name
    zoneId
    stoptimesWithoutPatterns {
      headsign
      scheduledArrival
      realtimeArrival
      realtime
      serviceDay
      trip {
        route {shortName}
      }
    }
  }
}