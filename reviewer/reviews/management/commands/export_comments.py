import os
import json

from django.core.management.base import BaseCommand, CommandError

from ...models import Section, Comment, Tag


class Command(BaseCommand):
    help = "Exports reviews to a json file."

    def add_arguments(self, parser):
        parser.add_argument("file", nargs="?", type=str, default="reviews.json")

    def handle(self, *args, **options):
        if options["file"]:
            filename = os.path.abspath(options["file"])
        else:
            raise CommandError("You need to specify a file to save to!")

        output = []

        self.stdout.write("Generating output...")

        for section in Section.objects.all():
            output.append({
                "term": section.term,
                "instructor": {
                    "id": section.instructor.id,
                    "name": section.instructor.name
                },
                "section": section.name,
                "comments": list(set(Comment.objects.filter(section=section, commentrating__rating__lt=2).values_list("text", flat=True))),
                "tags": list(Tag.objects.filter(review__section=section).values_list("name", flat=True))
            })

        self.stdout.write("Exporting to json...")

        with open(filename, "w") as outfile:
            json.dump(output, outfile, sort_keys=True, indent=4)

        self.stdout.write(self.style.SUCCESS("Reviews exported!"))
