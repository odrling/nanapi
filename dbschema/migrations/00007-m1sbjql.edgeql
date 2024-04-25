CREATE MIGRATION m1sbjqlnruo6x7qems6ukwa53puo3vsogettkok2dnhrcyin2wgcrq
    ONTO m1sc57pjblk5f5frr2toei7qv5ihtys6dplsy3g3rrf3mcg3el6uqa
{
  ALTER TYPE default::ClientObject {
      DROP ACCESS POLICY everyone_ro;
  };
};
