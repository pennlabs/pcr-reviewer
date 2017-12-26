import os
import json

from django.core.management.base import BaseCommand, CommandError

from ...models import Section, Tag
from ...helpers import get_best_comments


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

        self.stdout.write("Exporting to '{}'".format(filename))

        self.stdout.write("Generating output...")

        sections = Section.objects.all()
        for section in sections:
            output.append({
                "term": section.term,
                "instructor": {
                    "id": section.instructor.id,
                    "name": section.instructor.name
                },
                "section": section.name,
                "comments": list(get_best_comments(section)),
                "tags": list(Tag.objects.filter(review__section=section).distinct().values_list("name", flat=True))
            })

        self.stdout.write("Exporting to json...")

        with open(filename, "w") as outfile:
            json.dump(output, outfile, sort_keys=True, indent=4)

        self.stdout.write(self.style.SUCCESS("{} reviews exported!".format(sections.count())))
