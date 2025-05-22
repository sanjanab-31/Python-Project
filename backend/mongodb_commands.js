// Switch to our database
use rainwater_harvester

// Show all collections
show collections

// View all user inputs
db.user_inputs.find().pretty()

// View all historical data
db.historical_data.find().pretty()

// View user settings
db.user_settings.find().pretty()

// Find specific data (example: all entries from Coimbatore)
db.historical_data.find({ "location": "Coimbatore" }).pretty()

// Count documents in each collection
print("\nDocument counts:")
print("User Inputs:", db.user_inputs.count())
print("Historical Data:", db.historical_data.count())
print("User Settings:", db.user_settings.count())

// Find recent entries (last 5)
print("\nRecent Historical Data:")
db.historical_data.find().sort({"timestamp": -1}).limit(5).pretty()

// Find entries with specific conditions
print("\nEntries with tank capacity > 1000:")
db.historical_data.find({"tankCapacity": {$gt: 1000}}).pretty()

// Find leaking tanks
print("\nLeaking tanks:")
db.historical_data.find({"isLeaking": true}).pretty()

// Update example (update tank capacity)
// db.user_settings.updateOne(
//     { "_id": "default" },
//     { $set: { "defaultTankCapacity": 2000 } }
// )

// Delete example (remove old entries)
// db.historical_data.deleteMany({
//     "timestamp": { 
//         $lt: new Date(new Date().setDate(new Date().getDate() - 30))
//     }
// })
