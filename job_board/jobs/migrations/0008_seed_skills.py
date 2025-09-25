from django.db import migrations


def seed_skills(apps, schema_editor):
    Skill = apps.get_model('jobs', 'Skill')
    names = [
        'Python', 'Django', 'Flask', 'JavaScript', 'TypeScript', 'React', 'Node.js',
        'HTML', 'CSS', 'SQL', 'PostgreSQL', 'MySQL', 'MongoDB', 'Git', 'Docker',
        'Kubernetes', 'AWS', 'GCP', 'Azure', 'Linux', 'REST APIs', 'GraphQL',
        'Java', 'Spring', 'C#', '.NET', 'C++', 'Go', 'Swift', 'Kotlin',
        'Machine Learning', 'Data Science', 'Pandas', 'NumPy', 'TensorFlow', 'PyTorch'
    ]
    for n in names:
        Skill.objects.get_or_create(name=n)


def unseed_skills(apps, schema_editor):
    # Do not remove skills on reverse to avoid deleting data users may have referenced
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0007_jobapplication'),
    ]

    operations = [
        migrations.RunPython(seed_skills, unseed_skills),
    ]
