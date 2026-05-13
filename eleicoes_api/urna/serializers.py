import re
from rest_framework import serializers
from .models import Eleitor, Eleicao, Candidato, AptidaoEleitor, RegistroVotacao, Voto

class EleitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eleitor
        fields = '__all__' 

    def validate_cpf(self, value):
        cpf_regex = r'^\d{3}\.\d{3}\.\d{3}-\d{2}$'
        if not re.match(cpf_regex, value):
            raise serializers.ValidationError(
                "O CPF deve seguir o formato 000.000.000-00."
            )
        return value

class EleicaoSerializer(serializers.ModelSerializer):
    status_display = serializers.ReadOnlyField(source='get_status_display')
    total_candidatos = serializers.SerializerMethodField()
    total_aptos = serializers.SerializerMethodField()

    class Meta:
        model = Eleicao
        fields = '__all__' 

    def get_total_candidatos(self, obj):
        return obj.candidatos.count()

    def get_total_aptos(self, obj):
        return obj.aptos.count()

class CandidatoSerializer(serializers.ModelSerializer):
    eleicao_titulo = serializers.ReadOnlyField(source='eleicao.titulo')

    class Meta:
        model = Candidato
        fields = '__all__' 

    def validate_numero(self, value):
        if value == 0:
            raise serializers.ValidationError(
                "O número 0 não pode ser usado por candidatos, pois é reservado para votos em branco."
            )
        return value

class AptidaoEleitorSerializer(serializers.ModelSerializer):
    eleitor_nome = serializers.ReadOnlyField(source='eleitor.nome')
    eleicao_titulo = serializers.ReadOnlyField(source='eleicao.titulo')

    class Meta:
        model = AptidaoEleitor
        fields = '__all__' 

class RegistroVotacaoSerializer(serializers.ModelSerializer):
    eleitor_nome = serializers.ReadOnlyField(source='eleitor.nome')
    eleicao_titulo = serializers.ReadOnlyField(source='eleicao.titulo')

    class Meta:
        model = RegistroVotacao
        fields = '__all__' 
        read_only_fields = ['eleitor', 'eleicao', 'data_hora']

class VotoSerializer(serializers.ModelSerializer):
    candidato_nome_urna = serializers.ReadOnlyField(
        source='candidato.nome_urna', 
        allow_null=True
    )
    em_branco_display = serializers.SerializerMethodField()

    class Meta:
        model = Voto
        exclude = ['comprovante_hash']
        read_only_fields = ['id', 'eleicao', 'candidato', 'em_branco', 'data_hora']

    def get_em_branco_display(self, obj):
        return 'BRANCO' if obj.em_branco else None
    


class VotacaoInputSerializer(serializers.Serializer):
    eleitor_id = serializers.IntegerField()
    eleicao_id = serializers.IntegerField()
    candidato_id = serializers.IntegerField(required=False, allow_null=True)
    em_branco = serializers.BooleanField(default=False)

    def validate(self, data):
        e_id = data.get('eleitor_id')
        el_id = data.get('eleicao_id')
        c_id = data.get('candidato_id')
        branco = data.get('em_branco')

        eleicao = Eleicao.objects.get(pk=el_id)
        if eleicao.status != 'aberta':
            raise serializers.ValidationError("A eleição não está aberta.") 

        if not AptidaoEleitor.objects.filter(eleitor_id=e_id, eleicao_id=el_id).exists():
            raise serializers.ValidationError("Eleitor não está apto.") 

        if RegistroVotacao.objects.filter(eleitor_id=e_id, eleicao_id=el_id).exists():
            raise serializers.ValidationError("Você já votou nesta eleição.") 

        if branco and c_id:
            raise serializers.ValidationError("Não pode votar em branco e no candidato ao mesmo tempo.") 
        
        if not branco and not c_id:
            raise serializers.ValidationError("Escolha um candidato ou vote em branco.") 

        return data