![alt text](image-1.png)
Top 5 frequently occurring comments
[
  { $group: { _id: "$replyContent", count: { $sum: 1 } } },
  { $sort: { count: -1 } },
  { $limit: 5 }
]
![alt text](image-6.png)
All entries where the “content” field is less than 5 characters long;
![alt text](image-4.png)
![alt text](image-3.png)
Average rating for each day (the result should be in timestamp type).
[
  {
    $match: {
      at: {
        $type: "date"
      }
    }
  },
  {
    $group:
      /**
       * _id: The id of the group.
       * fieldN: The first field name.
       */
      {
        _id: {
          $dateTrunc: {
            date: "$at",
            unit: "day"
          }
        },
        avg_rating: {
          $avg: "$score"
        }
      }
  },
  {
    $sort:
      /**
       * Provide any number of field/order pairs.
       */
      {
        _id: 1
      }
  }
]
![alt text](image-5.png)