from django.core.management.base import BaseCommand, CommandError

from search.register import get_registered_models, add_to_search


class Command(BaseCommand):
    help = ""

    def add_arguments(self, parser):
        # TODO sync only one model
        # parser.add_argument("models", nargs="*", type=str)
        pass

    def handle(self, *args, **options):
        models = get_registered_models()
        for model in models:
            instances = model.objects.all()
            for instance in instances:
                try:
                    # TODO leverage `add_documents` for instance using the same
                    # index
                    add_to_search(instance)
                except Exception as error:
                    print("failed to process {} ({})".format(instance, error))
