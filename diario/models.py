from django.db import models

class Pessoa(models.Model):
    nome = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='foto')

    def __str__(self):
        return self.nome 
    
class Diario(models.Model):

    tags_choices = (
    ('V', 'Viagem'),
    ('T', 'Trabalho')
    )

    titulo = models.CharField(max_length=100)
    tags = models.TextField()
    texto = models.TextField()
    pessoas = models.ManyToManyField(Pessoa, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo 

    def get_tags(self):
        return self.tags.split(',') if self.tags else []
    def set_tags(self, list_tags, reset=False):
        if not reset:
            existing_tags = set(self.get_tags()) #set (conjunto) que remove dados repetidos de uma lista
            list_tags = existing_tags.union(set(list_tags))
        
        self.tags = ','.join(list_tags)

class Tag(models.Model):
        
        codigo = models.CharField(max_length=1,unique=True)
        nome = models.CharField(max_length=20)

        def __str__(self):
             return self.nome 
