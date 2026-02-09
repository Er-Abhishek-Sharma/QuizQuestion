from django.db import models

class Candidate(models.Model):
    username = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=128) 
    name = models.CharField(max_length=30)
    test_attempted = models.IntegerField(default=0)
    points = models.FloatField(default=0.0)

    def __str__(self):
        return self.username


class Question(models.Model):
    qid = models.BigAutoField(primary_key=True)
    que = models.TextField()
    a = models.CharField(max_length=255)
    b = models.CharField(max_length=255)
    c = models.CharField(max_length=255)
    d = models.CharField(max_length=255)
    ans = models.CharField(max_length=1, choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')]) 

    def __str__(self):
        return f"Q{self.qid}: {self.que[:50]}"


class Result(models.Model):
    resultid = models.BigAutoField(primary_key=True)
    username = models.ForeignKey(Candidate, on_delete=models.CASCADE, db_column='username')
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    attempt = models.IntegerField()
    right = models.IntegerField()
    wrong = models.IntegerField()
    points = models.FloatField()

    def __str__(self):
        return f"Result {self.resultid} for {self.username.username}"
