CREATE MIGRATION m1fibjb65ikohyekq75dj5exzzwaipmzoqldo7vyhodxpkglbdx44q
    ONTO m1lyp3h2y47mktrtmxcvv2quinwm3ur6bb3zttsg7rjzgz53lr6a4a
{
  ALTER TYPE user::Profile {
      CREATE PROPERTY birthday: std::datetime;
      CREATE PROPERTY pronouns: std::str;
      CREATE PROPERTY n7_major: std::str;
      CREATE PROPERTY graduation_year: std::int16;
      DROP PROPERTY promotion;
  };
};
