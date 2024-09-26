from rest_framework import serializers
from .models import User, Doctor, Appointment, Schedule

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Doctor
        fields = ['id', 'user', 'specialization', 'experience', 'rating']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        doctor = Doctor.objects.create(user=user, **validated_data)
        return doctor

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        # Update the User instance
        UserSerializer.update(UserSerializer(), instance=user, validated_data=user_data)

        # Update the Doctor instance
        instance.specialization = validated_data.get('specialization', instance.specialization)
        instance.experience = validated_data.get('experience', instance.experience)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance

class AppointmentSerializer(serializers.ModelSerializer):
    patient = UserSerializer()
    doctor = DoctorSerializer()

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'appointment_date', 'status']

    def create(self, validated_data):
        patient_data = validated_data.pop('patient')
        doctor_data = validated_data.pop('doctor')

        patient = UserSerializer.create(UserSerializer(), validated_data=patient_data)
        doctor = DoctorSerializer.create(DoctorSerializer(), validated_data=doctor_data)

        appointment = Appointment.objects.create(patient=patient, doctor=doctor, **validated_data)
        return appointment

    def update(self, instance, validated_data):
        patient_data = validated_data.pop('patient')
        doctor_data = validated_data.pop('doctor')

        patient = instance.patient
        doctor = instance.doctor

        # Update the User and Doctor instances
        UserSerializer.update(UserSerializer(), instance=patient, validated_data=patient_data)
        DoctorSerializer.update(DoctorSerializer(), instance=doctor, validated_data=doctor_data)

        # Update the Appointment instance
        instance.appointment_date = validated_data.get('appointment_date', instance.appointment_date)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

class ScheduleSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()

    class Meta:
        model = Schedule
        fields = ['id', 'doctor', 'available_date', 'start_time', 'end_time']

    def create(self, validated_data):
        doctor_data = validated_data.pop('doctor')
        doctor = DoctorSerializer.create(DoctorSerializer(), validated_data=doctor_data)
        schedule = Schedule.objects.create(doctor=doctor, **validated_data)
        return schedule

    def update(self, instance, validated_data):
        doctor_data = validated_data.pop('doctor')
        doctor = instance.doctor

        # Update the Doctor instance
        DoctorSerializer.update(DoctorSerializer(), instance=doctor, validated_data=doctor_data)

        # Update the Schedule instance
        instance.available_date = validated_data.get('available_date', instance.available_date)
        instance.start_time = validated_data.get('start_time', instance.start_time)
        instance.end_time = validated_data.get('end_time', instance.end_time)
        instance.save()
        return instance
