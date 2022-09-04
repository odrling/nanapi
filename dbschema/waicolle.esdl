module waicolle {
  scalar type Rank extending enum<S, A, B, C, D, E>;

  scalar type GameMode extending enum<WAIFU, HUSBANDO, ALL>;

  abstract type Trackable {}

  type Player extending default::ClientObject {
    required property game_mode -> GameMode;
    required property moecoins -> int32 {
      constraint min_value(0);
      default := 0;
    }
    required property blood_shards -> int32 {
      constraint min_value(0);
      default := 0;
    }
    required link user -> user::User {
      on target delete delete source;
    }
    multi link tracked_items -> Trackable {
      on target delete allow;
    }
    multi link tracked_collections -> Collection {
      on target delete allow;
    }
    multi link tracked_characters := (
      .tracked_items[is anilist::Media].character_edges.character union
      .tracked_items[is anilist::Staff].character_edges.character union
      .tracked_collections.characters
    );
    multi link waifus := .<owner[is Waifu];
    constraint exclusive on ((.client, .user));
  }

  scalar type CollagePosition extending enum<DEFAULT, LEFT_OF, RIGHT_OF>;

  type Waifu extending default::ClientObject {
    required property timestamp -> datetime {
      default := datetime_current();
    }
    required property level -> int32 {
      default := 0;
    }
    required property locked -> bool {
      default := false;
    }
    required property blooded -> bool {
      default := false;
    }
    required property nanaed -> bool {
      default := false;
    }
    property custom_image -> str;
    property custom_name -> str;
    required property custom_collage -> bool {
      default := false;
    }
    required property custom_position -> CollagePosition {
      default := CollagePosition.DEFAULT;
    }
    required link character -> anilist::Character {
      on target delete delete source;
    }
    required link owner -> Player {
      on target delete delete source;
    }
    link original_owner -> Player {
      on target delete allow;
    }
    link custom_position_waifu -> Waifu {
      on target delete allow;
    }
    property trade_locked := exists .<waifus_a[is Trade] or exists .<waifus_b[is Trade];
  }

  type Collection extending default::ClientObject {
    required property name -> str;
    required link author -> Player {
      on target delete delete source;
    }
    multi link items -> Trackable {
      on target delete allow;
    }
    multi link characters := (
      .items[is anilist::Media].character_edges.character union
      .items[is anilist::Staff].character_edges.character
    );
    constraint exclusive on ((.name, .author));
  }

  type Trade extending default::ClientObject {
    required link player_a -> Player {
      on target delete delete source;
    }
    multi link waifus_a -> Waifu {
      on target delete delete source;
    }
    required property moecoins_a -> int32 {
      default := 0;
    }
    required property blood_shards_a -> int32 {
      default := 0;
    }
    required link player_b -> Player {
      on target delete delete source;
    }
    multi link waifus_b -> Waifu {
      on target delete delete source;
    }
    required property moecoins_b -> int32 {
      default := 0;
    }
    required property blood_shards_b -> int32 {
      default := 0;
    }
  }

  type Coupon extending default::ClientObject {
    required property code -> str;
    multi link claimed_by -> Player {
      on target delete allow;
    }
    constraint exclusive on ((.client, .code));
    index on (.code);
  }
}
