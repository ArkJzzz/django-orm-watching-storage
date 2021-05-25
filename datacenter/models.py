import django
from django.db import models



class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved= "leaved at " + str(self.leaved_at) if self.leaved_at else "not leaved"
        )

    def get_duration(self):
        '''
        Рассчитывает длительность визита. 
        Возвращает объект datetime.timedelta
        '''
        entered_at = django.utils.timezone.localtime(self.entered_at)
        leaved_at = django.utils.timezone.localtime(self.leaved_at)
        if not leaved_at:
            leaved_at = django.utils.timezone.localtime()

        return leaved_at - entered_at


    def is_long(self, minutes=60):
        '''
        Определяет, подозрителен визит или нет. 
        Возвращает True или False
        '''
        duration = self.get_duration()
        duration = duration.total_seconds()
        duration = duration // 60

        return int(duration) > int(minutes)
