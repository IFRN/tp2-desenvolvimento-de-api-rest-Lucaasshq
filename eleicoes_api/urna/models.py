from django.db import models
from django.core.exceptions import ValidationError

class Eleitor(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField()
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Eleicao(models.Model):
    TIPO = [
        ('estudantil', 'estudantil'),
        ('sindical', 'sindical'),
        ('associacao', 'associacao'),
        ('condominio', 'condominio'),
        ('conselho', 'conselho'),
        ('outra', 'outra'),
    ]
    
    STATUS = [
        ('rascunho', 'rascunho'),
        ('aberta', 'aberta'),
        ('encerrada', 'encerrada'),
        ('apurada', 'apurada'),
    ]

    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS, default='rascunho')
    permite_branco = models.BooleanField(default=True)
    criada_por = models.ForeignKey(Eleitor, on_delete=models.PROTECT, related_name='eleicoes_criadas')

    def clean(self):
        if self.data_inicio and self.data_fim and self.data_fim <= self.data_inicio:
            raise ValidationError("A data_fim deve ser maior que a data_inicio.")
        
        if self.pk:
            original = Eleicao.objects.get(pk=self.pk)
            if original.status == 'rascunho' and self.status not in ['rascunho', 'aberta']:
                raise ValidationError("Fluxo permitido: rascunho -> aberta.")
            if original.status == 'aberta' and self.status not in ['aberta', 'encerrada']:
                raise ValidationError("Fluxo permitido: aberta -> encerrada.")
            if original.status == 'encerrada' and self.status not in ['encerrada', 'apurada']:
                raise ValidationError("Fluxo permitido: encerrada -> apurada.")
            if original.status == 'apurada' and self.status != 'apurada':
                raise ValidationError("Uma eleição apurada não pode mais ser alterada.")

    def __str__(self):
        return self.titulo

class Candidato(models.Model):
    eleicao = models.ForeignKey(Eleicao, on_delete=models.CASCADE, related_name='candidatos')
    numero = models.PositiveIntegerField()
    nome = models.CharField(max_length=150)
    nome_urna = models.CharField(max_length=50)
    partido_ou_chapa = models.CharField(max_length=100, blank=True)
    proposta = models.TextField(blank=True)
    foto_url = models.URLField(blank=True)

    class Meta:
        unique_together = [('eleicao', 'numero')]

    def __str__(self):
        return f"{self.numero} - {self.nome_urna}"

class AptidaoEleitor(models.Model):
    eleitor = models.ForeignKey(Eleitor, on_delete=models.PROTECT, related_name='aptidoes')
    eleicao = models.ForeignKey(Eleicao, on_delete=models.CASCADE, related_name='aptos')
    data_inclusao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('eleitor', 'eleicao')]

class RegistroVotacao(models.Model):
    eleitor = models.ForeignKey(Eleitor, on_delete=models.PROTECT, related_name='registros_votacao')
    eleicao = models.ForeignKey(Eleicao, on_delete=models.PROTECT, related_name='registros_votacao')
    data_hora = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('eleitor', 'eleicao')]

class Voto(models.Model):
    eleicao = models.ForeignKey(Eleicao, on_delete=models.PROTECT, related_name='votos')
    candidato = models.ForeignKey(Candidato, on_delete=models.PROTECT, related_name='votos', null=True, blank=True)
    em_branco = models.BooleanField(default=False)
    data_hora = models.DateTimeField(auto_now_add=True)
    comprovante_hash = models.CharField(max_length=64, unique=True)

    def clean(self):
        if self.em_branco is True and self.candidato is not None:
            raise ValidationError("Voto em branco não deve possuir um candidato.")
        if self.em_branco is False and self.candidato is None:
            raise ValidationError("Informe o candidato ou selecione voto em branco.")

    def __str__(self):
        return f"Voto {self.id} na eleição {self.eleicao.titulo}"
        