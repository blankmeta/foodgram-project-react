import pytest

TAGS_COUNT = 3


@pytest.fixture
def create_three_tags(user):
    from recipes.models import Tag

    for i in range(TAGS_COUNT):
        Tag.objects.create(
            name=f'tag_num_{i}',
            color='#123456'
        )
