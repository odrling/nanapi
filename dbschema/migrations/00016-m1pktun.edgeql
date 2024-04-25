CREATE MIGRATION m1pktunukfzyaa7uvhkjvxiezzmfylnwiv6xbaoyvbf3cpfktjrcdq
    ONTO m1egut3amvxd5hvetdj23jcjkyqkscwbrhcb3e7p6jjufw3xr47d7a
{
  CREATE ABSTRACT TYPE waicolle::Trackable;
  ALTER TYPE anilist::Media EXTENDING waicolle::Trackable LAST;
  ALTER TYPE anilist::Staff EXTENDING waicolle::Trackable LAST;
  ALTER TYPE waicolle::Collection {
      ALTER LINK medias {
          RENAME TO items;
      };
  };
  ALTER TYPE waicolle::Collection {
      ALTER LINK items {
          SET TYPE waicolle::Trackable;
      };
      CREATE MULTI LINK characters := ((.items[IS anilist::Media].character_edges.character UNION .items[IS anilist::Staff].character_edges.character));
  };
  ALTER TYPE waicolle::Player {
      ALTER LINK tracked_medias {
          RENAME TO tracked_items;
      };
  };
  ALTER TYPE waicolle::Player {
      ALTER LINK tracked_items {
          SET TYPE waicolle::Trackable;
      };
      CREATE MULTI LINK tracked_characters := (((.tracked_items[IS anilist::Media].character_edges.character UNION .tracked_items[IS anilist::Staff].character_edges.character) UNION .tracked_collections.characters));
  };
};
