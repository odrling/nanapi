with
  id := <uuid>$id,
  answer_bananed := <optional str>$answer_bananed,
update quizz::Game
filter .id = id
set {
  answer_bananed := answer_bananed,
}
