db.getCollection('games').aggregate([{$out: {db: "sbp-v2", coll: "streams"}]);

db.getCollection('streams').aggregate([
    {$group: {_id: {stream_id: "$stream_id", 
                    game: "$game", 
                    broadcaster: {_id: "$broadcaster.id", name: "$broadcaster.name", created: "$broadcaster.created"}}}},
    {$project: {_id: {game: "$_id.game.name", stream_id: "$_id.stream_id"}},
    {$group: {_id: "_id", count: {$sum: 1}}},
    {$match: {"count": {$gt: 1}}}
    ], {allowDiskUse: true})

db.getCollection('streams').aggregate([
    {$group: {_id: {stream_id: "$stream_id", 
                    game: "$game", 
                    broadcaster: {_id: "$broadcaster.id", name: "$broadcaster.name", created: "$broadcaster.created"}}, 
              details: {$push: {timestamp: "$timestamp", 
                                current_views: "$current_views", 
                                broadcaster_details: {
                                        follower_number: "$broadcaster.follower_number",
                                        total_views: "$broadcaster.total_views"}}},
              start_time: {$min: "$timestamp"}, 
              end_time: {$max: "$timestamp"},
              max_views: {$max: "$current_views"},
              min_views: {$min: "$current_views"},
              view_sum: {$sum: "$current_views"},
              timestamp_count: {$sum: 1}
              }},
    {$project: {_id: {game: "$_id.game.name", stream_id: "$_id.stream_id"},
                game: "$_id.game",
                stream_id: "$_id.stream_id",
                broadcaster: "$_id.broadcaster",
                details: 1,
                start_time: 1,
                end_time: 1,
                duration_in_minutes: {$divide: [{$subtract: ["$end_time", "$start_time"]}, 60000]},
                max_views: 1,
                min_views: 1,
                view_sum: 1,
                timestamp_count: 1}},
    {$out: {db: "sbp-v2", coll: "streams"}}
], {allowDiskUse: true});


db.getCollection('streams').aggregate([
    {$sort: {"timestamp": 1}},
    {$group: {_id: {name: "$broadcaster.name", id: "$broadcaster.id", created: "$broadcaster.created"}, 
              details: {$push: {
                        follower_number: "$broadcaster.follower_number",
                        total_views: "$broadcaster.total_views",
                        timestamp: "$timestamp",
                        partner: "$broadcaster.partner"}}
              }},
    {$project: {_id: {id: "$_id.id", name: "$_id.name"}, name: "$_id.name", created: "$_id.created", details: 1}},
    {$out: {db: "sbp-v2", coll: "broadcasters"}}
], {allowDiskUse: true})


db.getCollection('streams').aggregate([
    {$group: {_id: {game: "$game.name", game_id: "$game._id", genres: "$game.genres", timestamp: "$timestamp"}, 
              total_views: {$sum: "$current_views"},
              total_streams: {$sum: 1}}},
    {$project: {_id: {game: "$_id.game", timestamp: "$_id.timestamp"},
                game: {name: "$_id.game", _id: "$_id.game_id", genres: "$_id.genres"},
                timestamp: "$_id.timestamp",
                total_views: 1,
                total_streams: 1}},
    {$out: {db: "sbp-v2", coll: "games-per-time"}}
    ], {allowDiskUse: true});
