import re
from enum import Enum
from typing import Any, Literal, Optional

from pydantic import BaseModel

from nanapi.database.anilist.account_merge import ACCOUNT_MERGE_SERVICE
from nanapi.database.anilist.media_select import MediaSelectResult
from nanapi.models.waicolle import RANKS, WaicolleRank


##################
# AniList models #
##################
class AnilistService(str, Enum):
    ANILIST = 'ANILIST'
    MYANIMELIST = 'MYANIMELIST'


ANILIST_SERVICES = Literal['ANILIST', 'MYANIMELIST']


class MediaType(str, Enum):
    ANIME = 'ANIME'
    MANGA = 'MANGA'


MEDIA_TYPES = Literal['ANIME', 'MANGA']


class MediaTag(BaseModel):
    id: int
    rank: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    isAdult: Optional[bool] = None

    def to_edgedb(self):
        data = dict(id_al=self.id,
                    rank=self.rank,
                    name=self.name,
                    description=self.description,
                    category=self.category,
                    is_adult=self.isAdult)
        return data


class ALPageInfo(BaseModel):
    currentPage: int
    hasNextPage: bool


class ALBaseModel(BaseModel):
    id: int
    favourites: Optional[int] = None
    siteUrl: Optional[str] = None

    def to_edgedb(self) -> Any:
        data = dict(id_al=self.id,
                    favourites=self.favourites,
                    site_url=self.siteUrl)
        return data

    def __hash__(self):
        return hash(self.id)


class ALMediaTitle(BaseModel):
    userPreferred: str
    english: Optional[str] = None
    native: Optional[str] = None


class ALMediaCoverImage(BaseModel):
    extraLarge: str
    color: Optional[str] = None


class ALCharacterConnection(BaseModel):
    pageInfo: ALPageInfo
    nodes: list['ALCharacter']


class ALMedia(ALBaseModel):
    type: Optional[MEDIA_TYPES] = None
    idMal: Optional[int] = None
    title: Optional[ALMediaTitle] = None
    synonyms: Optional[list[str]] = None
    description: Optional[str] = None
    status: Optional[Literal['FINISHED', 'RELEASING', 'NOT_YET_RELEASED',
                             'CANCELLED', 'HIATUS']] = None
    season: Optional[Literal['WINTER', 'SPRING', 'SUMMER', 'FALL']] = None
    seasonYear: Optional[int] = None
    episodes: Optional[int] = None
    duration: Optional[int] = None
    chapters: Optional[int] = None
    coverImage: Optional[ALMediaCoverImage] = None
    popularity: Optional[int] = None
    isAdult: Optional[bool] = None
    genres: Optional[list[str]] = None
    tags: Optional[list[MediaTag]] = None
    characters: Optional[ALCharacterConnection] = None

    def to_edgedb(self):
        data = super().to_edgedb()
        data |= dict(
            type=self.type,
            id_mal=self.idMal,
            synonyms=self.synonyms,
            description=(self.description if self.description else None),
            status=self.status,
            season=self.season,
            season_year=self.seasonYear,
            episodes=self.episodes,
            duration=self.duration,
            chapters=self.chapters,
            popularity=self.popularity,
            is_adult=self.isAdult,
            genres=self.genres)
        if self.title is not None:
            data |= dict(title_user_preferred=self.title.userPreferred,
                         title_english=self.title.english,
                         title_native=self.title.native)
        if self.coverImage is not None:
            data |= dict(cover_image_extra_large=self.coverImage.extraLarge,
                         cover_image_color=self.coverImage.color)
        if self.tags is not None:
            data |= dict(tags=[tag.to_edgedb() for tag in self.tags])
        return data


class ALStaffName(BaseModel):
    userPreferred: str
    alternative: Optional[list[str]] = None
    native: Optional[str] = None


class ALStaffImage(BaseModel):
    large: str


class ALStaffDate(BaseModel):
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None


class ALStaff(ALBaseModel):
    name: Optional[ALStaffName] = None
    image: Optional[ALStaffImage] = None
    description: Optional[str] = None
    gender: Optional[str] = None
    dateOfBirth: Optional[ALStaffDate] = None
    dateOfDeath: Optional[ALStaffDate] = None
    age: Optional[int] = None
    characters: Optional['ALStaffCharacterConnection'] = None

    def to_edgedb(self):
        data = super().to_edgedb()
        data |= dict(
            description=(self.description if self.description else None),
            gender=self.gender,
            age=self.age,
        )
        if self.name:
            data |= dict(name_user_preferred=self.name.userPreferred,
                         name_alternative=self.name.alternative,
                         name_native=self.name.native)
        if self.image:
            data |= dict(image_large=self.image.large)
        if self.dateOfBirth:
            data |= dict(date_of_birth_year=self.dateOfBirth.year,
                         date_of_birth_month=self.dateOfBirth.month,
                         date_of_birth_day=self.dateOfBirth.day)
        if self.dateOfDeath:
            data |= dict(date_of_death_year=self.dateOfDeath.year,
                         date_of_death_month=self.dateOfDeath.month,
                         date_of_death_day=self.dateOfDeath.day)
        return data


class ALMediaEdge(BaseModel):
    node: ALMedia
    voiceActors: list[ALStaff]
    characterRole: Optional[Literal['MAIN', 'SUPPORTING', 'BACKGROUND']] = None

    def to_edgedb(self):
        sorted_va = sorted(self.voiceActors,
                           key=lambda va: -(va.favourites or 0))
        data = dict(media=self.node.to_edgedb(),
                    voice_actors=[va.to_edgedb() for va in sorted_va],
                    character_role=self.characterRole)
        return data


class ALMediaConnection(BaseModel):
    pageInfo: ALPageInfo
    edges: list[ALMediaEdge]


class ALCharacterName(BaseModel):
    userPreferred: str
    alternative: list[str]
    alternativeSpoiler: list[str]
    native: Optional[str] = None


class ALCharacterImage(BaseModel):
    large: str


class ALCharacterDate(BaseModel):
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None


female_prog = re.compile(r'\b(she|her)\b', re.IGNORECASE)
male_prog = re.compile(r'\b(he|his)\b', re.IGNORECASE)


class ALCharacter(ALBaseModel):
    name: Optional[ALCharacterName] = None
    image: Optional[ALCharacterImage] = None
    description: Optional[str] = None
    gender: Optional[str] = None
    dateOfBirth: Optional[ALCharacterDate] = None
    age: Optional[str] = None
    media: Optional[ALMediaConnection] = None

    @property
    def rank(self):
        assert self.favourites is not None
        if self.favourites >= RANKS[WaicolleRank.S].min_favourites:
            return WaicolleRank.S
        elif self.favourites >= RANKS[WaicolleRank.A].min_favourites:
            return WaicolleRank.A
        elif self.favourites >= RANKS[WaicolleRank.B].min_favourites:
            return WaicolleRank.B
        elif self.favourites >= RANKS[WaicolleRank.C].min_favourites:
            return WaicolleRank.C
        elif self.favourites >= RANKS[WaicolleRank.D].min_favourites:
            return WaicolleRank.D
        else:
            return WaicolleRank.E

    @property
    def fuzzy_gender(self) -> Optional[str]:
        if self.gender is not None:
            return self.gender

        if self.description is not None:
            female = female_prog.findall(self.description)
            male = male_prog.findall(self.description)

            if len(female) != len(male) and max(len(female),
                                                len(male)) >= 3 * min(len(female), len(male)):
                return 'Female' if len(female) > len(male) else 'Male'

        return None

    def to_edgedb(self, include_computed=False):
        data = super().to_edgedb()
        data |= dict(
            description=(self.description if self.description else None),
            gender=self.gender,
            age=self.age)
        if self.name is not None:
            data |= dict(name_user_preferred=self.name.userPreferred,
                         name_alternative=self.name.alternative,
                         name_alternative_spoiler=self.name.alternativeSpoiler,
                         name_native=self.name.native)
        if self.image is not None:
            data |= dict(image_large=self.image.large)
        if self.dateOfBirth is not None:
            data |= dict(date_of_birth_year=self.dateOfBirth.year,
                         date_of_birth_month=self.dateOfBirth.month,
                         date_of_birth_day=self.dateOfBirth.day)
        if include_computed:
            data |= dict(rank=self.rank, fuzzy_gender=self.fuzzy_gender)
        return data


class ALStaffCharacterEdge(BaseModel):
    node: ALCharacter
    media: list[ALMedia]


class ALStaffCharacterConnection(BaseModel):
    pageInfo: ALPageInfo
    edges: list[ALStaffCharacterEdge]


ALCharacterConnection.update_forward_refs()
ALStaff.update_forward_refs()


##############
# MAL models #
##############
class MALListRespDataEntryListStatus(BaseModel):
    is_rewatching: bool | None = None
    is_rereading: bool | None = None
    num_episodes_watched: int | None = None
    num_chapters_read: int | None = None
    score: int
    status: str


class MALListRespDataEntryNode(BaseModel):
    id: int


class MALListRespDataEntry(BaseModel):
    list_status: MALListRespDataEntryListStatus
    node: MALListRespDataEntryNode


class MALListRespPaging(BaseModel):
    previous: str | None = None
    next: str | None = None


class MALListResp(BaseModel):
    data: list[MALListRespDataEntry]
    paging: MALListRespPaging


##################
# FastAPI models #
##################
class UpsertAnilistAccountBody(BaseModel):
    discord_username: str
    service: ACCOUNT_MERGE_SERVICE
    username: str


class MediaTitleAutocompleteResult(BaseModel):
    id_al: int
    title_user_preferred: str
    type: MediaType


class CharaNameAutocompleteResult(BaseModel):
    id_al: int
    name_user_preferred: str
    name_native: str | None = None


class StaffNameAutocompleteResult(BaseModel):
    id_al: int
    name_user_preferred: str
    name_native: str | None = None


class RecommendationResult(BaseModel):
    media: MediaSelectResult
    score: float
