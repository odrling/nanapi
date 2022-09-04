with
  id := <uuid>$id,
  answer := <optional str>$answer,
  answer_source := <optional str>$answer_source,
update quizz::Quizz
filter .id = id
set {
  answer := answer,
  answer_source := answer_source,
}
