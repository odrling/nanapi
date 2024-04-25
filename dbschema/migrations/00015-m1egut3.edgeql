CREATE MIGRATION m1egut3amvxd5hvetdj23jcjkyqkscwbrhcb3e7p6jjufw3xr47d7a
    ONTO m134f3eja3e4h67lcrqcs2ogwteeebnbvy5xadcrczobmsoqpbpowa
{
  CREATE SCALAR TYPE anilist::MediaSeason EXTENDING enum<WINTER, SPRING, SUMMER, FALL>;
  ALTER TYPE anilist::Media {
      CREATE PROPERTY season -> anilist::MediaSeason;
      CREATE PROPERTY season_year -> std::int32;
  };
};
