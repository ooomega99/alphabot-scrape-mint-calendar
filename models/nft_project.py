from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class SocialMedia(Enum):
    CALENDAR = "Add to calendar"
    TWITTER = "Twitter"
    DISCORD = "Discord"
    INSTAGRAM = "Instagram"
    COLLECTION = "Collection"
    TELEGRAM = "telegram"


class AttributeCategory(Enum):
    SUPPLY = "Supply"
    WL = "WL"
    PRICE = "Price"
    PUBLIC = "Public"
    RAISE = "Raise"


@dataclass
class SocialMediaNft:
    name: SocialMedia
    url: str


@dataclass
class AttributeNft:
    name: AttributeCategory
    value: str


@dataclass
class NftProject:
    name: str
    background_url: str
    profile_url: str
    mint_datetime: datetime
    social_medias: list
    attributes: list

    def to_list(self):
        fmt_datetime = self.mint_datetime.strftime("%Y-%m-%d %H:%M")
        values = [fmt_datetime, f'=IMAGE("{self.profile_url}")', f'=IMAGE("{self.background_url}")', self.name]
        # Attribute
        for en in AttributeCategory:
            selected = None
            for attribute in self.attributes:
                if en != attribute.name:
                    continue
                selected = attribute
                break
            if selected is None:
                values.append('')
                continue
            print(f'selected.value: {selected.value}')
            values.append(selected.value)
        # Social Media
        for en in SocialMedia:
            selected = None
            for social_media in self.social_medias:
                if en != social_media.name:
                    continue
                selected = social_media
            if selected is None:
                values.append('')
                continue
            values.append(selected.url)
        print(f'values: {values}')
        return values

