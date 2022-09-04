with
  key := <str>$key,
  value := <str>$value,
insert redis::Data {
  key := key,
  value := value,
}
unless conflict on .key
else (
  update redis::Data set {
    value := value,
  }
)
