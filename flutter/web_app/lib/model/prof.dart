class Professor {
  final int id;
  final String firstName;
  final String lastName;
  final String email;
  final String? hireDate;
  final bool? isActive;
  final String? birthDate;
  final String? phoneNumber;
  final String? salary;
  final String? professorNumber;

  Professor({
    required this.id,
    required this.firstName,
    required this.lastName,
    required this.email,
    this.hireDate,
    this.isActive,
    this.birthDate,
    this.phoneNumber,
    this.salary,
    this.professorNumber,
  });

  factory Professor.fromJson(Map<String, dynamic> json) {
    return Professor(
      id: json['id'],
      firstName: json['firstname'],
      lastName: json['lastname'],
      email: json['email'],
      hireDate: json['hire_date'],
      isActive: json['is_active'],
      birthDate: json['birth_date'],
      phoneNumber: json['phone_number'],
      salary: json['salary'],
      professorNumber: json['professor_number'],
    );
  }
}
