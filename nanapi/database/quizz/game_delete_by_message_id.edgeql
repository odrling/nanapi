with
  message_id := <int64>$message_id
delete quizz::Game
filter .message_id = message_id
