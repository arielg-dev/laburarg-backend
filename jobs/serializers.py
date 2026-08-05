from rest_framework import serializers

from .models import Job


class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.StringRelatedField(source="company")

    class Meta:
        model = Job
        fields = [
            "id",
            "company",
            "company_name",
            "title",
            "description",
            "requirements",
            "province",
            "city",
            "modality",
            "contract_type",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def validate(self, attrs):
        """
        validate() se ejecuta DESPUÉS de que cada campo individual
        ya pasó sus propias validaciones, y sirve para reglas que
        involucran VARIOS campos a la vez o requieren consultar
        otros datos (como en este caso, contar cuántos jobs tiene
        ya la empresa).

        Solo aplica esta regla cuando se está CREANDO un aviso
        nuevo (self.instance es None), o cuando se está ACTIVANDO
        uno que antes no estaba activo -- no queremos bloquear
        ediciones de avisos que ya existían y ya estaban activos.
        """
        company = attrs.get("company") or (
            self.instance.company if self.instance else None
        )
        new_status = attrs.get("status", getattr(self.instance, "status", None))

        is_new_active_job = (
            new_status == Job.Status.ACTIVE
            and (self.instance is None or self.instance.status != Job.Status.ACTIVE)
        )

        if company and is_new_active_job:
            self._validate_job_limit(company)

        return attrs

    def _validate_job_limit(self, company):
        # getattr con default None: como Subscription es OneToOne,
        # si la empresa no tiene ninguna, acceder a
        # company.subscription lanzaría un error. getattr con un
        # tercer argumento evita ese error y nos da None en su lugar.
        subscription = getattr(company, "subscription", None)
        has_unlimited = subscription and subscription.has_unlimited_jobs

        if company.is_agency and not has_unlimited:
            raise serializers.ValidationError(
                "Las consultoras/agencias necesitan una suscripción "
                "activa para publicar búsquedas."
            )

        if not company.is_agency and not has_unlimited:
            active_jobs_count = company.jobs.filter(
                status=Job.Status.ACTIVE
            ).count()
            if active_jobs_count >= 5:
                raise serializers.ValidationError(
                    "Alcanzaste el límite de 5 búsquedas activas del "
                    "plan gratuito. Actualizá tu plan para publicar más."
                )