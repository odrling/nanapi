CREATE MIGRATION m1n2saa24miuujihs3er6idi2bphct3bxohztethbtmbobgbra5fwa
    ONTO m1kcicmm33tphhg355yyt2azjsijzp3hwk63oxfj2qsz22iyi2hhcq
{
  ALTER TYPE default::ClientObject {
      ALTER LINK client {
          ON TARGET DELETE DELETE SOURCE;
      };
  };
};
