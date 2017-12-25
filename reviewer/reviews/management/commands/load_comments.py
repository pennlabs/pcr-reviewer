import os
import sqlparse

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from ...models import Comment, Instructor, Section


class Command(BaseCommand):
    help = "Imports reviews from a sql file."

    def add_arguments(self, parser):
        parser.add_argument("file", nargs="?", type=str)
        parser.add_argument("--fake", action="store_true", dest="fake", help="Don't actually import anything into the database.")

    def handle(self, *args, **options):
        if options["file"]:
            filename = os.path.abspath(options["file"])
        else:
            raise CommandError("You need to specify a file to load!")
        if not os.path.isfile(filename):
            raise CommandError("The file '{}' does not exist!".format(filename))

        fake = options["fake"]

        self.stdout.write("Loading from '{}'".format(filename))

        if fake:
            self.stdout.write(self.style.WARNING("Running in fake mode, no changes will be made to the database."))

        existing = Comment.objects.all().count()

        if existing > 0:
            self.stdout.write(self.style.WARNING("{} comments already exist the database.").format(existing))

        self.stdout.write("Parsing sql file...")

        with open(filename, "r") as f:
            parsed = sqlparse.parse(f.read())

        self.stdout.write(self.style.SUCCESS("Finished parsing sql file!"))

        instructors = set()
        sections = set()
        comments = 0
        long_comments = 0
        length_check = 20

        self.stdout.write("Importing records...")

        for statement in parsed:
            if statement.get_type() == "INSERT":
                # Parse information from sql
                info = statement[-2][1]
                info = [x for x in info if not (x.ttype == sqlparse.tokens.Whitespace or x.ttype == sqlparse.tokens.Punctuation)]
                inst_id = int(str(info[0])[1:-1])
                inst_name = str(info[1])[1:-1]
                section = str(info[3])[1:-1]
                term = str(info[2])[1:-1]
                text = str(info[-1])[1:-1].replace("''", "'")

                # Statistics
                instructors.add(inst_id)
                sections.add(section)
                comments += 1
                if len(text) >= length_check:
                    long_comments += 1

                if comments % 1000 == 0:
                    self.stdout.write("Imported {} records...".format(comments))

                if not fake:
                    # Get or create instructor
                    try:
                        inst, _ = Instructor.objects.get_or_create(
                            id=inst_id,
                            name=inst_name
                        )
                    except IntegrityError:
                        self.stdout.write(self.style.WARNING("Duplicate instructor object ({}, {}) with different names!").format(inst_id, inst_name))
                        inst = Instructor.objects.get(id=inst_id)

                    # Get or create section
                    sect, _ = Section.objects.get_or_create(
                        name=section,
                        term=term,
                        instructor=inst
                    )

                    # Create comment
                    Comment.objects.create(
                        section=sect,
                        text=text
                    )

        self.stdout.write(self.style.SUCCESS("Finished importing comment data!"))

        self.stdout.write(self.style.SUCCESS("Total Instructors: {}".format(len(instructors))))
        self.stdout.write(self.style.SUCCESS("Total Sections: {}".format(len(sections))))
        self.stdout.write(self.style.SUCCESS("Total Comments: {} ({} more than {} characters long)".format(comments, long_comments, length_check)))
