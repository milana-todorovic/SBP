db.getCollection('streams').aggregate([
    {$group: {_id: {broadcaster_id: "$broadcaster._id", broadcaster_name: "$broadcaster.name", game: "$game.name", game_id: "$game._id", genres: "$game.genres"}, 
                number_of_streams: {$sum: 1},
                total_duration_in_minutes: {$sum: "$duration_in_minutes"}}},
    {$project: {_id: {game: "$_id.game", broadcaster: "$_id.broadcaster_name"}, 
                game: {name: "$_id.game", _id: "$_id.game_id", genres: "$_id.genres"}, 
                number_of_streams: 1, total_duration_in_minutes: 1,
                broadcaster: {name: "$_id.broadcaster_name", _id: "$_id.broadcaster_id"}}},
    {$out: {db: "sbp-v2", coll: "games-broadcasters"}}
], {allowDiskUse: true});