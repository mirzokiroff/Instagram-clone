from itertools import cycle

import pytest
from factory.fuzzy import FuzzyChoice
from faker import Faker
from factory import DictFactory, LazyAttribute
from content.models import Post
from model_bakery import baker

faker = Faker()


class PostFactory(DictFactory):
    _first = LazyAttribute(
        lambda obj: faker.unique.first_name_male() if obj._gender == "M" else faker.first_name_female())
    _last = LazyAttribute(
        lambda obj: faker.unique.last_name_male() if obj._gender == "M" else faker.unique.last_name_female())
    _gender = FuzzyChoice(("M", "F"))

    username = LazyAttribute(lambda obj: f"{obj._first} {obj._last}")
    media = LazyAttribute(lambda obj: faker.random.choice((True, False)))

    class Meta:
        exclude = ("_gender", '_first', '_last', 'alt_text', 'archived', 'image_description', 'location_description',
                   'audio_description')
        rename = {'username': 'username', 'tag': 'tag', 'locate': 'location', 'media': 'media', 'text': 'text'}


@pytest.mark.django_db
class TestPosts:

    @pytest.fixture
    def test_post_model(self):
        count = Post.objects.count()
        baker.make(
            'content.Post',
            username=cycle(PostFactory()['username'] for _ in range(10)),
            media=cycle(PostFactory()['media'] for _ in range(10)),
            _quantity=10
        )
        count_last = Post.objects.count()

        assert count + 10 == count_last
        return Post.objects.all()

    def test_post_media_system(self, test_post_model):
        post = test_post_model
        post_ten = post[:10]
        username_ten = post[:10]
