from collections import defaultdict

from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from wagtail import blocks
from wagtail.blocks.struct_block import StructBlockValidationError
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock

from utils.struct_values import CardStructValue, LinkStructValue


class AccordionBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255)
    content = blocks.RichTextBlock()

    class Meta:
        label = "Section"
        icon = "title"


class AccordionBlock(blocks.StructBlock):
    heading = blocks.ListBlock(AccordionBlock())
    list = blocks.ListBlock(AccordionBlock())

    class Meta:
        icon = "list-ol"
        template = "components/accordion/accordion.html"


class CaptionedImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    image_alt_text = blocks.CharBlock(
        required=False,
        help_text="If left blank, the image's global alt text will be used.",
    )
    caption = blocks.CharBlock(required=False)

    class Meta:
        icon = "image"
        template = "components/streamfield/blocks/image_block.html"


class InternalLinkBlock(blocks.StructBlock):
    page = blocks.PageChooserBlock()
    title = blocks.CharBlock(
        required=False,
        help_text="Leave blank to use page's listing title.",
    )

    class Meta:
        icon = "link"
        value_class = LinkStructValue


class ArticlePageLinkBlock(InternalLinkBlock):
    page = blocks.PageChooserBlock(
        page_type="news.ArticlePage",
    )


class ExternalLinkBlock(blocks.StructBlock):
    link = blocks.URLBlock()
    title = blocks.CharBlock()

    class Meta:
        icon = "link"
        value_class = LinkStructValue


class LinkStreamBlock(blocks.StreamBlock):
    """
    StreamBlock that allows editors to add a single link of type internal or external.
    """

    internal = InternalLinkBlock()
    external = ExternalLinkBlock()

    class Meta:
        icon = "link"
        label = "Link"
        min_num = 1
        max_num = 1


class QuoteBlock(blocks.StructBlock):
    quote = blocks.TextBlock(form_classname="title")
    attribution = blocks.CharBlock(required=False)

    class Meta:
        icon = "openquote"
        template = "components/streamfield/blocks/quote_block.html"


class CardBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=255)
    description = blocks.RichTextBlock(required=False, features=["bold", "italic"])
    link = LinkStreamBlock(required=False, min_num=0)

    class Meta:
        icon = "form"
        template = "components/streamfield/blocks/card_block.html"
        label = "Card"
        value_class = CardStructValue


class FeaturedArticleBlock(blocks.StructBlock):
    link = ArticlePageLinkBlock()
    image = ImageChooserBlock(
        required=False,
        help_text="Set to override the image of the chosen article page.",
    )
    description = blocks.TextBlock(
        max_length=255,
        required=False,
        help_text="Choose to override a page's listing summary or introduction.",
    )
    cta_text = blocks.CharBlock(
        max_length=255,
        blank=False,
        help_text="This is the cta link text. This will automatically redirect to the article page.",
    )
    left_aligned = blocks.BooleanBlock(
        required=False,
        help_text="If checked, the text will be left-aligned.",
    )

    class Meta:
        icon = "doc-full"
        template = "components/streamfield/blocks/feature_block.html"


class BaseSectionBlock(blocks.StructBlock):
    heading = blocks.CharBlock(
        form_classname="title",
        icon="title",
        required=True
    )  # Should use H2s only
    sr_only_label = blocks.BooleanBlock(
        required=False,
        label="Screen reader only label",
        help_text="If checked, the heading will be hidden from view and avaliable to screen-readers only.",
    )

    class Meta:
        abstract = True
        icon = "title"


class StatisticSectionBlock(BaseSectionBlock):
    statistics = blocks.ListBlock(
        SnippetChooserBlock(
            "utils.Statistic"
        ),
        max_num=3,
        min_num=3,
    )

    class Meta:
        icon = "snippet"
        template = "components/streamfield/blocks/stat_block.html"


class CTASectionBlock(blocks.StructBlock):
    heading = blocks.CharBlock(
        form_classname="title",
        icon="title",
        required=True
    )
    link = LinkStreamBlock()
    description = blocks.TextBlock(required=False)

    class Meta:
        icon = "link"
        label = "CTA"
        template = "components/streamfield/blocks/cta_block.html"


class BaseCardSectionBlock(BaseSectionBlock):
    cards = blocks.ListBlock(
        CardBlock(),
        max_num=6,
        min_num=3,
        label="Card",
    )
    class Meta:
        abstract = True
        icon = "form"


class CardSectionBlock(BaseCardSectionBlock):
    class Meta:
        template = "components/streamfield/blocks/card_section_block.html"


class PlainCardSectionBlock(BaseCardSectionBlock):
    class Meta:
        icon = "doc-full"
        template = "components/streamfield/blocks/plain_cards_block.html"


class SectionBlocks(blocks.StreamBlock):
    paragraph = blocks.RichTextBlock(
        features=["bold", "italic", "link", "ol", "ul", "h3"],
        template="components/streamfield/blocks/paragraph_block.html",
    )


class SectionBlock(blocks.StructBlock):
    heading = blocks.CharBlock(
        form_classname="title",
        icon="title",
        template="components/streamfield/blocks/heading2_block.html",
    )
    content = SectionBlocks()

    class Meta:
        icon = "doc-full"
        template = "components/streamfield/blocks/section_block.html"


# PrelineUI StreamField Blocks
class PrelineAccordionItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255, help_text="Accordion item title")
    content = blocks.RichTextBlock(features=["bold", "italic", "link", "ol", "ul"])

    class Meta:
        label = "Accordion Item"
        icon = "list-ul"


class PrelineAccordionBlock(blocks.StructBlock):
    heading = blocks.CharBlock(
        max_length=255, 
        required=False,
        help_text="Optional heading for the accordion section"
    )
    items = blocks.ListBlock(
        PrelineAccordionItemBlock(),
        min_num=1,
        help_text="Add accordion items"
    )

    class Meta:
        icon = "list-ol"
        template = "components/streamfield/blocks/preline_accordion.html"
        label = "PrelineUI Accordion"


class PrelineAlertBlock(blocks.StructBlock):
    ALERT_TYPES = [
        ('info', 'Info'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    ]
    
    alert_type = blocks.ChoiceBlock(
        choices=ALERT_TYPES,
        default='info',
        help_text="Choose the alert type"
    )
    title = blocks.CharBlock(
        max_length=255,
        required=False,
        help_text="Optional alert title"
    )
    content = blocks.RichTextBlock(
        features=["bold", "italic", "link"],
        help_text="Alert message content"
    )

    class Meta:
        icon = "warning"
        template = "components/streamfield/blocks/preline_alert.html"
        label = "PrelineUI Alert"


class PrelineCardBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255)
    description = blocks.RichTextBlock(
        required=False, 
        features=["bold", "italic", "link"]
    )
    image = ImageChooserBlock(required=False)
    link = LinkStreamBlock(required=False, min_num=0)
    card_style = blocks.ChoiceBlock(
        choices=[
            ('default', 'Default'),
            ('bordered', 'Bordered'),
            ('shadow', 'Shadow'),
        ],
        default='default'
    )

    class Meta:
        icon = "doc-full"
        template = "components/streamfield/blocks/preline_card.html"
        label = "PrelineUI Card"


class PrelineFeatureItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255, help_text="Feature title")
    description = blocks.TextBlock(help_text="Feature description")
    icon_svg = blocks.TextBlock(
        required=False,
        help_text="SVG icon code (optional)"
    )

    class Meta:
        label = "Feature Item"
        icon = "tick"


class PrelineFeaturesBlock(blocks.StructBlock):
    heading = blocks.CharBlock(
        max_length=255,
        help_text="Main heading for the features section"
    )
    description = blocks.TextBlock(
        required=False,
        help_text="Description text below the heading"
    )
    image = ImageChooserBlock(
        required=False,
        help_text="Optional hero image for the features section"
    )
    features = blocks.ListBlock(
        PrelineFeatureItemBlock(),
        min_num=1,
        help_text="Add feature items"
    )

    class Meta:
        icon = "list-ul"
        template = "components/streamfield/blocks/preline_features.html"
        label = "PrelineUI Features"


# PrelineUI Hero Section Blocks
class PrelineHeroButtonBlock(blocks.StructBlock):
    text = blocks.CharBlock(max_length=255, help_text="Button text")
    url = blocks.URLBlock(help_text="Button URL")
    style = blocks.ChoiceBlock(
        choices=[
            ('primary', 'Primary'),
            ('secondary', 'Secondary'),
            ('outline', 'Outline'),
        ],
        default='primary',
        help_text="Button style"
    )

    class Meta:
        label = "Button"
        icon = "link"


class PrelineHeroReviewBlock(blocks.StructBlock):
    rating = blocks.IntegerBlock(
        min_value=1,
        max_value=5,
        default=5,
        help_text="Star rating (1-5)"
    )
    text = blocks.CharBlock(
        max_length=255,
        help_text="Review text"
    )
    author = blocks.CharBlock(
        max_length=255,
        help_text="Review author name"
    )

    class Meta:
        label = "Review"
        icon = "tick"


class PrelineHeroWithImageReviewsBlock(blocks.StructBlock):
    heading = blocks.CharBlock(
        max_length=255,
        help_text="Main hero heading"
    )
    subheading = blocks.TextBlock(
        required=False,
        help_text="Subheading text"
    )
    description = blocks.TextBlock(
        required=False,
        help_text="Description text"
    )
    image = ImageChooserBlock(
        required=False,
        help_text="Hero background image"
    )
    buttons = blocks.ListBlock(
        PrelineHeroButtonBlock(),
        min_num=1,
        max_num=2,
        help_text="Call-to-action buttons"
    )
    reviews = blocks.ListBlock(
        PrelineHeroReviewBlock(),
        min_num=1,
        max_num=2,
        help_text="Customer reviews"
    )

    class Meta:
        icon = "image"
        template = "components/streamfield/blocks/preline_hero_image_reviews.html"
        label = "Hero with Image & Reviews"


class PrelineHeroCenterVideoBlock(blocks.StructBlock):
    heading = blocks.CharBlock(
        max_length=255,
        help_text="Main hero heading"
    )
    subheading = blocks.TextBlock(
        required=False,
        help_text="Subheading text"
    )
    description = blocks.TextBlock(
        required=False,
        help_text="Description text"
    )
    background_image = ImageChooserBlock(
        required=False,
        help_text="Background image for video section"
    )
    video_url = blocks.URLBlock(
        required=False,
        help_text="Video URL (YouTube, Vimeo, etc.)"
    )
    play_button_text = blocks.CharBlock(
        max_length=255,
        default="Play the overview",
        help_text="Text for the play button"
    )

    class Meta:
        icon = "media"
        template = "components/streamfield/blocks/preline_hero_center_video.html"
        label = "Hero Center with Video"


class PrelineHeroSimpleBlock(blocks.StructBlock):
    heading = blocks.CharBlock(
        max_length=255,
        help_text="Main hero heading"
    )
    subheading = blocks.TextBlock(
        required=False,
        help_text="Subheading text"
    )
    description = blocks.TextBlock(
        required=False,
        help_text="Description text"
    )
    background_image = ImageChooserBlock(
        required=False,
        help_text="Optional background image"
    )
    buttons = blocks.ListBlock(
        PrelineHeroButtonBlock(),
        min_num=1,
        max_num=3,
        help_text="Call-to-action buttons"
    )

    class Meta:
        icon = "title"
        template = "components/streamfield/blocks/preline_hero_simple.html"
        label = "Hero Simple"


class StoryBlock(blocks.StreamBlock):
    # Hero Sections
    preline_hero_image_reviews = PrelineHeroWithImageReviewsBlock(group="Hero Sections")
    preline_hero_center_video = PrelineHeroCenterVideoBlock(group="Hero Sections")
    preline_hero_simple = PrelineHeroSimpleBlock(group="Hero Sections")
    
    # Content Sections
    section = SectionBlock(group="Content")
    cta = CTASectionBlock(group="Content")
    statistics = StatisticSectionBlock(group="Content")
    
    # PrelineUI Components
    preline_accordion = PrelineAccordionBlock(group="PrelineUI Components")
    preline_alert = PrelineAlertBlock(group="PrelineUI Components")
    preline_card = PrelineCardBlock(group="PrelineUI Components")
    preline_features = PrelineFeaturesBlock(group="PrelineUI Components")

    class Meta:
        template = "components/streamfield/stream_block.html"
