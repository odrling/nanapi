CREATE MIGRATION m1xd2figtmwahmf7rrxig5wqvnnqcfiwrhlvhqdv3wvspxnaan43fa
    ONTO m1pktunukfzyaa7uvhkjvxiezzmfylnwiv6xbaoyvbf3cpfktjrcdq
{
  ALTER TYPE anilist::Character {
      ALTER PROPERTY rank {
          USING ((waicolle::Rank.S IF (.favourites >= 3000) ELSE (waicolle::Rank.A IF (.favourites >= 1000) ELSE (waicolle::Rank.B IF (.favourites >= 200) ELSE (waicolle::Rank.C IF (.favourites >= 20) ELSE (waicolle::Rank.D IF (.favourites >= 1) ELSE waicolle::Rank.E))))));
      };
  };
  ALTER SCALAR TYPE waicolle::Rank EXTENDING enum<S, A, B, C, D, E>;
};
