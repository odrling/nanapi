with
  code := <str>$code,
  coupon := (
    insert waicolle::Coupon {
      client := global client,
      code := code,
    }
  ),
select coupon { code }
