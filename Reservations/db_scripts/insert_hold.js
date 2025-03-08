// MongoDB Playground
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.

// The current database to use.
use('sample_mflix');

// Create a new document in the collection.
db.getCollection('reservations').insertOne({
    "reservation_id": "64a1e8c9f1a2bce47d85e006",  
    "user_email": "mansijpatel321@gmail.com",
    "book_id": "BOOK-1234",
    "reservation_date": new Date("2025-03-10T10:00:00Z"),  // Date object for reservation date
    "expiration_date": new Date("2025-03-15T10:00:00Z"),  // Date object for expiration date
    "status": "pending",
    "user_id": "6787541dea7503b89fa5cb1c", 
    "isbn": "11111LBXRN"
});



  
