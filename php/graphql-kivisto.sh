curl https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql \
-H "Content-Type: application/graphql" \
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
