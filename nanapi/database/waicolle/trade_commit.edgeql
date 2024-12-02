with
  id := <uuid>$id,
update waicolle::TradeOperation
filter .id = id
and not exists .completed_at
set {
  completed_at := datetime_current(),
}
