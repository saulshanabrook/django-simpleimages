import pytest

import simpleimages.utils


class TestTransformField:
    def test_blank_transform_wont_save(self, instance):
        simpleimages.utils.transform_field(
            instance=instance,
            source_field_name='image',
            destination_field_name='thumbnail',
            transformation=lambda file: None
        )

        assert not instance.thumbnail

    def test_will_save(self, instance):
        simpleimages.utils.transform_field(
            instance=instance,
            source_field_name='image',
            destination_field_name='thumbnail',
            transformation=lambda file: file
        )

        assert instance.thumbnail

    def test_yes_overwrite(self, instance_different_thumb):
        simpleimages.utils.transform_field(
            instance=instance_different_thumb,
            source_field_name='image',
            destination_field_name='thumbnail',
            transformation=lambda file: file
        )

        assert instance_different_thumb.thumbnail.width == instance_different_thumb.image.width

    def test_path_correct(self, instance):
        simpleimages.utils.transform_field(
            instance=instance,
            source_field_name='image',
            destination_field_name='thumbnail',
            transformation=lambda file: file
        )
        original_name = instance.image.name.split('/')[-1]
        new_path = 'thumbnails/' + original_name
        assert instance.thumbnail.name == new_path


@pytest.mark.usefixtures("call_on_rq_as_well")
class TestPerformTransformation:
    def test_all_fields(self, instance):
        simpleimages.utils.perform_transformation(instance)
        assert instance.thumbnail

    def test_one_field_transforms(self, instance):
        simpleimages.utils.perform_transformation(instance, ['image'])
        assert instance.thumbnail

    def test_without_field_doesnt_transform(self, instance):
        simpleimages.utils.perform_transformation(instance, ['not a field'])

        assert not instance.thumbnail


class TestPerformMultipleTransformations:
    def test_all_fields(self, instance):
        simpleimages.utils.perform_multiple_transformations([instance])
        assert instance.thumbnail

    def test_one_field_transforms(self, instance):
        simpleimages.utils.perform_multiple_transformations([instance], ['image'])
        assert instance.thumbnail

    def test_without_field_doesnt_transform(self, instance):
        simpleimages.utils.perform_multiple_transformations([instance], ['not a field'])

        assert not instance.thumbnail
