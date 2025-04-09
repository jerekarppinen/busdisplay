curl https://api.digitransit.fi/routing/v2/hsl/gtfs/v1 \
-H "Content-Type: application/graphql" \
-H "digitransit-subscription-key: xxx" \
-d @- << DATA
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
DATA
