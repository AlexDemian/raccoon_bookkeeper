from django.shortcuts import render


def CV(request):
    import datetime
    birth_date = datetime.datetime(year=1992, month=3, day=1)
    developer_from_date = datetime.datetime(year=2016, month=12, day=1)
    date_now = datetime.date.today()

    age = date_now.year - birth_date.year - ((date_now.month, date_now.day) < (birth_date.month, birth_date.day))
    experience_years = date_now.year - developer_from_date.year - ((date_now.month, date_now.day) < (developer_from_date.month, developer_from_date.day))


    context = {

        'age': age,
        'experience': experience_years,
        'skills': {
            'Backend': [
                ('Python', 4),
                ('Django', 3),
                ('Nginx', 4),
            ],

            'Frontend': [
                ('JS', 2),
                ('jQuery', 3),
                ('VueJS', 3),
                ('HTML', 4),
                ('CSS', 3),
                ('Bootstrap', 3)
            ],

            'Template engine': [
                ('Jinja2', 3)
            ],

            'Tools': [
                ('Git', 3),
                ('Docker', 3),
                ('Supervisor', 4),
            ],

            'Testing': [
                ('Selenium', 4),
                ('Unit testing', 1)
            ],

            'Databases(SQL / noSQL)': [
                ('PostgreSQL', 4),
                ('Django ORM', 3),
                ('Redis', 4)
            ],

            'VoIP': [
                ('Asterisk', 3)
            ],

            'Python libs': [
                ('Pandas', 2),
                ('Numpy', 3),
                ('Pydub', 3)
            ]


        }
    }

    return render(request, 'cv.html', context)