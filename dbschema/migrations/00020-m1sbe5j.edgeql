CREATE MIGRATION m1sbe5j6b6udweu2ah6uftugisxdyebbxlkpqugupnburuvapqakda
    ONTO m1feetbb32tka62czllwesfvtafxlxkt4idcqkwanjaptlhytvul4q
{
  ALTER TYPE projection::Projection {
      CREATE MULTI LINK participants: user::User {
          ON TARGET DELETE ALLOW;
      };
  };
};
